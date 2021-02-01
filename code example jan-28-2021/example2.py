# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 13:14:30 2021

@author: mrizki
"""


import simpy

class Car:
    def __init__(self, env):
        self.env = env
        self.env.process(self.printCar())
        
    def printCar(self):
        print('Car starts', self.env.now)
        event = simpy.events.Timeout(env, delay=5)
        yield event
        print('Car ends', self.env.now)
        
        
def carGen(env, numCars):
    for c in range(numCars):
        aCar = Car(env)
        yield simpy.events.Timeout(env, 1.0)


env = simpy.Environment()

example_gen = carGen(env, 5)

p = simpy.events.Process(env, example_gen)

env.run()