'''Caleb Austin and Daniel Chong'''
import random
import simpy
import numpy
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats

PICKUP_MAX = 2 #1 at the window, 1 behind
PAYMENT_MAX = 5 #1 at the window, 4 behind
ORDER_MAX = 8 #1 at the window, 7 behind
ORDER_DATA = []
PAYMENT_DATA = []
PICKUP_DATA = []
ARRIVAL_DATA = []


SAMPLED_ARRIVAL = []
data = ''

with open('arrival_data.txt') as f:
    data = f.read()
f.close()

data_set = data.split('\n\n')
for i in data_set:
    tmp = i.split('\n')
    for j in range(len(tmp)):
        if j != len(tmp) - 1:
            SAMPLED_ARRIVAL.append(round(float(tmp[j+1]),9)-round(float(tmp[j]),9))

SAMPLED_ORDER = []
data = ''

with open('order_data.txt') as f:
    data = f.read()
f.close()

data_set = data.split('\n\n')
for i in data_set:
    tmp = i.split('\n')
    for j in tmp:
        SAMPLED_ORDER.append(round(float(j),9))


SAMPLED_PAYMENT = []
data = ''

with open('payment_data.txt') as f:
    data = f.read()
f.close()

data_set = data.split('\n\n')
for i in data_set:
    tmp = i.split('\n')
    for j in tmp:
        SAMPLED_PAYMENT.append(round(float(j),9))

SAMPLED_PICKUP = []
data = ''

with open('pickup_data.txt') as f:
    data = f.read()
f.close()

data_set = data.split('\n\n')
for i in data_set:
    tmp = i.split('\n')
    for j in tmp:
        SAMPLED_PICKUP.append(round(float(j),9))


class Car:

    carNumber = 0

    def __init__(self, env, orderWindow, paymentWindow, pickupWindow):
        self.env = env
        self.orderWindow = orderWindow
        self.paymentWindow = paymentWindow
        self.pickupWindow = pickupWindow
        Car.carNumber += 1
        self.name = Car.carNumber
        tmp = float(stats.lognorm.rvs(0.705882537951898, scale=0.7169306089152209, size=1))
        self.orderTime = tmp
        ORDER_DATA.append(tmp)
        tmp = float(stats.lognorm.rvs(0.9354216450424766, scale=0.4946556213119036, size=1))
        self.paymentTime = tmp
        PAYMENT_DATA.append(tmp)
        tmp = float(stats.lognorm.rvs(1.039045798918802, scale=0.4808513685856047, size=1))
        self.pickupTime = tmp
        PICKUP_DATA.append(tmp)
        self.totalTime = 0


    def drive(self):

        if len(self.orderWindow.queue) < 8:
            self.arrivalTime = self.env.now
            #print('Arrival::', self)
            req = self.orderWindow.request()
            yield req
            #print('Start ordering::', self)
            evt = self.env.timeout(self.orderTime)
            yield evt
            #print("Finish ordering::", self)

            while len(self.paymentWindow.queue) == 5:
                yield self.paymentWindow.queue[0]

            self.orderWindow.release(req)
            #print('Waiting to pay::', self)
            req = self.paymentWindow.request()
            yield req
            #print('Start paying::', self)
            evt = self.env.timeout(self.paymentTime)
            yield evt
            #print('Finish paying::', self)

            while len(self.pickupWindow.queue) == 2:
                yield self.pickupWindow.queue[0]

            self.paymentWindow.release(req)
            #print('Waiting to pickup::', self)
            req = self.pickupWindow.request()
            yield req
            #print('Start pickup::', self)
            pickup = self.env.timeout(self.pickupTime)
            val = yield pickup
            #print("Finish pickup::", self)
            self.pickupWindow.release(req)
            self.totalTime = self.env.now - self.arrivalTime

        else:
            print('Left::', self, len(self.orderWindow.queue))


    def __str__(self):
        return f'Car: {self.name:d} time: {self.env.now:.3f}'

def arrivalGen(env, orderWindow, paymentWindow, pickupWindow):

    while True:

        c = Car(env, orderWindow, paymentWindow, pickupWindow)
        env.process(c.drive())
        tmp = float(stats.lognorm.rvs(1.0446698985442, scale=0.625674696640429, size=1))
        ARRIVAL_DATA.append(tmp)
        evt = env.timeout(tmp)
        yield evt

env = simpy.Environment()

orderWindow = simpy.Resource(env, 1)
paymentWindow = simpy.Resource(env, 1)
pickupWindow = simpy.Resource(env, 1)

env.process(arrivalGen(env, orderWindow, paymentWindow, pickupWindow))

env.run(until = 120.0)

print('Arrival')
print('Simulated', stats.describe(ARRIVAL_DATA))
print('Sampled', stats.describe(SAMPLED_ARRIVAL))
print('\nOrder')
print('Simulated', stats.describe(ORDER_DATA))
print('Sampled', stats.describe(SAMPLED_ORDER))
print('\nPayment')
print('Simulated', stats.describe(PAYMENT_DATA))
print('Sampled', stats.describe(SAMPLED_PAYMENT))
print('\nPickup')
print('Simulated', stats.describe(PICKUP_DATA))
print('Sampled', stats.describe(SAMPLED_PICKUP))
