#!/bin/env python3

from modelling.stochastic.gillespie import Model
from modelling.ode import Solver
import math
import numpy as np

if __name__ == '__main__':
  model = Model(T=50, V=1)

  lambda_1 = 10
  lambda_3 = 5
  lambda_2 = 10
  gamma = 0.1
  nabla_plus = 0.9
  nabla_minus = 0.9
  mu = 0.2
  omega = 2*math.pi/10

  model.addState("Triangle", 100)
  model.addState("Circle", 100)
  model.addState("Enzyme", 50)
  model.addState("Enzyme + Triangle", 0)
  model.addState("Enzyme + Circle", 0)

  def new_triangle(state, dt, w, W):
    p = np.random.poisson(w*dt)
    state["Triangle"] = state["Triangle"] + 1
    return state
  def w1(state, model):
    return lambda_1+lambda_3*math.sin(omega*model.t)

  def new_circle(state, dt, w, W):
    p = np.random.poisson(w*dt)
    state["Circle"] = state["Circle"] + 1
    return state
  def w2(state, model):
    return lambda_2

  def decay_triangle(state, dt, w, W):
    p = np.random.poisson(w*dt)
    state["Triangle"] = state["Triangle"] - 1
    return state
  def w3(state, model):
    return gamma*state["Triangle"]

  def decay_circle(state, dt, w, W):
    p = np.random.poisson(w*dt)
    state["Circle"] = state["Circle"] - 1
    return state
  def w4(state, model):
    return gamma*state["Circle"]

  def enzyme_circle_binding(state, dt, w, W):
    p = np.random.poisson(w*dt)
    state["Enzyme"] = state["Enzyme"] - 1
    state["Circle"] = state["Circle"] - 1
    state["Enzyme + Circle"] = state["Enzyme + Circle"] + 1
    return state
  def w5(state, model):
    return nabla_plus*state["Enzyme"]*state["Circle"]/model.V

  def enzyme_triangle_binding(state, dt, w, W):
    p = np.random.poisson(w*dt)
    state["Enzyme"] = state["Enzyme"] - 1
    state["Triangle"] = state["Triangle"] - 1
    state["Enzyme + Triangle"] = state["Enzyme + Triangle"] + 1
    return state
  def w6(state, model):
    return nabla_plus*state["Enzyme"]*state["Triangle"]/model.V

  def enzyme_circle_unbinding(state, dt, w, W):
    p = np.random.poisson(w*dt)
    state["Enzyme"] = state["Enzyme"] + 1
    state["Circle"] = state["Circle"] + 1
    state["Enzyme + Circle"] = state["Enzyme + Circle"] - 1
    return state
  def w7(state, model):
    return nabla_minus*state["Enzyme + Circle"]

  def enzyme_triangle_unbinding(state, dt, w, W):
    p = np.random.poisson(w*dt)
    state["Enzyme"] = state["Enzyme"] + 1
    state["Triangle"] = state["Triangle"] + 1
    state["Enzyme + Triangle"] = state["Enzyme + Triangle"] - 1
    return state
  def w8(state, model):
    return nabla_minus*state["Enzyme + Triangle"]

  def enzyme_circle_decay(state, dt, w, W):
    p = np.random.poisson(w*dt)
    state["Enzyme"] = state["Enzyme"] + 1
    state["Enzyme + Circle"] = state["Enzyme + Circle"] - 1
    return state
  def w9(state, model):
    return mu*state["Enzyme + Circle"]

  def enzyme_triangle_decay(state, dt, w, W):
    p = np.random.poisson(w*dt)
    state["Enzyme"] = state["Enzyme"] + 1
    state["Enzyme + Triangle"] = state["Enzyme + Triangle"] - 1
    return state
  def w10(state, model):
    return mu*state["Enzyme + Triangle"]


  model.addTransition(new_triangle, w1)
  model.addTransition(new_circle, w2)
  model.addTransition(decay_triangle, w3)
  model.addTransition(decay_circle, w4)
  model.addTransition(enzyme_circle_binding, w5)
  model.addTransition(enzyme_triangle_binding, w6)
  model.addTransition(enzyme_circle_unbinding, w7)
  model.addTransition(enzyme_triangle_unbinding, w8)
  model.addTransition(enzyme_circle_decay, w9)
  model.addTransition(enzyme_triangle_decay, w10)

  model.run()
  model.plot()

  X1 = lambda t, x1, x2, e, c1, c2: lambda_1+lambda_3*math.sin(omega*t)-gamma*x1-nabla_plus*x1*e+nabla_minus*c1
  X2 = lambda t, x1, x2, e, c1, c2: lambda_2-gamma*x2-nabla_plus*x2*e+nabla_minus*c2
  E = lambda t, x1, x2, e, c1, c2: -nabla_plus*e*(x1+x2)+(nabla_minus+gamma+mu)*(c1+c2)
  C1 = lambda t, x1, x2, e, c1, c2: nabla_plus*e*(x1)-(nabla_minus+gamma+mu)*(c1)
  C2 = lambda t, x1, x2, e, c1, c2: nabla_plus*e*(x2)-(nabla_minus+gamma+mu)*(c2)

  solver = Solver([X1,X2,E,C1,C2], initial=np.array([0,100,100,50,0,0]))

  solver.run('rk45',0,50,0.01)
  solver.plot(label=["X1","X2","Enzyme","X1+E","X2+E"])

  solver.show()