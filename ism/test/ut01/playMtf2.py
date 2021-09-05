
# Investigate and test whether these two options have the same output
# 1. MTF_sys -> PSF -> convolve with image
# 2. MTF_sys -> FFT of the image -> mult by MTF -> IFFT of the image

from numpy import arange, meshgrid, sqrt, sinc, ones, ceil, abs, sum
from numpy.fft import fftshift, ifft2, ifftshift, fft2

from numpy.matlib import repmat
from math import pi, acos, log, exp
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d
from scipy.signal import convolve2d
from common.plot.plotMat2D import plotMat2D
from common.plot.plotF import plotF
from common.io.writeToa import writeToa

# Inputs
# ----------------------------------------------------------------------------------------------
w = 25e-6 # [m]
focal = 0.4397 # [m]
D = 0.150 # [m]
lambd = 0.49e-6 # [m]

directory = '/home/luss/EODP/eodp/ism/test/ut01/output'

# System MTF = diffraction MTF x detector MTF
# ----------------------------------------------------------------------------------------------
def sysMTF(nlines, ncolumns):

    fc = D/(lambd*focal) # optics cut-off frequency
    # f_nyw = 1/(2*w) # Nyquist

    fstepAlt = 1/nlines/w
    fstepAct = 1/ncolumns/w

    fAlt = arange(-1/(2*w),1/(2*w),fstepAlt) # frequencies [-1/w,1/w)
    fAct = arange(-1/(2*w),1/(2*w),fstepAct) # frequencies [-1/w,1/w)

    fnAlt = fAlt/(1/w) # frequencies normalised with (1/w)
    fnAct = fAct/(1/w) # frequencies normalised with (1/w)


    [fnAltxx,fnActxx] = meshgrid(fnAlt,fnAct,indexing='ij')
    fn2D=sqrt(fnAltxx*fnAltxx + fnActxx*fnActxx)

    # Calculate the 2D frequencies normalised with the cut-off, for the diffraction MTF
    [frAltxx,frActxx] = meshgrid(fnAlt*(1/w)/fc,fnAct*(1/w)/fc,indexing='ij');
    fr2D=sqrt(frAltxx*frAltxx + frActxx*frActxx)

    # Optics diffraction MTF
    def acosf(x):
        return acos(x)
    acosv = np.vectorize(acosf)
    Hdiff = (2/pi)*(acosv(fr2D)-fr2D*sqrt(1-fr2D*fr2D))
    Hdiff[fr2D*fr2D>1]=0

    # Detector MTF
    Hdet=sinc(fn2D)

    # System MTF
    Hsys = Hdiff*Hdet
    print('Imaginary part of the Hsys ' + str(np.max(np.imag(Hsys))))
    Hsys = np.real(Hsys)

    # Plot cuts of the MTF ACT
    mAlt=int(nlines/2.0)
    mAct=int(ncolumns/2.0)

    fig = plt.figure(figsize=(20,10))
    plt.plot(-fnAct[0:mAct], abs(Hdiff[mAlt,0:mAct]),label='Diffraction MTF')
    plt.plot(-fnAct[0:mAct], abs(Hdet[mAlt,0:mAct]),label='Detector MTF')
    plt.plot(-fnAct[0:mAct], abs(Hsys[mAlt,0:mAct]),linewidth=2,label='System MTF')
    auxv = arange(0,1.1,0.1)
    plt.plot(0.5*ones(auxv.shape),auxv,label='f Nyquist')
    plt.title('System MTF - slice ACT', fontsize=20)
    plt.xlabel('Spatial frequencies f/(1/w) [-]', fontsize=16)
    plt.ylabel('MTF', fontsize=16)
    plt.grid()
    plt.legend()
    saveas_str = 'system_mtf_cutAct'
    savestr = directory + "/" + saveas_str
    plt.savefig(savestr)
    plt.close(fig)
    print("Saved image " + savestr)

    # Plot cuts of the MTF ALT
    fig = plt.figure(figsize=(20,10))
    plt.plot(-fnAlt[0:mAlt], abs(Hdiff[0:mAlt,mAct]),label='Diffraction MTF')
    plt.plot(-fnAlt[0:mAlt], abs(Hdet[0:mAlt,mAct]),label='Detector MTF')
    plt.plot(-fnAlt[0:mAlt], abs(Hsys[0:mAlt,mAct]),linewidth=2,label='System MTF')
    auxv = arange(0,1.1,0.1)
    plt.plot(0.5*ones(auxv.shape),auxv,label='f Nyquist')
    plt.title('System MTF - slice ALT', fontsize=20)
    plt.xlabel('Spatial frequencies f/(1/w) [-]', fontsize=16)
    plt.ylabel('MTF', fontsize=16)
    plt.grid()
    plt.legend()
    saveas_str = 'system_mtf_cutAlt'
    savestr = directory + "/" + saveas_str
    plt.savefig(savestr)
    plt.close(fig)
    print("Saved image " + savestr)

    return Hsys

# Generate TOA
# ----------------------------------------------------------------------------------------------
# 2D TOA with increasing frequencies
nlines=100
ncolumns = 150
toaline = arange(0,ncolumns)
toa = repmat(toaline,nlines,1)


# FT(TOA) x System MTF and then IFFT(TOA)
# ----------------------------------------------------------------------------------------------
Hsys = sysMTF(nlines, ncolumns)
GE = fft2(toa)
GE_img = GE* fftshift(Hsys) # Shift the MTF so that the 1 in in the first position
toa_ft = ifft2(GE_img)
toa_ft = np.real(toa_ft)

# Save & plot
saveas_str = 'toa_mtf'
# writeToa(directory, saveas_str, toa_ft)

title_str = 'TOA multiplied with MTF'
xlabel_str=''
ylabel_str=''
plotMat2D(toa_ft, title_str, xlabel_str, ylabel_str, directory, saveas_str)
saveas_str = 'toa_mtf_1d'
plotF([], toa_ft[50,:], title_str, xlabel_str, ylabel_str, directory, saveas_str)


luss =1
