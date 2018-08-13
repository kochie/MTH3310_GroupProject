#!/bin/env python3

import random

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def main():
    # Initializing the simulation size
    number_of_steps = 10000
    circle_population = np.zeros(number_of_steps)
    triangle_population = np.zeros(number_of_steps)

    # Defining the inital population
    circle_population[0] = 100
    triangle_population[0] = 100
    
    triangle_chance = 0.5
    circle_chance = 0.3

    circle_production = 5
    triangle_production = 5
    enzyme_population = 8
    decay_rate = 0.01

    for i in range(1, number_of_steps):
        triangle_population[i] = max(
            0, triangle_population[i-1]*(1-decay_rate) + triangle_production
        )
        circle_population[i] = max(0, circle_population[i-1]*(1-decay_rate) + circle_production)
        for _ in range(0, enzyme_population):
            chance = random.random()

            if 0 <= chance < circle_chance and circle_population[i] >= 1:
                circle_population[i] = circle_population[i] - 1
            elif circle_chance <= chance < triangle_chance+circle_chance and triangle_population[i] >= 1:
                triangle_population[i] = triangle_population[i] - 1
            else:
                pass

    plt.plot(np.arange(0, number_of_steps), circle_population)
    plt.plot(np.arange(0, number_of_steps), triangle_population)
    plt.show()

if __name__ == "__main__":
    main()
