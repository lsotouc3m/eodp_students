
# Script to test the bad/dead pixels

from numpy import  ones
from common.plot.plotMat2D import plotMat2D
from common.io.writeToa import writeToa
from ism.src.detectionPhase import detectionPhase


# Initialise the TOA
toa = 10*ones((2000,1500))

# Call the function
myDet = detectionPhase()
toa = myDet.badDeadPixels(toa,
                          myDet.ismConfig.bad_pix,
                          myDet.ismConfig.dead_pix,
                          myDet.ismConfig.bad_pix_red,
                          myDet.ismConfig.dead_pix_red)

# Plot
title_str = "Bad and Dead pixels over a homogeneous scene"
xlabel_str = 'ACT'
ylabel_str = 'ALT'
directory = '/home/luss/EODP/eodp/ism/test/ut01/output'
saveas_str = 'bad_dead_pix'
plotMat2D(toa, title_str, xlabel_str, ylabel_str, directory, saveas_str)

# Save to file
writeToa(directory, 'toa_baddead.nc', toa)
