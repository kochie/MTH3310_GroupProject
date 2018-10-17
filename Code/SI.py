#!/bin/env python3

from modelling.stochastic.gillespie import Model as GillespieModel
from modelling.ode import Solver as ODESolver
import numpy as np

if __name__ == "__main__":
    alpha = 1.1
    beta = 0.5
    N = 351

    model = GillespieModel(T=100, V=N)
    model.addState("Susceptible", 350)
    model.addState("Infected", 1)
    model.addState("Recovered", 0)


    def infected(state, dt, w, W):
        # print(dt, w, dt*w)
        p = np.random.poisson(W*dt)
        state["Susceptible"] = state["Susceptible"] - p
        state["Infected"] = state["Infected"] + p
        # print(state["Susceptible"], state["Infected"], dt*w)
        return state
    def healed(state, dt, w, W):
        p = np.random.poisson(W*dt)
        state["Recovered"] = state["Recovered"] + p
        state["Infected"] = state["Infected"] - p
        return state

    def w1(state, model):
        return alpha*state["Susceptible"]*state["Infected"]/model.V
    def w2(state, model):
        return beta*state["Infected"]

    model.addTransition(infected, w1)
    model.addTransition(healed, w2)

    model.run()
    model.plot()

    f1 = lambda t, S, I, R: -alpha*S*I/N
    f2 = lambda t, S, I, R: alpha*S*I/N-beta*I
    f3 = lambda t, S, I, R: beta*I
    ode = ODESolver([f1,f2,f3], initial=np.array([0,350,1,0]))
    ode.run('rk45', 0, 100, 0.01)
    ode.plot(label=["Susceptible", "Infected", "Recovered"])
    ode.show()
