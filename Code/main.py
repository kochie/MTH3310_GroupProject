#!/bin/env python3

import math
import matplotlib.pyplot as plt
import numpy as np
from modelling.ode import Solver


if __name__ == "__main__":
    lambda_1 = 3
    lambda_2 = 10
    gamma = 1.2
    nabla_plus = 1
    nabla_minus = 1
    c_1 = 1
    c_2 = 1
    mu = 0.5

    f1 = lambda t, x1, x2, e, c: lambda_1-gamma*x1-nabla_plus*x1*e+nabla_minus*c_1
    f2 = lambda t, x1, x2, e, c: lambda_2-gamma*x2-nabla_plus*x2*e+nabla_minus*c_2
    f3 = lambda t, x1, x2, e, c: -nabla_plus*e*(x1+x2)+(nabla_minus+gamma+mu)*(c_1+c_2)
    f4 = lambda t, x1, x2, e, c: nabla_plus*e*(x1+x2)-(nabla_minus+gamma+mu)*(c_1+c_2)

    solver = Solver([f1,f2,f3,f4], initial=np.array([0,1,2,1,1]))

    solver.run('rk45',0,50,0.01)
    solver.plot(label=["X1","X2","Enzyme","Combined"])

    solver.show()
