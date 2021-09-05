
# Compute the Gain, conversion from DN back to radiances
from common.io.writeToa import readToa
from l1b.test.ut01.old.readGain import writeGain
from config.globalConfig import globalConfig
import numpy as np

# Inputs
# ------------------------------------------------------------------------
toa_dir = '/ism/test/ut02/output'
in_toa_name = globalConfig().ism_toa_isrf # ism_toa_isrf_VNIR-0.nc # After the ISRF integration
out_toa_name = globalConfig().ism_toa
outputdir = '/home/luss/EODP/eodp/l1b/test/ut01/output'

# Do stuff
# ------------------------------------------------------------------------
for band in globalConfig().bands:

    # Read input TOA in radiances
    intoa = readToa(toa_dir, in_toa_name + band + '.nc') # [rad]

    # Read output TOA in DN
    outtoa = readToa(toa_dir, out_toa_name + band + '.nc') # [DN]

    # Compute the gain, factor rad/DN
    gain = np.zeros(intoa.shape[1])
    irow = int(intoa.shape[0]/2) # Get central line to avoid edge effects from the ISRF
    gain[1:] = intoa[irow,1:]/outtoa[irow,1:] # [rad/DN]
    gain[0] = np.mean(gain[1:])

    # Sanity check
    check=outtoa[irow,-1]*gain[-1]
    print('Sanity check. Apply gain ' + str(check) + ' compare ' + str(intoa[irow,-1]))

    # Save to file
    writeGain(outputdir, 'l1b_gain_' + band, gain)

    luss=1
