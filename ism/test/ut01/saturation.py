# Check the use of argwhere and find indexes and substitute

import numpy as np

toa = np.zeros((2,8))
toa[0,:] = [100, 10000, 41875, 758, 7587857, 587, 7578, 57]
toa[1,:] = [100, 10000, 41875, 758, 7587857, 587, 7578, 57]

idx=np.argwhere(toa>1000)

# toa[idx] = 0 # doesn't work


for ii in range(idx.shape[0]):
    toa[idx[ii][0], idx[ii][1]] = -9999

luss=1
