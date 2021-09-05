
# Compute the Gain, conversion from DN back to radiances
from common.io.writeToa import readToa
from config.globalConfig import globalConfig
import numpy as np

# Inputs
# ------------------------------------------------------------------------
toa_dir = '/home/luss/my_shared_folder/TLS/ism_out/'
in_toa_name = globalConfig().ism_toa_isrf # ism_toa_isrf_VNIR-0.nc # After the ISRF integration
out_toa_name = globalConfig().ism_toa

# Do stuff
# ------------------------------------------------------------------------
for band in globalConfig().bands:

    print('\nBAND ' + band)

    # Read input TOA in radiances
    intoa = readToa(toa_dir, in_toa_name + band + '.nc') # [rad]

    # Read output TOA in DN
    outtoa = readToa(toa_dir, out_toa_name + band + '.nc') # [DN]

    # Compute the gain, a single factor rad/DN
    idx0 = 20
    idx1 = 140
    irow = 50 # Central row
    gain = np.mean(intoa[irow,idx0:idx1]/outtoa[irow,idx0:idx1]) # [rad/DN]
    print('GAIN ' + str(gain))

    # Sanity check
    check=outtoa[irow,-1]*gain
    print('Sanity check. Apply gain ' + str(check) + ' compare ' + str(intoa[irow,-1]))


