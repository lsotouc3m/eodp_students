# Script to test the whole ISM chain

from numpy import zeros, ones
from ism.src.opticalPhase import opticalPhase

# TOA
# -----------------------------------------------------------
# temp, generate a 2D TOA image
toa = 10*ones((20,1000)) # [mW/sr/m2]



# Test the Rad2Irrad
# -----------------------------------------------------------
myO = opticalPhase()
toa_irr = myO.opticalPhase(toa)
myO.logger.info("Testing the Rad 2 Irrad conversion")
myO.logger.debug("TOA [mW/sr/m2/nm] " + str(toa[0,0]))
myO.logger.debug("TOA [mW/m2/nm] " + str(toa_irr[0,0])) # OK
