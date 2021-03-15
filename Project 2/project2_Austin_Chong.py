'''Caleb Austin and Daniel Chong'''
import random
import simpy
import numpy
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

PICKUP_MAX = 2 #1 at the window, 1 behind
PAYMENT_MAX = 5 #1 at the window, 4 behind
ORDER_MAX = 8 #1 at the window, 7 behind


SERVED = 0
SERV_DATA = []
LEFT = 0
BALK_DATA = []
SERVICETIME = 0
TIME_DATA = []
RUNS = 20
BALK_TO_SERV = []
ARRIVALRATE = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]


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

def arrivalGen(env, orderWindow, paymentWindow, pickupWindow, arrivalRate):

    while True:

        c = Car(env, orderWindow, paymentWindow, pickupWindow)
        env.process(c.drive())
        evt = env.timeout(random.expovariate(arrivalRate/10.0))
        yield evt

for x in ARRIVALRATE:
    for i in range(RUNS):
        env = simpy.Environment()

        orderWindow = simpy.Resource(env, 1)
        paymentWindow = simpy.Resource(env, 1)
        pickupWindow = simpy.Resource(env, 1)

        env.process(arrivalGen(env, orderWindow, paymentWindow, pickupWindow, x))

        env.run(until = 120.0)
    BALK_TO_SERV.append(LEFT/SERVED)
    SERV_DATA.append(SERVED/RUNS)
    BALK_DATA.append(LEFT/RUNS)
    TIME_DATA.append(SERVICETIME/SERVED)
    SERVED = 0
    LEFT = 0
    SERVICETIME = 0




#Start of second scenario
PICKUP_MAX = 2 #1 at the window, 1 behind
PAYMENT_MAX = 5 #1 at the window, 4 behind
ORDER_MAX = 8 #1 at the window, 7 behind


SERVED2 = 0
SERV_DATA2 = []
LEFT2 = 0
BALK_DATA2 = []
SERVICETIME2 = 0
TIME_DATA2 = []
BALK_TO_SERV2 = []

class Car2:

    carNumber = 0

    def __init__(self, env, orderWindow, orderWindow2, paymentWindow, pickupWindow):
        self.env = env
        self.orderWindow = orderWindow
        self.orderWindow2 = orderWindow2
        self.paymentWindow = paymentWindow
        self.pickupWindow = pickupWindow
        Car2.carNumber += 1
        self.name = Car2.carNumber
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

def arrivalGen(env, orderWindow, orderWindow2, paymentWindow, pickupWindow, arrivalRate):

    while True:

        c = Car2(env, orderWindow, orderWindow2, paymentWindow, pickupWindow)
        env.process(c.drive())
        evt = env.timeout(random.expovariate(arrivalRate/10.0))
        yield evt

for x in ARRIVALRATE:
    for i in range(RUNS):
        env = simpy.Environment()

        orderWindow = simpy.Resource(env, 1)
        orderWindow2 = simpy.Resource(env, 1)
        paymentWindow = simpy.Resource(env, 1)
        pickupWindow = simpy.Resource(env, 1)

        env.process(arrivalGen(env, orderWindow, orderWindow2, paymentWindow, pickupWindow, x))

        env.run(until = 120.0)

    SERV_DATA2.append(SERVED2/RUNS)
    BALK_DATA2.append(LEFT2/RUNS)
    TIME_DATA2.append(SERVICETIME2/SERVED2)
    BALK_TO_SERV2.append(LEFT2/SERVED2)
    SERVED2 = 0
    LEFT2 = 0
    SERVICETIME2 = 0

#Create plot for Number of people served in comparison to differing arrival rates
plt.plot(ARRIVALRATE, SERV_DATA, label = "Scenario 1")
plt.plot(ARRIVALRATE, SERV_DATA2, label = "Scenario 2")
blue_line = mpatches.Patch(color='blue', label='Scenario 1')
orange_line = mpatches.Patch(color='orange', label='Scenario 2')
plt.legend(handles=[blue_line])
plt.legend(handles=[orange_line])
plt.title('People Served/Arrival rate')
plt.xlabel('Arrival Rate')
plt.ylabel('People Served')
plt.show()

plt.plot(ARRIVALRATE, BALK_DATA, label = "Scenario 1")
plt.plot(ARRIVALRATE, BALK_DATA2, label = "Scenario 2")
plt.title('Balks/Arrival rate')
plt.xlabel('Arrival Rate')
plt.ylabel('Balks')
plt.show()

plt.plot(ARRIVALRATE, TIME_DATA, label = "Scenario 1")
plt.plot(ARRIVALRATE, TIME_DATA2, label = "Scenario 2")
plt.title('Service Time/Arrival rate')
plt.xlabel('Arrival Rate')
plt.ylabel('Service Time')
plt.show()

plt.plot(ARRIVALRATE, BALK_TO_SERV, label = "Scenario 1")
plt.plot(ARRIVALRATE, BALK_TO_SERV2, label = "Scenario 2")
plt.title('(Balked/Served)/Arrival rate')
plt.xlabel('Served/Balked')
plt.ylabel('Service Time')
plt.show()


print(SERV_DATA2, BALK_DATA2, TIME_DATA2)
print(SERV_DATA, BALK_DATA, TIME_DATA)

#total = 0
#for i in SERV_DATA:
#    total += i
#print(total/20)
#total = 0
#for i in SERV_DATA2:
#    total += i
#print(total/20)
#
#total = 0
#for i in BALK_DATA:
#    total += i
#print(total/20)
#total = 0
#for i in BALK_DATA2:
#    total += i
#print(total/20)
