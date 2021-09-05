
# Plot the NL effect from FLEX

from common.io.readTwoColumns import readTwoColumns
import matplotlib.pyplot as plt

# Inputs
# ----------------------------------------------------------------------------
outputdir = '/home/luss/EODP/eodp/ism/test/ut01/output'
nllutfile = '/home/luss/FLEX/flex-fips/auxiliary/fips/CCDB/non_linearity/flex_NL_simu_16042020.txt'

# Read NL LUT
# ----------------------------------------------------------------------------
# Read input TOA+LUT
# ----------------------------------------------------------------------
xp,fp = readTwoColumns(nllutfile) # Non-linearity LUT col1->col2

# Plot
# ----------------------------------------------------------------------------
title_str = 'Non-linearity'
xlabel_str = 'Excitation [DN]'
ylabel_str = 'Response [DN]'
directory = outputdir
saveas_str = 'flex_nl'

# Diff and plot
fig = plt.figure(figsize=(10, 7))
plt.plot(xp, xp, '--k',label='linear')
plt.plot(xp, fp, '-r',label='nl')
plt.title(title_str, fontsize=20)
plt.xlabel(xlabel_str, fontsize=16)
plt.ylabel(ylabel_str, fontsize=16)
plt.grid()
plt.legend()
savestr = directory + "/" + saveas_str
plt.savefig(savestr)
plt.close(fig)
print("Saved image " + savestr)
