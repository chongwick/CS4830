# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 12:20:12 2021

@author: mrizki
"""

import simpy

def example(env):
     event = simpy.events.Timeout(env, delay=5)
     yield event
     print('now=%d' % (env.now))
     
     event = simpy.events.Timeout(env, delay=1)
     yield event
     print('now=%d' % (env.now))


env = simpy.Environment()

example_gen = example(env)

p = simpy.events.Process(env, example_gen)

env.run()

