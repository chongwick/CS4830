from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
import random

data = ''
sampleData = []
numBins = 20
with open('arrival_data.txt') as f:
    data = f.read()
f.close()

#Converting recorded times into difference between times
data_set = data.split('\n\n')
for i in data_set:
    tmp = i.split('\n')
    for j in range(len(tmp)):
        if j != len(tmp)-1:
            sampleData.append(round(float(tmp[j+1]), 9)-round(float(tmp[j]), 9))

sampleData = stats.expon.rvs(3.0, 1000)
observed, bins = np.histogram(sampleData, bins=numBins)
fit_loc, fit_beta = stats.expon.fit(sampleData)
binMidPt = (bins[1:] + bins[:-1]) / 2
expectedProb = stats.expon.cdf(bins, scale=fit_beta)
expected = 1000 * np.diff(expectedProb) / (np.sum(np.diff(expectedProb)))

plt.hist(sampleData, bins=numBins, label='Observed')
plt.plot(binMidPt, expected, 'or-', label='Expected')
plt.plot(binMidPt, observed, 'oy-', label='Observed')
plt.legend()

chiSq, pValue = stats.chisquare(f_obs=observed, f_exp=expected, ddof=2)
print(f'ChiSquare Statistic {chiSq:0.3f} P value {pValue:0.3f}')

print('H0: (null hypothesis) Sample data follows the hypothesized distribution.')
print('H1: (alternative hypothesis) Sample data does not follow a hypothesized distribution.')

if pValue >= 0.05:
    print('we can not reject the null hypothesis')
else:
    print('we reject the null hypothesis')

#sampleDta = stats.expon.rvs(3.0, 1000)
#sampleSize, min_max, sampleMean, sampleVariance, skew, kurtosis= stats.describe(sampleDta)
#print(f'mean {sampleMean:0.3f}  variance: {sampleVariance:0.3f} range: ({min_max[0]:f}, {min_max[1]:f})')

#Fit the data to an exponential distribution
#loc, scale = stats.expon.fit(sampleData)
#dist_data = []
##Generate values given the parameters of the distribution
#sample_data = stats.expon.rvs(scale, len(sampleData))
#print(stats.describe(sample_data))
#for i in range(len(sampleData)):
#    dist_data.append(random.expovariate(1/scale))

#x = np.linspace(0, 12, 100)
#fitted_data = stats.distributions.expon.pdf(x, loc, scale)

#plt.hist(sampleData, density = True, bins = 20)
#plt.plot(x, fitted_data, 'r-')
#plt.show()
#print(stats.chisquare(dist_data, sampleData))
