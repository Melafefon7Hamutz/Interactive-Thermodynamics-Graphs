from IsothermalProcess import IsothermalProcess
from AdiabaticProcess import AdiabaticProcess
import sympy as sp


class Intersector:
    def __init__(self):
        self.processes = []

    def add_process(self, process):
        i = type(process), process.args
        if not i in self.processes:
            self.processes.append((i))
            self.generate_sols()

    def generate_sols(self):
        n = len(self.processes)
        idxs = [(i, j) for i in range(n) for j in range(n) if i < j]
        self.sols = {}
        for idx in idxs:
            self.sols[idx] = self.get_analythic_sol(
                *self.processes[idx[0]], *self.processes[idx[1]])

    def get_analythic_sol(self, p1, k1, p2, k2):
        v, p = sp.symbols('v p', positive=True)
        c1, c2 = sp.symbols('c1 c2', positive=True)
        eq1 = sp.Eq(p1.get_equation(v, p, c1, **k1), 0)
        eq2 = sp.Eq(p2.get_equation(v, p, c2, **k2), 0)
        sol = sp.solve([eq1, eq2], (v, p))[0]
        return [sp.lambdify((c1, c2), s, 'numpy') for s in sol]

    def get_intersection(self, p1, p2):
        i = self.processes.index((type(p1), p1.args))
        j = self.processes.index((type(p2), p2.args))
        if i == j:
            raise ValueError("RAAAAAAAAAAAAAAAAAAAAA")
        if i > j:
            i, j = j, i
            p1, p2 = p2, p1
        funcs = self.sols[(i, j)]
        return funcs[0](p1.c, p2.c), funcs[1](p1.c, p2.c)

