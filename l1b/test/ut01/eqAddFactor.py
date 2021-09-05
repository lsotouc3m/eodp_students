
# Retrieve the multiplicative factor for the equalization
# TOA = TOA*(1+k*PRNU) + DS*(1+k*DSNU)
# Therefore the DS*(1+k*DSNU) is an additive factor per pixel. Dark image.

from common.io.writeToa import readToa
from config.globalConfig import globalConfig
from config.l1bConfig import l1bConfig
from common.io.readFactor import writeFactor, EQ_ADD, NC_EXT
import numpy as np
import os

# Inputs
# ----------------------------------------------------------------------------------------------------------------------
rootdir = '/home/luss/EODP/eodp/ism/test/ut03/'
toa_ref_dir = os.path.join(rootdir,'output_ref')
toa_ds_dir = os.path.join(rootdir,'output_ds')

outputdir = '/home/luss/EODP/eodp/l1b/test/ut03/output'

toa_name = globalConfig().ism_toa

# Calculations
# ----------------------------------------------------------------------------------------------------------------------
for band in globalConfig().bands:

    # Read input TOA in radiances
    toa_ref = readToa(toa_ref_dir, toa_name + band + NC_EXT) # [rad]

    # Read output TOA in DN
    toa_ds = readToa(toa_ds_dir, toa_name + band + NC_EXT) # [DN]

    # Compute the gain, factor rad/DN
    eq_add = np.zeros(toa_ref.shape[1])
    irow = int(toa_ref.shape[0]/2) # Get central line to avoid edge effects from the ISRF
    eq_add = toa_ds[irow,:]-toa_ref[irow,:] # [rad/DN]

    # Save to file
    writeFactor(outputdir, l1bConfig().eq_add+band, eq_add, EQ_ADD, "-", "Additive factor for the equalization.")

