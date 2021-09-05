
# Check the application of the gain.
# So, we have the ISM output in DN, and the Gain in Rad/DN.
# We apply output_ism * Gain and we should get the radiances after the application of the ISRF

from config.globalConfig import globalConfig
from config.l1bConfig import l1bConfig
from common.io.writeToa import readToa
from common.io.readGain import readGain
import numpy as np
import os

# INPUTS
# ----------------------------------------------------------------------------------------------------------------------
# Gain files
auxdir = '/home/luss/EODP/eodp/auxiliary'
gainfile = os.path.join(auxdir,l1bConfig().gain_filename)

# ISM output files
ismdir = '/home/luss/EODP/eodp/ism/test/ut02/output'
ism_out_file = globalConfig().ism_toa # [DN]

# ISM after ISRF files (spectral integration)
ism_isrf_file = globalConfig().ism_toa_isrf # [rad]


# AUXILIARY
# ----------------------------------------------------------------------------------------------------------------------
def applyGain(toa_dn, G):
    '''
    Application of the Gain
    :param toa_dn: TOA in Digital Numbers
    :param G: Gain, read from auxliary in [rad/DN]
    :return: TOA in radiance units [mW/m2/nm/sr]
    '''
    # Check that the sizes are consistent
    if toa_dn.shape[1] != len(G):
        raise Exception('Sizes of the TOA and the Gain are not consistent. TOA ALT x ACT' + str(toa_dn.shape)
                        + ' Gain ' + str(len(G)) )

    toa_rad = np.zeros(toa_dn.shape)
    for irow in range(toa_dn.shape[0]):
        toa_rad[irow,:] = toa_dn[irow,:]*G

    return toa_rad

# CALLS
# ----------------------------------------------------------------------------------------------------------------------
for band in globalConfig().bands:

    print('\nBAND ' + band)

    # Read input TOA in radiances (after the spectral integration and ISRF)
    toa_rad_ref = readToa(ismdir, ism_isrf_file + band + '.nc') # [rad]

    # Read output TOA in DN
    toa_dn = readToa(ismdir, ism_out_file + band + '.nc') # [DN]

    # Read gain
    G = readGain(gainfile + band + '.nc') # [rad/DN]

    # Apply gain
    toa_rad = applyGain(toa_dn, G) # [rad]

    # Checks
    print('Sanity check. after gain ' + str(toa_rad[50,-1]) + ' compare ' + str(toa_rad_ref[50,-1]))
    diff_toa = np.abs(toa_rad-toa_rad_ref)
    diff_toa = diff_toa[1:-1] # There are edge effects in the first and last rows!!
    idx = np.argwhere(diff_toa==np.max(diff_toa))
    print('TOA difference, maximum: ' + str(np.max(diff_toa)) + '. idx ' + str(idx[0]))
    print('Sanity check at idx. after gain ' + str(toa_rad[idx[0][0], idx[0][1]]) + ' compare ' + str(toa_rad_ref[idx[0][0], idx[0][1]]))

    luss=0
