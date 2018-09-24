#!/bin/env python3

import numpy as np
import math
import matplotlib.pyplot as plt

class Model:
  def __init__(self, T=500):
    self.T = T # maximum elapsed time
    self.stateNames = list()
    self.stateInitialValues = np.empty([0], dtype=np.float)
    self.stateUpdateFunctions = list()
    self.stateW = list()
    self.stateValues = np.empty([0], dtype=np.float)
    self.timeStamp = np.empty([1,0], dtype=np.float)
    self.V = 100

  
  def addState(self, state):
    self.stateNames.append(state[0])
    self.stateInitialValues = np.insert(self.stateInitialValues, 0, state[1])
    self.stateUpdateFunctions.append(state[2])
    self.stateW.append(state[3])


  def run(self):
    self.stateInitialValues = np.flip(self.stateInitialValues, axis=0) 
    print(self.stateInitialValues, self.stateNames)
    self.stateHistoricalValues = np.empty([0,len(self.stateInitialValues)], dtype=np.float)
    self.stateValues = np.array(self.stateInitialValues)
    self.timeStamp = np.empty([1,0], dtype=np.float)
    t = 0

    while t < self.T:
      state = dict(zip(self.stateNames, self.stateValues))
      w_array = [w(state, self) for w in self.stateW]
      W = sum(w_array)
      
      if W == 0:
        return
      
      dt = -np.log(np.random.random_sample()) / W
      t = t + dt
      self.timeStamp = np.insert(self.timeStamp, 0, t)

      event = np.random.random_sample()
      sum_a = 0
      idx = 0

      for w in w_array:
        if  sum_a / W <= event < (sum_a + w) / W:
            self.stateHistoricalValues = np.vstack((self.stateHistoricalValues, self.stateValues))
            newStates = self.stateUpdateFunctions[idx](state)
            self.stateValues = [newStates[state] for state in self.stateNames]
            break
        else:
            idx += 1
            sum_a += w
  
  def plot(self):
    # print(self.stateHistoricalValues)
    for i in range(0, len(self.stateNames)):
      # print(self.timeStamp.reshape(1,len(self.timeStamp)), self.stateHistoricalValues.T[i:i+1])
      plt.plot(self.timeStamp.reshape(1,len(self.timeStamp)).T, np.flip(self.stateHistoricalValues[:,i:i+1], axis=0))
    plt.title("Populations vs Time")
    plt.legend(self.stateNames)
    plt.xlabel("Time")
    plt.ylabel("Population")
    plt.show()


if __name__ == '__main__':
  model = Model()

  def susceptible(state):
    # state["Susceptible"] = state["Susceptible"] + 1
    # state["Infected"] = state["Infected"] - 1
    return state

  def w1(state, model):
    return 0.3 * state["Infected"] / model.V

  model.addState(("Susceptible", 500, susceptible, w1))


  def infected(state):
    state["Susceptible"] = state["Susceptible"] - 1
    state["Infected"] = state["Infected"] + 1
    return state

  def w2(state, model):
    return 0.01 * state["Susceptible"] * state["Infected"] / model.V

  model.addState(("Infected", 1, infected, w2))

  def recovered(state):
    state["Recovered"] = state["Recovered"] + 1
    state["Infected"] = state["Infected"] - 1
    return state

  def w3(state, model):
    return 0.07 * state["Infected"] / model.V

  model.addState(("Recovered", 0, recovered, w3))

  model.run()
  model.plot()