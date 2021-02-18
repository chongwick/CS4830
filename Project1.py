import random
import simpy
import numpy
import matplotlib.pyplot as plt

PICKUP_MAX = 2 #1 at the window, 1 behind
PAYMENT_MAX = 5 #1 at the window, 4 behind
ORDER_MAX = 8 #1 at the window, 7 behind


SERVED = 0
LEFT = 0
SERVICETIME = 0
RUNS = 50

class Car:

    carNumber = 0

    def __init__(self, env, orderWindow, paymentWindow, pickupWindow):
        self.env = env
        self.orderWindow = orderWindow
        self.paymentWindow = paymentWindow
        self.pickupWindow = pickupWindow
        Car.carNumber += 1
        self.name = Car.carNumber
        self.orderTime = random.weibullvariate(3, 1.5)
        self.paymentTime = random.weibullvariate(2, 1.5)
        self.foodPrepTime = random.weibullvariate(6, 2.0)
        self.pickupTime = random.weibullvariate(2, 1.5)
        self.foodPrep = self.env.timeout(self.foodPrepTime)
        self.totalTime = 0


    def drive(self):
        global SERVED, LEFT, SERVICETIME

        if len(self.orderWindow.queue) < 8:
            self.arrivalTime = self.env.now
            print('Arrival::', self)
            req = self.orderWindow.request()
            yield req
            print('Start ordering::', self)
            evt = self.env.timeout(self.orderTime)
            yield evt
            print("Finish ordering::", self)
            self.foodPrep = self.env.timeout(self.foodPrepTime)

            while len(self.paymentWindow.queue) == 5:
                yield env.timeout(1)

            self.orderWindow.release(req)
            print('Waiting to pay::', self)
            req = self.paymentWindow.request()
            yield req
            print('Start paying::', self)
            evt = self.env.timeout(self.paymentTime)
            yield evt
            print('Finish paying::', self)

            while len(self.pickupWindow.queue) == 2:
                yield env.timeout(1)

            self.paymentWindow.release(req)
            print('Waiting to pickup::', self)
            req = self.pickupWindow.request()
            yield req
            print('Start pickup::', self)
            pickup = self.env.timeout(self.pickupTime)
            val = yield pickup & self.foodPrep
            print("Finish pickup::", self)
            if pickup in val:
                print('food was ready waited to pay')
            elif self.foodPrep in val:
                print("food wasn't ready had to wait")
            else:
                print('oops')
            self.pickupWindow.release(req)
            SERVED += 1
            self.totalTime = self.env.now - self.arrivalTime
            SERVICETIME += self.totalTime

        else:
            print('Left::', self, len(self.orderWindow.queue))
            LEFT += 1


    def __str__(self):
        return f'Car: {self.name:d} time: {self.env.now:.3f}'

def arrivalGen(env, orderWindow, paymentWindow, pickupWindow):

    while True:

        c = Car(env, orderWindow, paymentWindow, pickupWindow)
        env.process(c.drive())
        evt = env.timeout(random.expovariate(1.0/10.0))
        yield evt


for i in range(RUNS):
    env = simpy.Environment()

    orderWindow = simpy.Resource(env, 1)
    paymentWindow = simpy.Resource(env, 1)
    pickupWindow = simpy.Resource(env, 1)

    env.process(arrivalGen(env, orderWindow, paymentWindow, pickupWindow))

    env.run(until = 120.0)

print('\nSCENARIO 1')
print('Served:', SERVED/RUNS)
print('Left:', LEFT/RUNS)
print('Average service time:', SERVICETIME/SERVED)


#Start of second scenario
PICKUP_MAX = 2 #1 at the window, 1 behind
PAYMENT_MAX = 5 #1 at the window, 4 behind
ORDER_MAX = 8 #1 at the window, 7 behind


SERVED2 = 0
LEFT2 = 0
SERVICETIME2 = 0

