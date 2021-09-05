# EXERCISE 1
print('Hello World!')

from datetime import date
today = date.today()
print("Today's date:", today)

import numpy as np
a = np.ones((2,4))
print('a ' + str(a) )

# EXERCISE 2
import numpy as np
a = np.arange(-1,1.001,0.5) # Arran -1:0.5:+1
print('a ' + str(a))
print('Second value a ' + str(a[1])) # Second value
print('Last value a ' + str(a[-1])) # Last value

b=a[1:4] # Assign three intermediate values
print('b ' + str(b))

for ii in a: # Loop over each element and print
    print(ii)

# EXERCISE 3
import numpy as np
import math
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

# (xp,fp)
xp = np.arange(-math.pi,math.pi+0.01,0.1) # Array -pi:0.1:+pi
def sinf(x):
    return math.sin(x)
sinv = np.vectorize(sinf)
fp = sinv(xp)

# (x,f)
x = np.arange(-2*math.pi,2*math.pi+0.01,0.5) # Array -2*pi:0.5:+2*pi

# 1D Cubic spline with not-a-knot boundary condition
cs = CubicSpline(xp, fp, bc_type='not-a-knot')
f = cs(x)

# Plot
fig = plt.figure(figsize=(20,10))
plt.plot(xp,fp,'b-o', label='(xp,fp)')
plt.plot(x,f,'r-o', label='(x,p) interp')
plt.title('Cubic spline interpolation ', fontsize=20)
plt.xlabel('x [-]', fontsize=16)
plt.ylabel('sin(x) [-]', fontsize=16)
plt.grid()
plt.legend()
directory = '/home/luss/EODP/eodp/ism/test/ut01/output'
savestr = directory + "/example"
plt.savefig(savestr)
plt.close(fig)
