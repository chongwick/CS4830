import random
import simpy

PICKUP_MAX = 2 #1 at the window, 1 behind
PAYMENT_MAX = 5 #1 at the window, 4 behind
ORDER_MAX = 8 #1 at the window, 7 behind

PICKUP_QUEUE = []
PAYMENT_QUEUE = []
ORDER_QUEUE = []

ORDER_NUM = 0
SERVED = 0

class Car:

    carNumber = 0

    def __init__(self, env, queue):
        self.env = env
        self.queue = queue
        Car.carNumber += 1
        self.name = Car.carNumber
        self.orderTime = random.expovariate(1.0/12.0)
        self.paymentTime = random.expovariate(1.0/12.0)
        self.foodPrepTime = random.expovariate(1.0/5.0)
        self.pickupTime = random.expovariate(1.0/3.0)
        self.foodPrep = self.env.timeout(self.foodPrepTime)


    def drive(self):
        global SERVED, ORDER_NUM
        if ORDER_NUM < ORDER_MAX:
            ORDER_NUM += 1
            for i in range(len(self.queue)):
                if i == ORDER_MAX-1:  #At order window
                    self.arrivalTime = self.env.now
                    print('Arrival::', self)
                    req = self.queue[i].request()
                    yield req
                    print('Start ordering::', self)
                    evt = self.env.timeout(self.orderTime)
                    yield evt
                    print("Finish ordering::", self)
                    self.foodPrep = self.env.timeout(self.foodPrepTime)
                    self.queue[i].release(req)
                    ORDER_NUM -= 1
                elif i == ORDER_MAX + PAYMENT_MAX-1:   #At payment window
                    print('Waiting to pay::', self)
                    req = self.queue[i].request()
                    yield req
                    print('Start paying::', self)
                    evt = self.env.timeout(self.paymentTime)
                    yield evt
                    print('Finish paying::', self)
                    self.queue[i].release(req)
                elif i == ORDER_MAX + PAYMENT_MAX + PICKUP_MAX-1:   #At pickup window
                    print('Waiting to pickup::', self)
                    req = self.queue[i].request()
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
                    self.queue[i].release(req)
                    SERVED += 1
                else:
                    req = self.queue[i].request()
                    yield req
                    self.queue[i].release(req)

        else:
            print('Left::', self, 'Order queue length::', ORDER_NUM)


    def __str__(self):
        return f'Car: {self.name:d} time: {self.env.now:.3f}'

def arrivalGen(env, queue):

    while True:

        c = Car(env, queue)
        env.process(c.drive())
        evt = env.timeout(random.expovariate(1.0/10.0))
        yield evt


env = simpy.Environment()
queue = []
for i in range(15):
    queue.append(simpy.Resource(env, 1))

env.process(arrivalGen(env, queue))

env.run(until = 300.0)

print('Customers served:', SERVED)
