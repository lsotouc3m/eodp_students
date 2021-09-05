
# Retrieve the multiplicative factor for the equalization
# TOA = TOA*(1+k*PRNU) + DS*(1+k*DSNU)
# Therefore the (1*k*PRNU) is a multiplicative factor per pixel. Flat field calibration
# IMPORTANT
# We calculate the PRNU with a simulation with PRNU+DS
# And we remove the offset
# TOA_prnu_ds = TOA_ideal*PRNU + DS
# PRNU = (TOA_prnu_ds-DS)/TOA_ideal

from common.io.writeToa import readToa
from config.globalConfig import globalConfig
from config.l1bConfig import l1bConfig
from common.io.readFactor import writeFactor, EQ_MULT, EQ_ADD, NC_EXT, readFactor
import numpy as np
import os

# Inputs
# ----------------------------------------------------------------------------------------------------------------------
rootdir = '/home/luss/EODP/eodp/ism/test/ut03/'
toa_ref_dir = os.path.join(rootdir,'output_ref')
toa_prnu_dir = os.path.join(rootdir,'output_prnu_ds') # WITH DARK SIGNAL

outputdir = '/home/luss/EODP/eodp/l1b/test/ut03/output'

# Calculations
# ----------------------------------------------------------------------------------------------------------------------
for band in globalConfig().bands:

    # Read input TOA in radiances
    toa_ref = readToa(toa_ref_dir, globalConfig().ism_toa + band + NC_EXT) # [rad]

    # Read output TOA in DN
    toa_prnu = readToa(toa_prnu_dir, globalConfig().ism_toa + band + NC_EXT) # [DN]

    # Read the offset
    eq_add = readFactor(os.path.join(outputdir,l1bConfig().eq_add+band+NC_EXT),EQ_ADD)

    # Compute the gain, factor rad/DN
    eq_mult = np.zeros(toa_ref.shape[1])
    irow = int(toa_ref.shape[0]/2) # Get central line to avoid edge effects from the ISRF
    eq_mult = (toa_prnu[irow,:] - eq_add)/toa_ref[irow,:] # [rad/DN] REMOVE THE OFFSET

    # Save to file
    writeFactor(outputdir, l1bConfig().eq_mult+band, eq_mult, EQ_MULT, "-", "Multiplicative factor for the equalization.")





