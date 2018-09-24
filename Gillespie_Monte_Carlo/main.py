#!/bin/env python3

import numpy as np
import math
import matplotlib.pyplot as plt

class Model:
  def __init__(self, T=500):
    self.T = T # maximum elapsed time
    self.stateNames = list()
    self.stateInitialValues = np.empty([0], dtype=np.float)
    self.stateTransitionFunctions = list()
    self.stateW = list()
    # self.stateValues = np.empty([0], dtype=np.float)
    self.timeStamp = np.empty([1,0], dtype=np.float)
    self.V = 100
    self.transitions = list()

  def addTransition(self, transitionFunction, weightFunction):
    self.stateTransitionFunctions.append(transitionFunction)
    self.stateW.append(weightFunction)

  def addState(self, name, initialValue=0):
    self.stateNames.append(name)
    self.stateInitialValues = np.insert(self.stateInitialValues, 0, initialValue)

  def run(self):
    stateInitialValues = np.flip(self.stateInitialValues, axis=0) 
    self.stateHistoricalValues = np.empty([0,len(stateInitialValues)], dtype=np.float)
    stateValues = np.array(stateInitialValues)
    self.timeStamp = np.empty([1,0], dtype=np.float)
    t = 0

    while t < self.T:
      state = dict(zip(self.stateNames, stateValues))
      w_array = [w(state, self) for w in self.stateW]
      W = sum(w_array)
      
      if W == 0:
        return
      
      dt = -np.log(np.random.random_sample()) / W
      self.timeStamp = np.insert(self.timeStamp, 0, t)
      t = t + dt

      event = np.random.random_sample()
      sum_a = 0
      idx = 0

      for w in w_array:
        if  sum_a / W <= event < (sum_a + w) / W:
            self.stateHistoricalValues = np.vstack((self.stateHistoricalValues, stateValues))
            newStates = self.stateTransitionFunctions[idx](state)
            stateValues = [newStates[state] for state in self.stateNames]
            break
        else:
            idx += 1
            sum_a += w
  
  def plot(self):
    for i in range(0, len(self.stateNames)):
      plt.plot(self.timeStamp.reshape(1,len(self.timeStamp)).T, np.flip(self.stateHistoricalValues[:,i:i+1], axis=0))
    plt.title("Populations vs Time")
    plt.legend(self.stateNames)
    plt.xlabel("Time")
    plt.ylabel("Population")
    plt.show()


if __name__ == '__main__':
  model = Model()

  model.addState("Triangle", 40)
  model.addState("Circle", 40)
  model.addState("Enzyme", 10)
  model.addState("Enzyme + Triangle")
  model.addState("Enzyme + Circle")

  def new_triangle(state):
    state["Triangle"] = state["Triangle"] + 1
    return state
  def w1(state, model):
    return 0.1

  def new_circle(state):
    state["Circle"] = state["Circle"] + 1
    return state
  def w2(state, model):
    return 0.1

  def decay_triangle(state):
    state["Triangle"] = state["Triangle"] - 1
    return state
  def w3(state, model):
    return 0.9*state["Triangle"]/model.V

  def decay_circle(state):
    state["Circle"] = state["Circle"] - 1
    return state
  def w4(state, model):
    return 0.1*state["Circle"]/model.V

  def enzyme_circle(state):
    state["Enzyme"] = state["Enzyme"] - 1
    state["Enzyme + Circle"] = state["Enzyme + Circle"] + 1
    return state
  def w5(state, model):
    return 0.2*state["Enzyme"]*state["Circle"]/model.V

  def enzyme_triangle(state):
    state["Enzyme"] = state["Enzyme"] - 1
    state["Enzyme + Triangle"] = state["Enzyme + Triangle"] + 1
    return state
  def w6(state, model):
    return 0.2*state["Enzyme"]*state["Triangle"]/model.V

  
  def enzyme_circle_decay(state):
    state["Enzyme"] = state["Enzyme"] + 1
    state["Enzyme + Circle"] = state["Enzyme + Circle"] - 1
    return state
  def w7(state, model):
    return state["Enzyme + Circle"]/model.V

  def enzyme_triangle_decay(state):
    state["Enzyme"] = state["Enzyme"] + 1
    state["Enzyme + Triangle"] = state["Enzyme + Triangle"] - 1
    return state
  def w8(state, model):
    return state["Enzyme + Triangle"]/model.V
  

  model.addTransition(new_triangle, w1)
  model.addTransition(new_circle, w2)
  model.addTransition(decay_triangle, w3)
  model.addTransition(decay_circle, w4)
  model.addTransition(enzyme_circle, w5)  
  model.addTransition(enzyme_triangle, w6)
  model.addTransition(enzyme_circle_decay, w7)  
  model.addTransition(enzyme_triangle_decay, w8)

  # def susceptible(state):
  #   # state["Susceptible"] = state["Susceptible"] + 1
  #   # state["Infected"] = state["Infected"] - 1
  #   return state

  # def w1(state, model):
  #   return 0.3 * state["Infected"] / model.V

  # model.addState(("Susceptible", 500, susceptible, w1))


  # def infected(state):
  #   state["Susceptible"] = state["Susceptible"] - 1
  #   state["Infected"] = state["Infected"] + 1
  #   return state

  # def w2(state, model):
  #   return 0.01 * state["Susceptible"] * state["Infected"] / model.V

  # model.addState(("Infected", 1, infected, w2))

  # def recovered(state):
  #   state["Recovered"] = state["Recovered"] + 1
  #   state["Infected"] = state["Infected"] - 1
  #   return state

  # def w3(state, model):
  #   return 0.17 * state["Infected"] / model.V

  # model.addState(("Recovered", 0, recovered, w3))

  model.run()
  model.plot()