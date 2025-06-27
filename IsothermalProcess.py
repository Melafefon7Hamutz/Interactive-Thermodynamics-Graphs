import numpy as np

from Process import Process


class IsothermalProcess(Process):
    def __init__(self, parent, p0, v0, args=None):
        super().__init__(parent, p0, v0, args)

    def get_points(self, v, p):
        self.c = p * v
        V = np.linspace(self.vrange[0], self.vrange[1], 100)
        P = p * v / V
        return V, P

    def get_equation(v, p, c, **kargs):
        return v * p - c

    def evaluate(self, v):
        return self.c / v
