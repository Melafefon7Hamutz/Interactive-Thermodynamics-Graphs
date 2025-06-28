

class Process:
    default_args = {}
    
    def __init__(self, parent, v0, p0, args=None):
        self.parent = parent
        self.plot_widget = parent.plot_widget
        self.vrange = self.parent.plot_widget.getViewBox().viewRange()[0]
        self.prange = self.parent.plot_widget.getViewBox().viewRange()[1]
        if self.vrange[0] <= 0:
            self.vrange = (1e-5, self.vrange[1])
        self.line = self.plot_widget.plot(*self.get_points(v0, p0), pen='red')
        self.edges = []
        self.point = (v0, p0)
        self.args = args

    def move_with(self, v0, p0):
        self.point = (v0, p0)
        self.update()

    def update(self):
        self.vrange = sorted([self.edges[0].x, self.edges[1].x])
        self.prange = sorted([self.edges[0].y, self.edges[1].y])
        self.line.setData(*self.get_points(*self.point))

    def set_edges(self, edges):
        self.edges = edges

    def get_edges(self):
        return self.edges

    def update_args(self, args):
        self.args = args