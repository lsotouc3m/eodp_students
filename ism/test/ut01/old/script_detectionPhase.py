# Script to test the whole ISM chain

from numpy import zeros, ones
from ism.src.detectionPhase import detectionPhase

# TOA
# -----------------------------------------------------------
# temp, generate a 2D TOA image
toa = 10*ones((20,1000)) # [mW/sr/m2]


# Test the Detection Stage
# -----------------------------------------------------------
myO = detectionPhase()
toa_out = myO.detectionPhase(toa)
myO.logger.info("Testing the Detection Stage")
myO.logger.debug("TOA [mW/sr/m2/nm] " + str(toa[0,0]))
myO.logger.debug("TOA [mW/m2/nm] " + str(toa_out[0,0]))
