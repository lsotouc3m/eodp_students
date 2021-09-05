
# Test FFT2, IFFT2 and the shifts

import numpy as np
from numpy.fft import fftshift, ifft2, ifftshift, fft2
from numpy.matlib import repmat

# Generate TOA
# ----------------------------------------------------------------------------------------------
# 2D TOA with increasing frequencies
of = 1
nlines=100
ncolumns = 100
toaline = np.arange(0,ncolumns)
toa = repmat(toaline,nlines,1)

# Retrieve original TOA after FFT and IFFT
# ----------------------------------------------------------------------------------------------
toaft = fft2(toa)
toaifft = ifft2(toaft)
toaifft = np.real(toaifft)
toaifft==toa # This is kinda correct. toaifft has imag parts and slight inprecisions
print('Max difference after conversion ' + str(np.max(toaifft-toa)))

# toaft2 = fft2(ifftshift(toa)) NO- Starts flipping +/-
toaifft2 = fftshift(ifft2(toaft))
toaifft2==toa # WRONG - It's actually shifted

luss=1
