numBins = 30

sampleData = []
data = ''

with open('order_data.txt') as f:
    data = f.read()
f.close()

data_set = data.split('\n\n')
for i in data_set:
    tmp = i.split('\n')
    for j in tmp:
        sampleData.append(round(float(j),9))
sampleSize = len(sampleData)

from scipy import stats
import matplotlib.pyplot as plt

#describe calculates statistics
sampleSize, min_max, sampleMean, sampleVariance, skew, kurtosis= stats.describe(sampleData)
print(f'mean {sampleMean:0.3f}  variance: {sampleVariance:0.3f} range: ({min_max[0]:f}, {min_max[1]:f})')

#generating plots of data
#have every bin to have at least 5 points
binSize = [5, 10, 20, 50, 100]
fig, axs = plt.subplots(len(binSize), 1)
plt.subplots_adjust(hspace=.5)

titleLabel = 'Number of bins: ' + ' '.join([str(bs) for bs in binSize])

fig.suptitle(titleLabel)
for idx, ax in enumerate(axs):
    ax.hist(sampleData, bins=binSize[idx])

plt.show()

#%%
# check chi square goodness of fit of an exponential distribution

from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

# observed
binEdges = np.linspace(0.0, np.max(sampleData), numBins)
observed, _ = np.histogram(sampleData, bins=binEdges)

# MLE
fit_loc, fit_beta = stats.expon.fit(sampleData)

# expected
expectedProb = stats.expon.cdf(binEdges, scale=fit_beta)
expectedProb[-1] += 1.0 - np.sum(np.diff(expectedProb))
expected = sampleSize * np.diff(expectedProb)

binMidPt = (binEdges[1:] + binEdges[:-1]) / 2
plt.hist(sampleData, bins=binEdges, label='Observed')
plt.plot(binMidPt, expected, 'or-', label='Expected')
plt.plot(binMidPt, observed, 'oy-', label='Observed')
plt.legend()
plt.show()

chiSq, pValue = stats.chisquare(f_obs=observed, f_exp=expected)
print(f'ChiSquare Statistic {chiSq:0.3f} P value {pValue:0.3f}')
print('EXPONENTIAL')
print('H0: (null hypothesis) Sample data follows the hypothesized distribution.')
print('H1: (alternative hypothesis) Sample data does not follow a hypothesized distribution.')

if pValue >= 0.05:
    print('we can not reject the null hypothesis')
else:
    print('we reject the null hypothesis')

#%%
# check chi square goodness of fit of a weibull distribution

from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

# observed
binEdges = np.linspace(0.0, np.max(sampleData), numBins)
observed, _ = np.histogram(sampleData, bins=binEdges)


# MLE
fit_alpha, fit_loc, fit_beta=stats.weibull_min.fit(sampleData)

# expected
expectedProb = stats.weibull_min.cdf(binEdges, fit_alpha, scale=fit_beta, loc=fit_loc)
expectedProb[-1] += 1.0 - np.sum(np.diff(expectedProb))
expected = sampleSize * np.diff(expectedProb)

binMidPt = (binEdges[1:] + binEdges[:-1]) / 2
plt.hist(sampleData, bins=binEdges, label='Observed')
plt.plot(binMidPt, expected, 'or-', label='Expected')
plt.plot(binMidPt, observed, 'oy-', label='Observed')
plt.legend()
plt.show()

chiSq, pValue = stats.chisquare(f_obs=observed, f_exp=expected, ddof=0)
print(f'ChiSquare Statistic {chiSq:0.3f} P value {pValue:0.3f}')
print('WEIBULL')
print('H0: (null hypothesis) Sample data follows the hypothesized distribution.')
print('H1: (alternative hypothesis) Sample data does not follow a hypothesized distribution.')

if pValue >= 0.05:
    print('we can not reject the null hypothesis')
else:
    print('we reject the null hypothesis')


#%%
# check chi square goodness of fit of a lognormal distribution

from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

# observed
binEdges = np.linspace(0.0, np.max(sampleData), numBins)
observed, _ = np.histogram(sampleData, bins=binEdges)

# MLE
fit_alpha, fit_loc, fit_beta=stats.lognorm.fit(sampleData)
print('alpha, loc, beta')
print(fit_alpha, fit_loc, fit_beta)

# expected
expectedProb = stats.lognorm.cdf(binEdges, fit_alpha, scale=fit_beta, loc=fit_loc)
expectedProb[-1] += 1.0 - np.sum(np.diff(expectedProb))
expected = sampleSize * np.diff(expectedProb)

binMidPt = (binEdges[1:] + binEdges[:-1]) / 2
plt.hist(sampleData, bins=binEdges, label='Observed')
plt.plot(binMidPt, expected, 'or-', label='Expected')
plt.plot(binMidPt, observed, 'oy-', label='Observed')
plt.legend()
plt.show()

chiSq, pValue = stats.chisquare(f_obs=observed, f_exp=expected)
print(f'ChiSquare Statistic {chiSq:0.3f} P value {pValue:0.3f}')
print('LOGNORMAL')
print('H0: (null hypothesis) Sample data follows the hypothesized distribution.')
print('H1: (alternative hypothesis) Sample data does not follow a hypothesized distribution.')

if pValue >= 0.05:
    print('we can not reject the null hypothesis')
else:
    print('we reject the null hypothesis')

#%%
# check chi square goodness of fit of a gamma distribution

from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

# observed
binEdges = np.linspace(0.0, np.max(sampleData), numBins)
observed, _ = np.histogram(sampleData, bins=binEdges)

# MLE
fit_alpha, fit_loc, fit_beta = stats.gamma.fit(sampleData)

# expected
expectedProb = stats.gamma.cdf(binEdges, fit_alpha, scale=fit_beta, loc=fit_loc)
expectedProb[-1] += 1.0 - np.sum(np.diff(expectedProb))
expected = sampleSize * np.diff(expectedProb)

binMidPt = (binEdges[1:] + binEdges[:-1]) / 2
plt.hist(sampleData, bins=binEdges, label='Observed')
plt.plot(binMidPt, expected, 'or-', label='Expected')
plt.plot(binMidPt, observed, 'oy-', label='Observed')
plt.legend()
plt.show()

chiSq, pValue = stats.chisquare(f_obs=observed, f_exp=expected)
print(f'ChiSquare Statistic {chiSq:0.3f} P value {pValue:0.3f}')
print('GAMMA')
print('H0: (null hypothesis) Sample data follows the hypothesized distribution.')
print('H1: (alternative hypothesis) Sample data does not follow a hypothesized distribution.')

if pValue >= 0.05:
    print('we can not reject the null hypothesis')
else:
    print('we reject the null hypothesis')
