
# Check the input TOA to the ISM and the output TOA after the L1B calibration

import numpy as np
from common.io.writeToa import readToa
from config.globalConfig import globalConfig
import matplotlib.pyplot as plt
import os

# Inputs
# ------------------------------------------------------------------------
ismdir = '/home/luss/EODP/eodp//ism/test/ut02/output'
ism_toa = globalConfig().ism_toa_isrf # After the spectral integration and the ISRF

l1bdir = '/home/luss/EODP/eodp/l1b/test/ut02/output'
l1b_toa = globalConfig().l1b_toa

# outputs
outputdir = '/home/luss/EODP/eodp/l1b/test/ut02/output'
saveas_str = 'diff_toa_ism_l1b'

# Compare
# ------------------------------------------------------------------------

# Init plot
fig = plt.figure(figsize=(20,10))

for band in globalConfig().bands:

    print('\nBAND ' + band)

    # Read input TOA in radiances
    intoa = readToa(ismdir, ism_toa + band + '.nc') # [rad]

    # Read output TOA in radiances
    outtoa = readToa(l1bdir, l1b_toa + band + '.nc') # [rad]

    # Differences
    diff_toa = np.abs(intoa-outtoa)
    # diff_toa = diff_toa[1:-1] # There are edge effects in the first and last rows!!
    idx = np.argwhere(diff_toa==np.max(diff_toa))
    print('TOA difference, maximum: ' + str(np.max(diff_toa)) + '. idx ' + str(idx[0]))
    print('Sanity check at idx. L1B OUT ' + str(outtoa[50,-1]) + ' compare ISM IN ' + str(intoa[50,-1]))

    # Plot for one ALT position
    plt.plot(diff_toa[50,0:-1], label=band) # Excludes the last pixel

plt.title('Difference in the after restoration', fontsize=20)
plt.xlabel('ACT pixel [-]', fontsize=16)
plt.ylabel('Difference in Radiances [mW/m2/sr]', fontsize=16)
plt.grid()
plt.legend()
savestr = outputdir + os.path.sep + saveas_str
plt.savefig(savestr)
plt.close(fig)
print("Saved image " + savestr)
