import matplotlib.pyplot as plt
import dynamics
from scipy import signal
import numpy as np


class PredatorPrey(dynamics.Dynamics):
    def __init__(self, preyBirth, preyDeath, predBirth, predDeath, time_step, pesWeight, endTime):
        numEquations = 3                            # set the number of state equations

        # set constants
        self.preyInc = preyBirth
        self.preyDec = preyDeath
        self.predInc = predBirth
        self.predDec = predDeath
        self.endTime = endTime

        self.pesWeight = pesWeight

        super().__init__(numEquations, time_step)   # initialize super class dynamics (Euler Method)

        # create variables to hold the state history for plotting
        self.Q = [[] for i in range(numEquations)]
        self.T = []

    def initialize(self, preyWeight, predWeight, pesWeight):
        # set state variable initial values
        self.q[0] = preyWeight
        self.q[1] = predWeight
        self.q[2] = pesWeight
        # initialize state history used for plotting
        self.Q = [[self.q[i]] for i in range(len(self.q))]
        self.T = [0.0]

    def advance(self, count):
        # compute "count" updates of the state equations
        for i in range(count):
            self.dq[0] = (self.preyInc * self.q[0]) - (self.preyDec * self.q[0] * self.q[1]) - (
                    self.q[2]/100000 * self.q[0])

            pes_potency = 1

            self.dq[1] = (self.predInc * self.q[0] * self.q[1]) - (self.predDec * self.q[1]) - (
                    self.q[2]/100 * pes_potency * self.q[1])

            #Pesticide equation
            decay = 4/self.endTime #Pesticide decay rate
            self.dq[2] = self.pesWeight * float((signal.sawtooth(2 * np.pi * decay * self.time, 0)+1)/2) - self.q[2]

            self.step()
        # save the updated state variables after the "count" updates for plotting
        [self.Q[i].append(self.q[i]) for i in range(len(self.q))]
        self.T.append(self.now())

    def print(self):
        # custom print for current simulation
        print('time={0:10f} prey={1:10f} predator={2:10f} pesticide={3:10f}'.format(self.time, self.q[0], self.q[1], self.q[2]))

    def plot(self):
        # custom plot for current simulation
        plt.figure()
        plt.subplot(411)
        plt.plot(self.T, self.Q[0], 'k')
        plt.ylabel('prey')

        plt.subplot(412)
        plt.plot(self.T, self.Q[1], 'r')
        plt.ylabel('predator')

        plt.subplot(413)
        plt.plot(self.T, self.Q[2], 'r')
        plt.ylabel('pesticide')

        plt.subplot(414)
        plt.plot(self.T, self.Q[0], 'k', self.T, self.Q[1], self.T, self.Q[2], 'r--')
        plt.ylabel('prey - predator - pesticide')
        plt.xlabel('time')

        plt.figure()
        plt.plot(self.Q[0], self.Q[1], 'b')
        plt.ylabel('prey')
        plt.xlabel('predator')

        plt.show()


# set parameters for predator-prey simulation

# parameters describing the simulation time
endTime = 500.0       # length of simulation (i.e. end time)
dt = 0.005             # time step size used to update state equations

# parameters describing the real system
preyBirth = 0.1 #Beta g
preyDeath = 0.001 #Delta g
predBirth = 0.0005 #Beta i
predDeath = 0.01 #Delta i
initPreyWt = 150.0 #G(0)
initPredWt = 50.0 #I(0)
#Pesticide parameters
initPesWt = 100.0

# create the simulation and initialize state variables
P = PredatorPrey(preyBirth, preyDeath, predBirth, predDeath, dt, initPesWt, endTime)
P.initialize(initPreyWt, initPredWt, initPesWt)

# run the simulation
displayInterval = 1         # number of state updates before saving state
while P.now() < endTime:
    P.advance(displayInterval)
    P.print()               # call print to see numeric values of state per display interval

P.plot()                    # call custom plot
