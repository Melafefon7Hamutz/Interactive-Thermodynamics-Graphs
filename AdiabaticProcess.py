import numpy as np
import sympy as sp

from Process import Process


class AdiabaticProcess(Process):
    default_args = {'dof': 3}

    def __init__(self, parent, p0, v0, args):
        args = self.check_args(args)
        self.dof = args['dof']
        self.gamma = (self.dof+2)/self.dof
        super().__init__(parent, p0, v0, args)

    def check_args(self, args):
        if not isinstance(args, dict):
            args = {}
        if not 'dof' in args:
            args = AdiabaticProcess.default_args.copy()
        return args

    def get_points(self, v, p):
        self.c = p * v ** self.gamma
        V = np.linspace(self.vrange[0], self.vrange[1], 100)
        P = p * (v / V) ** self.gamma
        return V, P

    def get_equation(v, p, c, args):
        return sp.Eq(p * v ** ((args['dof']+2)/args['dof']), c)

    def evaluate(self, v):
        return self.c / v ** self.gamma

    def update_args(self, args):
        args = self.check_args(args)
        self.dof = args['dof']
        self.gamma = (self.dof + 2) / self.dof
