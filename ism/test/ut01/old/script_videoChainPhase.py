# Script to test the whole ISM chain

from numpy import zeros, ones, linspace
from numpy.matlib import repmat
from ism.src.videoChainPhase import videoChainPhase
from common.plot.plotF import plotF

# Inputs
# -----------------------------------------------------------
directory = '/home/luss/EODP/eodp/ism/test/ut01/output'

# TOA
# -----------------------------------------------------------
myO = videoChainPhase()
myO.logger.info("Testing the Electronics Stage")

# Calculate min/max voltages, and e-
factor = myO.ismConfig.OCF * myO.ismConfig.ADC_gain
myO.logger.debug("Factor " + str(factor))
max_e = myO.ismConfig.max_voltage/factor # weird
myO.logger.debug("Mex number of e- " + str(max_e))

# temp, generate a 2D TOA image
toa = repmat(linspace(0.0, max_e, 1000), 20, 1)

# Test the Rad2Irrad
# -----------------------------------------------------------
toa_out = myO.videoChainPhase(toa)
myO.logger.debug("TOA [0,0] in [e-] " + str(toa[0,0]))
myO.logger.debug("TOA [0,0] out [DN] " + str(toa_out[0,0]))
myO.logger.debug("TOA[0,-1] out [DN] " + str(toa_out[0,-1]))

title_str = "Electronics stage"
xlabel_str = 'ACT'
ylabel_str = 'DN'
saveas_str = 'toa_dn'
plotF(toa_out[0,:], [], title_str, xlabel_str, ylabel_str, directory, saveas_str)
