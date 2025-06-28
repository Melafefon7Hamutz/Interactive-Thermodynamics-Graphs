import pyqtgraph as pg
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget
from PyQt5.QtCore import QSize

from DraggablePoint import DraggablePoint
from IsochoricProcess import IsochoricProcess
from Intersections import Intersector
from EnergyCalculator import EnergyCalculator

from UIWidget import UIWidget

R = 8.314  # Universal gas constant in J/(mol*K)


class MainWindow(QMainWindow):
    def __init__(self, screen_size: QSize):
        super().__init__()
        w = screen_size.width()
        h = screen_size.height()
        self.setGeometry((w-h)//2, h//20, h, h*17//20)

        # Create central widget and layout
        central_widget = QWidget()
        central_widget.setLayout(QHBoxLayout())
        self.setCentralWidget(central_widget)
        layout = central_widget.layout()

        self.setup_plot()

        # UI on the right
        self.UIwidget = UIWidget(self)
        layout.addWidget(self.UIwidget)

        # Intersector for intersecting curves
        self.intersector = Intersector()
        self.energty_calculator = EnergyCalculator()
        self.points = [DraggablePoint(self, 10, 20)]
        self.curves = []
        self.closed = False

        # default values
        self.number_of_moles = 1.0
        self.degrees_of_freedom = 3
        self.update_args()

        self.plot_widget.plotItem.enableAutoRange()

    def setup_plot(self):
        # Create PyQtGraph plot widget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.showGrid(x=True, y=True)
        plot_item = self.plot_widget.getPlotItem()
        pen = pg.mkPen(width=3)
        vline = pg.InfiniteLine(pos=0, angle=90, pen=pen)
        plot_item.addItem(vline)
        hline = pg.InfiniteLine(pos=0, angle=0, pen=pen)
        plot_item.addItem(hline)

        # Add plot widget to layout
        self.centralWidget().layout().addWidget(self.plot_widget)

    def update_args(self):
        self.args = {'dof': self.degrees_of_freedom,
                     'n': self.number_of_moles, 'R': R}

    def update_dof(self, dof):
        self.degrees_of_freedom = dof
        self.update_args()
        self.update_plot()
        self.update_readouts()

    def update_moles(self, moles):
        self.number_of_moles = moles
        self.update_args()
        # self.update_plot()
        self.update_readouts()

    def evaluete_process(self, process, v, p):
        # stupid exception
        if isinstance(process, IsochoricProcess):
            return process.evaluate(p), p
        else:
            return v, process.evaluate(v)

    def add_process(self, process_type, point: DraggablePoint = None):
        if point is None:
            point = self.points[-1]

        for process in point.get_curves():
            if type(process) == process_type:
                return

        self.intersector.add_process(process_type)
        process = process_type(self, point.x, point.y, self.args)

        end = DraggablePoint(self, *self.evaluete_process(
            process, point.x+5, point.y+5))

        process.set_edges([point, end])
        point.add_neighbor(end)
        point.add_curve(process)
        end.add_neighbor(point)
        end.add_curve(process)

        process.update()

        self.curves.append(process)
        self.points.append(end)
        self.update_readouts()

    def connect_ends(self):
        if self.closed:
            return
        # assume points are first and last in array
        p1: DraggablePoint = self.points[0]
        p2: DraggablePoint = self.points[-1]
        c1 = p1.get_curves()[0]
        c2 = p2.get_curves()[0]
        p1.move_to(*self.intersector.get_intersection(c1, c2, self.args))
        p3: DraggablePoint = p2.get_neighbors()[0]
        p3.remove_neighbor(p2)
        p3.add_neighbor(p1)
        p1.add_neighbor(p3)
        p1.add_curve(c2)
        c2.set_edges([p3, p1])
        c1.update()
        c2.update()
        p2.remove()
        self.points.remove(p2)
        self.closed = True
        self.update_readouts()

    def on_point_drag(self, point):
        self.plot_widget.plotItem.disableAutoRange()
        processes = point.get_curves()
        for process in processes:
            process.move_with(point.x, point.y)
            p2 = [p for p in process.get_edges() if p != point][0]
            if len(p2.get_curves()) == 2:
                p2.move_to(
                    *self.intersector.get_intersection(*p2.get_curves(), self.args))
            else:
                p2.move_to(p2.x, process.evaluate(p2.x))
        for p in point.get_neighbors():
            for process in p.get_curves():
                if process not in processes:
                    process.update()
        self.update_readouts()

    def update_plot(self):
        # bfs to update all curves and points
        points_to_update = set()
        points_to_update.add(self.points[0])
        visited = set()
        while points_to_update:
            point = points_to_update.pop()
            if point in visited:
                continue
            visited.add(point)
            for process in point.get_curves():
                process.update_args(self.args)
                process.move_with(point.x, point.y)
                for neighbor in process.get_edges():
                    if neighbor not in visited:
                        points_to_update.add(neighbor)
                        neighbor.move_to(
                            *self.evaluete_process(process, neighbor.x, neighbor.y))
                process.update()

    def update_readouts(self):
        wh = self.get_work_heat()
        tmin, tmax = self.get_temperature_range()
        eff = abs(wh[0] / wh[1]) if wh[1] != 0 else 0
        c_eff = 1 - tmin / tmax if tmin != tmax else 1
        readouts = {'Work Done': wh[0], "Heat Transfer": wh[1], "Efficiency": eff,
                    "Min Temperature": tmin, "Max Temperature": tmax, "Carnot Efficiency": c_eff, "Percentage of Carnot": eff / c_eff * 100}
        self.UIwidget.update_readouts(readouts)

    def get_work_heat(self):
        n = len(self.points)
        if n < 2:
            return 0.0, 0.0
        works, heats = [], []
        # assume points in order
        for i in range(n):
            p1 = self.points[i % n]
            p2 = self.points[(i + 1) % n]
            process = p1.get_curve_with(p2)
            if process is None:
                continue
            w, h = self.energty_calculator.calculate_work_heat(
                process, self.args)
            works.append(w)
            heats.append(h)
        work = sum(works)
        heat = sum([h for h in heats if h * work > 0])

        return work, heat

    def temperature(self, v, p):
        return p * v / (self.number_of_moles * R)

    def get_temperature_range(self):
        temps = [self.temperature(p.x, p.y) for p in self.points]
        return min(temps), max(temps)
