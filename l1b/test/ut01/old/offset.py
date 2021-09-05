
# Calculate the equalization coefficients to correct for the
# PRNU and Dark Signal

from common.io.writeToa import readToa
from config.globalConfig import globalConfig
from config.ismConfig import ismConfig
import numpy as np
import os

# Inputs
# ------------------------------------------------------------------------
rootdir = '/home/luss/EODP/eodp/ism/test/ut03/'
toa_ref_dir = os.path.join(rootdir,'output_reference')
toa_ds_dir = os.path.join(rootdir,'output_ds') # DIRECTLY THE OFFSET in [e-]

outputdir = '/home/luss/EODP/eodp/l1b/test/ut03/output'
outputfigname = 'offset_equal'

toa_name = globalConfig().ism_toa+globalConfig().bands[0]+'.nc'

# Do stuff
# ------------------------------------------------------------------------

# OFFSET -> Dark Signal



# The offset in the equalization of the DS should be ds + DN0
# The DSNU is a normal distribution with mean 0
T = ismConfig().T
Tref = ismConfig().Tref
A=ismConfig().ds_A_coeff
B=ismConfig().ds_B_coeff
Sd  = A*((T/Tref)**3) * np.exp(-B*(1/T-1/Tref))  # [e-] Sd 2988.1549207653256 [e-]

# Read ref TOA
# Read ref TOA+DS
toa_ref = readToa(toa_ref_dir,toa_name)
toa_ds = readToa(toa_ds_dir,toa_name)

# The diff in the TOAs is the Dark Signal, which is constant ALT.
diff_toa_DN = toa_ds-toa_ref

bit_depth = ismConfig().bit_depth
OCF = ismConfig().OCF # 5.4e-6  [V/e-] Output conversion factor
ADC_gain = ismConfig().ADC_gain # 0.56 [-]
Vmin = ismConfig().min_voltage # 0.0 [V]
Vmax = ismConfig().max_voltage # 0.86 [V]

# Calculate the conversion factor from e- -> DN
saturation = 2**bit_depth-1
CVF_calc = OCF*ADC_gain/(Vmax)*saturation # [DN/e-] 0.014399162790697676
offset_dn = Sd*CVF_calc # 43.026929147924236 [DN]


