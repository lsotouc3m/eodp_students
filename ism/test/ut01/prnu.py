# Generate a vector for the PRNU that follows the standard distribution

import numpy as np

np.random.seed(123456789)

mu=0
sigma=1
N=1000
s = np.random.normal(mu, sigma, N)

# Check the distribution
print('Mean of the distribution ' + str(np.sum(s)/N))
print('Sigma of the distribution ' + str( np.sqrt(1/N * np.sum((s-mu)*(s-mu))) ))


s1 = np.random.normal(mu, sigma, 10)
s2 = np.random.normal(mu, sigma, 10)
print(s1)
print(s2)
luss=1
