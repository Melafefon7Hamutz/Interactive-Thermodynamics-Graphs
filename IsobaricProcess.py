import numpy as np
import sympy as sp

from Process import Process


class IsobaricProcess(Process):
    def __init__(self, parent, p0, v0, args=None):
        super().__init__(parent, p0, v0, args)

    def get_points(self, v, p):
        self.c = p
        V = np.array([self.vrange[0], self.vrange[1]])
        P = p * np.ones(2)
        return V, P

    def get_equation(v, p, c, args):
        return sp.Eq(p, c)

    def evaluate(self, v):
        return self.c
