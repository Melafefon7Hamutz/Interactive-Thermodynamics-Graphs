import pyqtgraph as pg
import PyQt5
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget

from DraggablePoint import DraggablePoint
from Intersections import Intersector
from UIWidget import UIWidget

from IsochoricProcess import IsochoricProcess

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 1800, 1500)

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
        self.points = [DraggablePoint(self, 10, 20)]
        self.curves = []
        self.closed = False
        
        # Rescale the plot
        # self.plot_widget.setXRange(8, 20)
        # self.plot_widget.setYRange(10, 30)
        self.plot_widget.plotItem.enableAutoRange()


    def setup_plot(self):
        # Create PyQtGraph plot widget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.showGrid(x=True, y=True)

        # Set plot ranges
        # self.plot_widget.setXRange(0, 10)
        # self.plot_widget.setYRange(0, 5)

        # Add plot widget to layout
        self.centralWidget().layout().addWidget(self.plot_widget)

    def add_process(self, process_type, args, point: DraggablePoint = None):
        if point is None:
            point = self.points[-1]


        for process in point.get_curves():
            if type(process) == process_type:
                if process.is_args_equivalent(args):
                    return

        process = process_type(self, point.x, point.y, args)
        self.intersector.add_process(process)
        # stupid exception
        if type(process) != IsochoricProcess:
            v = point.x+5
            end = DraggablePoint(self, v, process.evaluate(v))
        else:
            p = point.y+5
            end = DraggablePoint(self, process.evaluate(p), p)

        process.set_edges([point, end])
        point.add_neighbor(end)
        point.add_curve(process)
        end.add_neighbor(point)
        end.add_curve(process)

        process.update()

        self.curves.append(process)
        self.points.append(end)

    def connect_ends(self):
        # assume points are first and last in array
        p1: DraggablePoint = self.points[0]
        p2: DraggablePoint = self.points[-1]
        c1 = p1.get_curves()[0]
        c2 = p2.get_curves()[0]
        p1.move_to(*self.intersector.get_intersection(c1, c2))
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

    def update(self, point):
        self.plot_widget.plotItem.disableAutoRange()
        processes = point.get_curves()
        for process in processes:
            process.move_with(point.x, point.y)
            p2 = [p for p in process.get_edges() if p != point][0]
            if len(p2.get_curves()) == 2:
                p2.move_to(
                    *self.intersector.get_intersection(*p2.get_curves()))
            else:
                p2.move_to(p2.x, process.evaluate(p2.x))
        for p in point.get_neighbors():
            for process in p.get_curves():
                if process not in processes:
                    process.update()
