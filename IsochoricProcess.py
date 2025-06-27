import numpy as np

from Process import Process


class IsochoricProcess(Process):
    def __init__(self, parent, p0, v0, args=None):
        super().__init__(parent, p0, v0, args)

    def get_points(self, v, p):
        self.c = v
        V = v * np.ones(2)
        P = np.array([self.prange[0], self.prange[1]])
        return V, P

    def get_equation(v, p, c, **kargs):
        return v - c

    def evaluate(self, p):
        return self.c
