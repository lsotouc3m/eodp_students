
# Roughly the TOA is like this
# TOA = TOA*(1+k*PRNU) + DS*(1+k*DSNU)
#
# Therefore the (1*k*PRNU) is a multiplicative factor per pixel. Flat field calibration
# Therefore the DS*(1+k*DSNU) is an additive factor per pixel. Dark image.
#
# Here we read the ISM output TOA, we use the gain, and equalization mult and add factors
# We compare with the input TOA (after ISRF) and it should be the same (?)
#
from common.io.writeToa import readToa
from config.globalConfig import globalConfig
from config.l1bConfig import l1bConfig
from common.io.readFactor import readFactor, EQ_MULT, EQ_ADD, NC_EXT
from common.src.auxFunc import getIndexBand
import numpy as np
import os
import matplotlib.pyplot as plt

# Inputs
# ----------------------------------------------------------------------------------------------------------------------
rootdir = '/home/luss/EODP/eodp/ism/test/ut03/'
toa_ref_dir = os.path.join(rootdir,'output_ref')
toa_prnu_dir = os.path.join(rootdir,'output_prnu')

outputdir = '/home/luss/EODP/eodp/l1b/test/ut03/output'

# Equalisation
auxdir = '/home/luss/EODP/eodp/l1b/test/ut03/output/'


# Calculations
# ----------------------------------------------------------------------------------------------------------------------

for band in globalConfig().bands:

    print("\nEqualization for band " + band)

    # Initialisations
    eq_mult = readFactor(os.path.join(auxdir,l1bConfig().eq_mult+band+NC_EXT),EQ_MULT)

    # Read "dirty"" TOA in DN (with PRNU, DS)
    toa_dirty = readToa(toa_prnu_dir, globalConfig().ism_toa + band + NC_EXT) # [DN]
    toa_ref = readToa(toa_ref_dir, globalConfig().ism_toa + band + NC_EXT) # [rad]

    # Equalisation
    toa_eq = np.zeros(toa_dirty.shape)
    for ialt in range(toa_dirty.shape[0]):
        toa_eq[ialt,:] = (toa_dirty[ialt,:])/eq_mult # [DN]

    # Compare
    diff_toa = np.abs(toa_eq - toa_ref)
    diff_toa_rel = np.abs(toa_eq - toa_ref)/toa_ref*100
    print("Maximum difference [DN] " + str(np.max(diff_toa)))
    print("Maximum relative [%] " + str(np.max(diff_toa_rel)))
