import simpy
import random

#Queue to represent each space in the drive-thru
CAR_QUEUE = []

def source(env, number, interval, order_station):
    for i in range(number):
        c = car(env, 'Car%02d' % i, order_station, 12)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)

#add pickup and pay to arguments later
def car(env, name, order_station, time):
    print('%s starting at %d' % (name, env.now))
    r1 = order_station.request()
    yield r1
    orderTime = random.expovariate(1.0 / 1.0)
    yield env.timeout(orderTime)
    order_station.release(r1)

env = simpy.Environment()

order_station = simpy.Resource(env, capacity=1)
#pay_station = simpy.Resource(env, capacity=1)
#pickup_station = simpy.Resource(env, capacity=1)

env.process(source(env, 12, 2.0, order_station))
env.run()
