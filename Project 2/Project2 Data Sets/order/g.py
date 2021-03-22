from matplotlib import pyplot as plt
import numpy as np
import scipy.stats
import random

data = ''
time = []
with open('order_data.txt') as f:
    data = f.read()
f.close()

#Converting recorded times into difference between times
data_set = data.split('\n\n')
for i in data_set:
    for i in data_set:
        tmp = i.split('\n')
        for j in tmp:
            time.append(round(float(j),9))
shape, loc, scale = scipy.stats.weibull_min.fit(time, floc = 0)
print(shape, loc, scale)

x = np.linspace(0, max(time), 100)
fitted_data = scipy.stats.weibull_min(shape, loc, scale).pdf(x)
plt.plot(x, fitted_data)
plt.hist(time, density = True, bins = 10); plt.show()

dist_data = []
for i in range(len(time)):
    dist_data.append(random.weibullvariate(scale, shape))
print(scipy.stats.chisquare(dist_data, time))
