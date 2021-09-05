

# Check the application of the gain.
# So, we have the ISM output in DN, and the Gain in Rad/DN.
# We apply output_ism * Gain and we should get the radiances after the application of the ISRF

from config.globalConfig import globalConfig
from config.l1bConfig import l1bConfig
from common.io.readGain import readGain
import matplotlib.pyplot as plt
import os

# INPUTS
# ----------------------------------------------------------------------------------------------------------------------
outputdir = '/home/luss/EODP/eodp/l1b/test/ut01/output'
saveas_str = 'gain'

# Gain files
# gainfile = '/home/luss/EODP/eodp/l1b/test/ut01/output/l1b_gain_'
auxdir = '/home/luss/EODP/eodp/auxiliary'
gainfile = os.path.join(auxdir,l1bConfig().gain_filename)

# CALLS
# ----------------------------------------------------------------------------------------------------------------------

# Diff and plot
fig = plt.figure(figsize=(20,10))


for band in globalConfig().bands:

    # Read gain
    G = readGain(gainfile + band + '.nc') # [rad/DN]

    plt.plot(G, label=band)

plt.title('Gain for the different bands', fontsize=20)
plt.xlabel('ACT pixel [-]', fontsize=16)
plt.ylabel('Gain [rad/DN]', fontsize=16)
plt.grid()
plt.legend()
savestr = outputdir + os.path.sep + saveas_str
plt.savefig(savestr)
plt.close(fig)
print("Saved image " + savestr)
