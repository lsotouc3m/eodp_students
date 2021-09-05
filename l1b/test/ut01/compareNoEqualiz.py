
# Compare a case with and without equalization
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

l1bdir = '/home/luss/EODP/eodp/l1b/test/ut02/output'
l1bdir_noeq = '/home/luss/EODP/eodp/l1b/test/ut02/output_noeq'

outputfigname = 'toa_comp_equaliz_'

# Equalisation
auxdir = '/home/luss/EODP/eodp/auxiliary/'


# Calculations
# ----------------------------------------------------------------------------------------------------------------------


for band in globalConfig().bands:

    print("\nEqualization for band " + band)

    # TOA in radiances - output of the ISRF
    toa_isrf = readToa(toa_prnu_ds_dir, globalConfig().ism_toa_isrf + band + NC_EXT) # [rad]

    # TOA in radiances - restored in the L1B
    toa_l1b = readToa(l1bdir, globalConfig().l1b_toa + band + NC_EXT) # [rad]
    toa_l1b_noeq = readToa(l1bdir_noeq, globalConfig().l1b_toa + band + NC_EXT) # [rad]

    irow = int(toa_isrf.shape[0]/2) # Get central line to avoid edge effects from the ISRF
    # Diff and plot
    fig = plt.figure(figsize=(20,10))
    plt.plot(toa_l1b[irow,:], 'k', linewidth=2, label='TOA L1B with eq')
    plt.plot(toa_l1b_noeq[irow,:], 'r', linewidth=2, label='TOA L1B no eq')
    plt.plot(toa_isrf[irow,:], 'b', linewidth=2, label='TOA after the ISRF')
    plt.title('Effect of the Equalization for ' + band, fontsize=20)
    plt.xlabel('ACT pixel [-]', fontsize=16)
    plt.ylabel('TOA [mW/m2/sr]', fontsize=16)
    plt.grid()
    plt.legend()
    savestr = l1bdir + os.path.sep + outputfigname + band
    plt.savefig(savestr)
    plt.close(fig)
    print("Saved image " + savestr)
