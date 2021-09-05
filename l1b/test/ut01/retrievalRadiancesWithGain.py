
# Check the application of the gain.
# So, we have the ISM output in DN, and the Gain in Rad/DN.
# We apply output_ism * Gain and we should get the radiances after the application of the ISRF

from config.globalConfig import globalConfig
from config.l1bConfig import l1bConfig
from common.io.writeToa import readToa
import numpy as np
from common.src.auxFunc import getIndexBand
import matplotlib.pyplot as plt
import os

# INPUTS
# ----------------------------------------------------------------------------------------------------------------------
# ISM output files
ismdir = '/home/luss/EODP/eodp/ism/test/ut02/output'
ism_out_file = globalConfig().ism_toa # [DN]

# ISM after ISRF files (spectral integration)
ism_isrf_file = globalConfig().ism_toa_isrf # [rad]

# outputs
outputdir = '/home/luss/EODP/eodp/l1b/test/ut02/output'
saveas_str = 'diff_toa'

# CALLS
# ----------------------------------------------------------------------------------------------------------------------

# Init plot
fig = plt.figure(figsize=(20,10))

for band in globalConfig().bands:

    print('\nBAND ' + band)

    # Read input TOA in radiances (after the spectral integration and ISRF)
    toa_rad_ref = readToa(ismdir, ism_isrf_file + band + '.nc') # [rad]

    # Read output TOA in DN
    toa_dn = readToa(ismdir, ism_out_file + band + '.nc') # [DN]

    # Read gain
    G = l1bConfig().gain[getIndexBand(band)] # [rad/DN]

    # Apply gain
    toa_rad = toa_dn*G # [rad]

    # Checks
    print('Sanity check. after gain ' + str(toa_rad[50,-1]) + ' compare ' + str(toa_rad_ref[50,-1]))
    diff_toa = np.abs(toa_rad-toa_rad_ref)
    diff_toa = diff_toa[1:-1] # There are edge effects in the first and last rows!!
    idx = np.argwhere(diff_toa==np.max(diff_toa))
    print('TOA difference, maximum: ' + str(np.max(diff_toa)) + '. idx ' + str(idx[0]))
    print('Sanity check at idx. after gain ' + str(toa_rad[idx[0][0], idx[0][1]]) + ' compare ' + str(toa_rad_ref[idx[0][0], idx[0][1]]))

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


