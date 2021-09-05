
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
import numpy as np
import os
import matplotlib.pyplot as plt

# Inputs
# ----------------------------------------------------------------------------------------------------------------------
rootdir = '/home/luss/EODP/eodp/ism/test/ut04/' # GRADIENT
toa_ref_dir = os.path.join(rootdir,'output_ref')
toa_prnu_ds_dir = os.path.join(rootdir,'output_prnu_ds')

outputdir = '/home/luss/EODP/eodp/l1b/test/ut04/output'
outputfigname = 'toa_equalized_'

# Equalisation files location
auxdir = '/home/luss/EODP/eodp/l1b/test/ut03/output/'


# Calculations
# ----------------------------------------------------------------------------------------------------------------------


for band in globalConfig().bands:

    print("\nEqualization for band " + band)

    # Initialisations
    eq_mult = readFactor(os.path.join(auxdir,l1bConfig().eq_mult+band+NC_EXT),EQ_MULT)
    eq_add = readFactor(os.path.join(auxdir,l1bConfig().eq_add+band+NC_EXT),EQ_ADD)

    # Read "dirty"" TOA in DN (with PRNU, DS)
    toa_dirty = readToa(toa_prnu_ds_dir, globalConfig().ism_toa + band + NC_EXT) # [DN]
    toa_ref = readToa(toa_ref_dir, globalConfig().ism_toa + band + NC_EXT) # [rad]

    # Equalisation
    toa_eq = np.zeros(toa_dirty.shape)
    for ialt in range(toa_dirty.shape[0]):
        toa_eq[ialt,:] = (toa_dirty[ialt,:] - eq_add)/eq_mult # [DN]

    # Compare
    diff_toa = np.abs(toa_eq - toa_ref)
    diff_toa_rel = np.abs(toa_eq - toa_ref)/toa_ref*100
    print("Maximum difference [DN] " + str(np.max(diff_toa)))
    print("Maximum relative [%] " + str(np.max(diff_toa_rel)))

    irow = int(toa_ref.shape[0]/2) # Get central line to avoid edge effects from the ISRF
    # Diff and plot
    fig = plt.figure(figsize=(20,10))
    plt.plot(toa_eq[irow,:], 'k', linewidth=2, label='TOA equalized')
    plt.plot(toa_dirty[irow,:], 'r', linewidth=2, label='TOA not-equalized')
    plt.plot(toa_ref[irow,:], 'b', linewidth=2, label='TOA ideal')
    plt.title('Equalization for ' + band, fontsize=20)
    plt.xlabel('ACT pixel [-]', fontsize=16)
    plt.ylabel('TOA [DN]', fontsize=16)
    plt.grid()
    plt.legend()
    savestr = outputdir + os.path.sep + outputfigname + band
    plt.savefig(savestr)
    plt.close(fig)
    print("Saved image " + savestr)
