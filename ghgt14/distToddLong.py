#!/usr/bin/env python
import sys
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

np.random.seed(seed=233423)

lower = 0
upper = 1
mu = 0.7
sigma = 0.1


X = stats.truncnorm(
    (lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
N = stats.norm(loc=mu, scale=sigma)


#s = N.rvs(100)
s = X.rvs(100)

np.random.seed(seed=255245)
lower = 0
upper = 1
mu = 0.7
sigma = 0.1
X = stats.truncnorm(
    (lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
N = stats.norm(loc=mu, scale=sigma)


s2 = X.rvs(100)

#for i in range(1,101):
#	path = "Sim" + str(i) + "/tlmixpar.dat"
#    	new = open( path, 'w+')
#	new.write("TLMIXPAR \n " + str(s[i-1]) + " " + str(s2[i-1]) + "/ \n\n")

# plot
count, bins, ignored = plt.hist(s, 30, normed=True)
plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
                np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
          linewidth=2, color='r')
plt.show()

count, bins, ignored = plt.hist(s2, 30, normed=True)
plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
                np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
          linewidth=2, color='r')
plt.show()
