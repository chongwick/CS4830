import random
import simpy

PICKUP_MAX = 2 #1 at the window, 1 behind
PAYMENT_MAX = 5 #1 at the window, 4 behind
ORDER_MAX = 8 #1 at the window, 7 behind

PICKUP_QUEUE = []
PAYMENT_QUEUE = []
ORDER_QUEUE = []

SERVED = 0

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
        self.orderTime = random.expovariate(1.0/9.0)
        self.paymentTime = random.expovariate(1.0/5.0)
        self.foodPrepTime = random.expovariate(1.0/5.0)
        self.pickupTime = random.expovariate(1.0/3.0)
        self.foodPrep = self.env.timeout(self.foodPrepTime)
        self.order = 0


    def drive(self):
        global SERVED
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
            SERVED += 1

        else:
            print('Left::', self, len(self.orderWindow.queue))


    def __str__(self):
        return f'Car: {self.name:d} time: {self.env.now:.3f}'

def arrivalGen(env, orderWindow, orderWindow2, paymentWindow, pickupWindow):

    while True:

        c = Car(env, orderWindow, orderWindow2, paymentWindow, pickupWindow)
        env.process(c.drive())
        evt = env.timeout(random.expovariate(1.0/10.0))
        yield evt


env = simpy.Environment()

orderWindow = simpy.Resource(env, 1)
orderWindow2 = simpy.Resource(env, 1)
paymentWindow = simpy.Resource(env, 1)
pickupWindow = simpy.Resource(env, 1)

env.process(arrivalGen(env, orderWindow, orderWindow2, paymentWindow, pickupWindow))

env.run(until = 300.0)

print('Customers served:', SERVED)
