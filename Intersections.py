import sympy as sp

from AdiabaticProcess import AdiabaticProcess
from IsothermalProcess import IsothermalProcess
from IsochoricProcess import IsochoricProcess
from IsobaricProcess import IsobaricProcess


class Intersector:
    def __init__(self):
        self.processes: list[type] = [AdiabaticProcess,
                                      IsothermalProcess, IsochoricProcess, IsobaricProcess]
        self.sols: dict[tuple[int, int], tuple[sp.Expr, sp.Expr]] = {}
        self.generate_sols()

    def add_process(self, process_type):
        if process_type in self.processes:
            return

        n = len(self.processes)
        self.processes.append(process_type)
        for i in range(n):
            self.sols[(i, n)] = self.get_analythic_sol(
                self.processes[i], process_type)

    def generate_sols(self):
        print("Generating analytical solutions for intersections...")
        n = len(self.processes)
        idxs = [(i, j) for i in range(n) for j in range(n) if i < j]
        for idx in idxs:
            if idx not in self.sols:
                self.sols[idx] = self.get_analythic_sol(
                    self.processes[idx[0]], self.processes[idx[1]])
        print("Done generating analytical solutions.")

    def get_analythic_sol(self, p1, p2) -> tuple[sp.Expr, sp.Expr]:
        args_vars = {}
        for p in (p1, p2):
            default_args = p.default_args
            for name in default_args.keys():
                args_vars[name] = sp.symbols(name, positive=True)

        v, p = sp.symbols('v p', positive=True)
        c1, c2 = sp.symbols('c1 c2', positive=True)

        eq1 = p1.get_equation(v, p, c1, args_vars)
        eq2 = p2.get_equation(v, p, c2, args_vars)
        sol = sp.solve([eq1, eq2], (v, p), rational=False)
        if type(sol) == list:
            sol = sol[0]
        elif type(sol) == dict:
            sol = (sol[v], sol[p])
        return sol

    def get_intersection(self, p1, p2, args):
        i = self.processes.index(type(p1))
        j = self.processes.index(type(p2))
        if i == j:
            raise ValueError("RAAAAAAAAAAAAAAAAAAAAA")
        if i > j:
            i, j = j, i
            p1, p2 = p2, p1
        funcs = self.sols[(i, j)]
        c1, c2 = sp.symbols('c1 c2', positive=True)
        args_vars = {c1: p1.c, c2: p2.c}
        for name, value in args.items():
            var = sp.symbols(name, positive=True)
            args_vars[var] = value
        return [float(f.evalf(subs=args_vars)) for f in funcs]
