import numpy as np
import matplotlib.pyplot as plt
from common.plot.plotMat2D import plotMat2D
from common.plot.plotF import plotF
from math import pi, acos, sqrt

# Construct the spatial frequencies for the MTF calculation

# Inputs
# ----------------------------------------------------------------------
p = 30e-6 # Pixel size [m]
n_points = 10
D = 0.150 # Telescope pupil diameter [m]
wv = 0.49e-6 # channel VNIR0 of the LSTM. Central wavelength [m]
f = 0.5262 # Focal length [m]

outputdir = '/home/luss/EODP/eodp/ism/test/ut01/output/'

# Frequencies
# ----------------------------------------------------------------------
# Optics cut-off frequency
fc = D/(wv*f)
print("Cut-off frequency fc " + str(fc))

# 1D frequencies
# df = 1/(n_points*p);
df = 2*fc/n_points;
# fmax= 1/p # Inverse of the pixel size
fmax=2*fc # Twice the cut-off frequency
print("fmax " + str(fmax) + " df " + str(df))

fr = np.arange(-fmax/2, +fmax/2 -df/100.0, df) # Last point is not taken on purpose
frel = fr/fc
print("First two indexes fr " + str(fr[0:2]) + " Last index " + str(fr[-1]))
print("First two indexes frel " + str(frel[0:2]) + " Last index " + str(frel[-1]))
plotF(frel, [], "Relative frequencies (fr/fc) ", "", "", outputdir, "frel")

# 2D frequencies
xv, yv = np.meshgrid(frel, frel)
frel2d = np.sqrt(xv*xv + yv*yv)
frel2d[np.where(frel2d > 1)] = 0
plotMat2D(frel2d, "Relative frequencies 2D", "[-]", "frel_2d [-]", outputdir, "frel2d")
f_alt = frel2d[np.int(frel2d.shape[0]/2), :]
f_act = frel2d[:, np.int(frel2d.shape[1]/2)]
plotF(f_alt, [], "Relative frequencies 2D - cut centre ALT", "[ALT]", "[-]", outputdir, "frel2d_1d_alt")


# Diffraction MTF
# https://spie.org/publications/tt52_151_diffraction_mtf?SSO=1
# ----------------------------------------------------------------------
def mtf_diffract(frel2d):
    return 2/pi * (acos(frel2d) - frel2d*sqrt(1-frel2d*frel2d))
mtf_diffract_v = np.vectorize(mtf_diffract)

plotMat2D(mtf_diffract_v(frel2d), "Diffraction MTF", "fr/fc [ACT]", "fr/fc [ALT]", outputdir, "mtf_diffract")
# plot 2D cuts
plotF(f_alt, mtf_diffract_v(f_alt), "Diffraction MTF - cut centre ALT", "fr/fc [ALT]", "[-]", outputdir, "mtf_diffract_1d_alt")
plotF(f_act, mtf_diffract_v(f_act), "Diffraction MTF - cut centre ACT", "fr/fc [ACT]", "[-]", outputdir, "mtf_diffract_1d_act")

