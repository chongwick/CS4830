# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 00:59:43 2021

@author: mrizki
"""

# generate exponential distributed data
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

sampleScale = 3.0  # mean
sampleSize = 100

sampleData = stats.expon.rvs(scale=sampleScale, size=sampleSize)
sampleData = []
data = ''

with open('arrival_data.txt') as f:
    data = f.read()
f.close()

data_set = data.split('\n\n')
for i in data_set:
    tmp = i.split('\n')
    for j in range(len(tmp)):
        if j != len(tmp) - 1:
            sampleData.append(round(float(tmp[j+1]),9)-round(float(tmp[j]),9))
sampleSize = len(sampleData)
sortedData = np.sort(sampleData)

count = np.ones(sampleSize)
count = np.cumsum(count) / sampleSize
binEdges = np.linspace(0.0, np.max(sampleData), 3)
fit_alpha, fit_loc, fit_beta = stats.gamma.fit(sampleData, floc=0)
cdf = stats.gamma.cdf(binEdges, fit_alpha, scale=fit_beta, loc=fit_loc)

KS_stat, p_value = stats.ks_2samp(count, cdf)
print('KS statistic', KS_stat)
print('p value', p_value)
print('H0: (null hypothesis) Sample data comes from same distrbution as theortectical distrbution.')
print('H1: (alternative hypothesis) Sample data does not comes from same distrbution as theortectical distrbution.')
if p_value >= 0.05:
    print('we can not reject the null hypothesis')
else:
    print('we reject the null hypothesis')

plt.hist(sampleData, density = True, bins = 20); plt.show()