class Car:

    carNumber = 0

    def __init__(self, env, orderWindow, orderWindow2, paymentWindow, pickupWindow):
        self.env = env
        self.orderWindow = orderWindow
        self.orderWindow2 = orderWindow2
        self.paymentWindow = paymentWindow
        self.pickupWindow = pickupWindow
        Car.carNumber += 1
        self.name = Car.carNumber
        self.orderTime = random.weibullvariate(3, 1.5)
        self.paymentTime = random.weibullvariate(2, 1.5)
        self.foodPrepTime = random.weibullvariate(6, 2.0)
        self.pickupTime = random.weibullvariate(2, 1.5)
        self.foodPrep = self.env.timeout(self.foodPrepTime)
        self.order = 0
        self.totalTime = 0


    def drive(self):
        global SERVED2, LEFT2, SERVICETIME2
        if len(self.orderWindow.queue) + len(self.orderWindow2.queue) < 8:
            if len(self.orderWindow.queue) <= len(self.orderWindow2.queue):
                self.order = 1
                self.arrivalTime = self.env.now
                print('Arrival::', self)
                req = self.orderWindow.request()
                yield req
                print('Start ordering::', self)
                evt = self.env.timeout(self.orderTime)
                yield evt
                print("Finish ordering::", self)
                self.foodPrep = self.env.timeout(self.foodPrepTime)
            else:
                self.order = 2
                self.arrivalTime = self.env.now
                print('Arrival::', self)
                req = self.orderWindow2.request()
                yield req
                print('Start ordering::', self)
                evt = self.env.timeout(self.orderTime)
                yield evt
                print("Finish ordering::", self)
                self.foodPrep = self.env.timeout(self.foodPrepTime)

            while len(self.paymentWindow.queue) == 5:
                yield env.timeout(1)
            if self.order == 1:
                self.orderWindow.release(req)
            else:
                self.orderWindow2.release(req)
            print('Waiting to pay::', self)
            req = self.paymentWindow.request()
            yield req
            print('Start paying::', self)
            evt = self.env.timeout(self.paymentTime)
            yield evt
            print('Finish paying::', self)

            while len(self.pickupWindow.queue) == 2:
                yield env.timeout(1)

            self.paymentWindow.release(req)
            print('Waiting to pickup::', self)
            req = self.pickupWindow.request()
            yield req
            print('Start pickup::', self)
            pickup = self.env.timeout(self.pickupTime)
            val = yield pickup & self.foodPrep
            print("Finish pickup::", self)
            if pickup in val:
                print('food was ready waited to pay')
            elif self.foodPrep in val:
                print("food wasn't ready had to wait")
            else:
                print('oops')
            self.pickupWindow.release(req)
            SERVED2 += 1
            self.totalTime = self.env.now - self.arrivalTime
            SERVICETIME2 += self.totalTime

        else:
            print('Left::', self, len(self.orderWindow.queue))
            LEFT2 += 1


    def __str__(self):
        return f'Car: {self.name:d} time: {self.env.now:.3f}'

def arrivalGen(env, orderWindow, orderWindow2, paymentWindow, pickupWindow):

    while True:

        c = Car(env, orderWindow, orderWindow2, paymentWindow, pickupWindow)
        env.process(c.drive())
        evt = env.timeout(random.expovariate(1.0/10.0))
        yield evt

for i in range(RUNS):
    env = simpy.Environment()

    orderWindow = simpy.Resource(env, 1)
    orderWindow2 = simpy.Resource(env, 1)
    paymentWindow = simpy.Resource(env, 1)
    pickupWindow = simpy.Resource(env, 1)

    env.process(arrivalGen(env, orderWindow, orderWindow2, paymentWindow, pickupWindow))

    env.run(until = 120.0)

print('\nSCENARIO 1:')
print('Served', SERVED/RUNS, 'Left:', LEFT/RUNS, 'Time:', SERVICETIME/SERVED)
print('\nSCENARIO 2:')
print('Served:', SERVED2/RUNS, 'Left:', LEFT2/RUNS, 'Time:', SERVICETIME2/SERVED2)
