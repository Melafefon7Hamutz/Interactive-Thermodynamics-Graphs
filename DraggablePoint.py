import pyqtgraph as pg
from PyQt5.QtCore import Qt

# from MainWindow import MainWindow
from Process import Process


class DraggablePoint:
    def __init__(self, parent, x=0, y=0):
        self.parent = parent
        self.plot_widget = parent.plot_widget
        self.x = x
        self.y = y
        self.is_dragging = False
        self.neighbors: list[DraggablePoint] = []
        self.curves: list[Process] = []

        self.point = pg.ScatterPlotItem(
            pos=[[x, y]],
            size=30,
            brush='red',
            pen='black',
            symbol='o'
        )

        self.plot_widget.addItem(self.point)
        self.plot_view = self.plot_widget.getViewBox()

        self.point.mousePressEvent = self.mouse_press_event
        self.point.mouseMoveEvent = self.mouse_move_event
        self.point.mouseReleaseEvent = self.mouse_release_event

    def remove(self):
        self.plot_widget.removeItem(self.point)
        self.plot_view = None
        self.plot_widget = None
        self.parent = None
        self.neighbors = None
        self.curves = None
        self.point = None
        self.x = None
        self.y = None

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors

    def add_neighbor(self, p2):
        self.neighbors.append(p2)

    def remove_neighbor(self, p2):
        self.neighbors.remove(p2)

    def set_curves(self, curves):
        self.curves = curves

    def add_curve(self, process):
        self.curves.append(process)

    def get_neighbors(self):
        return self.neighbors

    def get_curves(self):
        return self.curves

    def get_curve_with(self, p2):
        for curve in self.curves:
            if p2 in curve.get_edges():
                return curve
        return None

    def move_to(self, x, y):
        self.x = x
        self.y = y
        self.point.setData(pos=[[self.x, self.y]])

    def mouse_press_event(self, event):
        """Handle mouse press on the point"""
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            # Disable the plot's mouse interaction
            self.plot_view.setMouseEnabled(x=False, y=False)
            event.accept()  # Accept the event to prevent it from propagating
        else:
            event.ignore()

    def mouse_move_event(self, event):
        """Handle mouse move events when dragging"""
        if self.is_dragging:
            # Convert screen coordinates to plot coordinates
            scene_pos = event.scenePos()
            mouse_point = self.plot_view.mapSceneToView(scene_pos)
            self.x = max(mouse_point.x(), 0)
            self.y = max(mouse_point.y(), 0)

            # Update point position
            self.point.setData(pos=[[self.x, self.y]])
            self.parent.on_point_drag(self)
            event.accept()
        else:
            event.ignore()

    def mouse_release_event(self, event):
        """Handle mouse release events"""
        if event.button() == Qt.LeftButton and self.is_dragging:
            self.is_dragging = False
            # Re-enable the plot's mouse interaction
            self.plot_view.setMouseEnabled(x=True, y=True)
            event.accept()
        else:
            event.ignore()
