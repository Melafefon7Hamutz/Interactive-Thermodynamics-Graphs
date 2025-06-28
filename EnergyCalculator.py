import sympy as sp

from AdiabaticProcess import AdiabaticProcess
from IsothermalProcess import IsothermalProcess
from IsochoricProcess import IsochoricProcess
from IsobaricProcess import IsobaricProcess


class EnergyCalculator:

    def __init__(self):
        self.processes: list[type] = [AdiabaticProcess,
                                      IsothermalProcess, IsochoricProcess, IsobaricProcess]
        self.work_exprs: dict[int, sp.Expr] = {}
        self.generate_work_exprs()

    def generate_work_exprs(self):
        print("Generating work expressions for processes...")
        for i, process_type in enumerate(self.processes):
            if i not in self.work_exprs:
                self.work_exprs[i] = self.generate_work_integral(process_type)
        print("Done generating work expressions.")

    def generate_work_integral(self, process_type):
        if process_type == IsochoricProcess:
            return sp.Float(0)
        v, p, c = sp.symbols('v p c', positive=True)
        args_vars = {name: sp.symbols(name, positive=True)
                     for name in process_type.default_args.keys()}
        eq = process_type.get_equation(v, p, c, args_vars)
        p_expr = sp.solve(eq, p)[0]
        return sp.integrate(p_expr, v)

    def calculate_work(self, process, args):
        v_start, v_end = [p.x for p in process.get_edges()]
        i = self.processes.index(type(process))
        
        v, c = sp.symbols('v c', positive=True)
        args_vars = {c: process.c}
        for name, value in args.items():
            var = sp.symbols(name, positive=True)
            args_vars[var] = value

        return float(self.work_exprs[i].evalf(subs={**args_vars, v:v_end}) - 
                     self.work_exprs[i].evalf(subs={**args_vars, v:v_start}))
    
    def calculate_work_heat(self, process, args):
        W = self.calculate_work(process, args)
        (v1, p1), (v2, p2) = [(p.x, p.y) for p in process.get_edges()]
        U = (p2 * v2 - p1 * v1) * args['dof'] / 2
        return W, W + U
    