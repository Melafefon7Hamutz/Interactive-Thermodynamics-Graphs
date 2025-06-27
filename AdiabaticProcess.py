import numpy as np

from Process import Process

class AdiabaticProcess(Process):
    def __init__(self, parent, p0, v0, args={'gamma':5/3}):
        if not 'gamma' in args:
            args={'gamma':5/3}
        gamma = args['gamma']
        self.gamma = gamma
        super().__init__(parent, p0, v0, args)

    def get_points(self, v, p):
        self.c = p * v ** self.gamma
        V = np.linspace(self.vrange[0], self.vrange[1], 100)
        P = p * (v / V) ** self.gamma
        return V, P

    def get_equation(v, p, c, **kargs):
        return p * v ** kargs['gamma'] - c
    
    def evaluate(self, v):
        return self.c / v ** self.gamma
    
    def is_args_equivalent(self, args2):
        if 'gamma' in args2:
            return args2['gamma'] == self.gamma
        else:
            return self.gamma == 5/3