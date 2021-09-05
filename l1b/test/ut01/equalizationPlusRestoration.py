
# Check the whole L1B chain
# So equalization + restoration (Gain)

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
rootdir = '/home/luss/EODP/eodp/ism/test/ut02/'
toa_prnu_ds_dir = os.path.join(rootdir,'output')

outputdir = '/home/luss/EODP/eodp/l1b/test/ut02/output'
outputfigname = 'toa_equalized_restored_'

# Equalisation
auxdir = '/home/luss/EODP/eodp/auxiliary/'


# Calculations
# ----------------------------------------------------------------------------------------------------------------------


for band in globalConfig().bands:

    print("\nEqualization for band " + band)

    # Initialisations
    eq_mult = readFactor(os.path.join(auxdir,l1bConfig().eq_mult+band+NC_EXT),EQ_MULT)
    eq_add = readFactor(os.path.join(auxdir,l1bConfig().eq_add+band+NC_EXT),EQ_ADD)
    gain = l1bConfig().gain[getIndexBand(band)]

    # Read "dirty"" TOA in DN (with PRNU, DS)
    toa_dirty = readToa(toa_prnu_ds_dir, globalConfig().ism_toa + band + NC_EXT) # [DN]

    # TOA in radiances - output of the ISRF
    toa_isrf = readToa(toa_prnu_ds_dir, globalConfig().ism_toa_isrf + band + NC_EXT) # [rad]

    # TOA in radiances - restored in the L1B
    toa_l1b = readToa(outputdir, globalConfig().l1b_toa + band + NC_EXT) # [rad]

    # Equalisation
    toa_eq = np.zeros(toa_dirty.shape)
    for ialt in range(toa_dirty.shape[0]):
        toa_eq[ialt,:] = (toa_dirty[ialt,:] - eq_add)/eq_mult # [DN]

    # Restoration
    toa_rad = toa_eq*gain # [rad]

    # Compare
    diff_toa = np.abs(toa_rad - toa_isrf)
    diff_toa_rel = np.abs(toa_rad - toa_isrf)/toa_isrf*100
    print("Maximum difference [mW/m2/sr] " + str(np.max(diff_toa)))
    print("Maximum relative [%] " + str(np.max(diff_toa_rel)))

    irow = int(toa_isrf.shape[0]/2) # Get central line to avoid edge effects from the ISRF
    # Diff and plot
    fig = plt.figure(figsize=(20,10))
    plt.plot(toa_rad[irow,:], 'k', linewidth=2, label='TOA equalized+restored')
    plt.plot(toa_l1b[irow,:], 'r', linewidth=2, label='TOA L1B')
    plt.plot(toa_isrf[irow,:], 'b', linewidth=2, label='TOA after the ISRF')
    plt.title('Equalization and restoration for ' + band, fontsize=20)
    plt.xlabel('ACT pixel [-]', fontsize=16)
    plt.ylabel('TOA [mW/m2/sr]', fontsize=16)
    plt.grid()
    plt.legend()
    savestr = outputdir + os.path.sep + outputfigname + band
    plt.savefig(savestr)
    plt.close(fig)
    print("Saved image " + savestr)
