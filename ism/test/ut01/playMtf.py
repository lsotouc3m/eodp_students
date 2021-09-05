
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
def sysMTF(npoints):
    fstep = 1/npoints/w
    fc = D/(lambd*focal) # optics cut-off frequency
    f = arange(-1/(2*w),1/(2*w),fstep) # frequencies [-1/w,1/w)
    fn = f/(1/w) # frequencies normalised with (1/w)
    [fnACT,fnALT] = meshgrid(fn,fn,indexing='ij')
    fn2D=sqrt(fnACT*fnACT + fnALT*fnALT)

    f_nyw = 1/(2*w) # Nyquist

    # Calculate the 2D frequencies normalised with the cut-off, for the diffraction MTF
    [frACT,frALT] = meshgrid(fn*(1/w)/fc,fn*(1/w)/fc,indexing='ij')
    fr2D=sqrt(frACT*frACT + frALT*frALT)

    # Optics diffraction MTF
    def acosf(x):
        return acos(x)
    acosv = np.vectorize(acosf)
    Hdiff = (2/pi)*(acosv(fr2D)-fr2D*sqrt(1-fr2D*fr2D))
    Hdiff[fr2D*fr2D>1]=0

    # Detector MTF
    # detMtfNyquist=0.5
    # ff=1
    # k=-4*log(detMtfNyquist/sinc(ff/2));
    # def expf(x):
    #     return exp(x)
    # expv = np.vectorize(expf)
    # Hdet=sinc(fn2D)*expv(-k*fn2D*fn2D)
    Hdet=sinc(fn2D)

    # System MTF
    Hsys = Hdiff*Hdet
    print('Imaginary part of the Hsys ' + str(np.max(np.imag(Hsys))))
    Hsys = np.real(Hsys)

    # Plot cuts of the MTF
    ns=int(len(f)/2)
    fig = plt.figure(figsize=(20,10))
    plt.plot(-fn[0:ns], abs(Hdiff[0:ns,ns]),label='Diffraction MTF')
    plt.plot(-fn[0:ns], abs(Hdet[0:ns,ns]),label='Detector MTF')
    plt.plot(-fn[0:ns], abs(Hsys[0:ns,ns]),linewidth=2,label='System MTF')
    auxv = arange(0,1.1,0.1)
    plt.plot(0.5*ones(auxv.shape),auxv,label='f Nyquist')
    plt.title('System MTF', fontsize=20)
    plt.xlabel('Spatial frequencies f/(1/w) [-]', fontsize=16)
    plt.ylabel('MTF', fontsize=16)
    plt.grid()
    plt.legend()
    saveas_str = 'system_mtf'
    savestr = directory + "/" + saveas_str
    plt.savefig(savestr)
    plt.close(fig)
    print("Saved image " + savestr)

    return Hsys

# Calculation of the PSF
# ----------------------------------------------------------------------------------------------
npoints=10
Hsys= sysMTF(npoints)
PSF = fftshift(ifft2(fftshift(Hsys)))
print('Imaginary part of the PSF ' + str(np.max(np.imag(PSF))))
PSF = np.real(PSF)

dw=2*pi*1/npoints/w
ds=1/float(PSF.shape[0])/dw
smax=ceil((float(PSF.shape[0])-1)/2.0)
s=ds*arange(-smax, smax)
ip = interp2d(s/w,s/w,PSF) # interpolant

kernel_half_width = 0.5
kernel_step = 0.1
p_int=arange(-kernel_half_width, kernel_half_width, kernel_step)
PSF_int_trunc = ip(p_int,p_int) # interpolated PSF
PSF_int_trunc=PSF_int_trunc/sum(PSF_int_trunc[:])

fig = plt.figure(figsize=(20,10))
idx=int(ceil((PSF_int_trunc.shape[0]-1)/2.0))
plt.plot(p_int, PSF_int_trunc[:,idx])
plt.title('System PSF', fontsize=20)
plt.xlabel('Pixel number [-]', fontsize=16)
plt.ylabel('PSF', fontsize=16)
plt.grid()
saveas_str = 'system_psf'
savestr = directory + "/" + saveas_str
plt.savefig(savestr)
plt.close(fig)
print("Saved image " + savestr)

# Generate TOA
# ----------------------------------------------------------------------------------------------
# 2D TOA with increasing frequencies
nlines=100
ncolumns = 100
toaline = arange(0,ncolumns)
toa = repmat(toaline,nlines,1)


# Colvolve TOA with PSF
# ----------------------------------------------------------------------------------------------
# Build the PSF grid by taking into account both the PSF
# oversampling factor and the TOA oversampling factor
ovx_def = 1+arange(0,toa.shape[0])
ovy_def = 1+arange(0,toa.shape[1])
ip2 = interp2d(ovx_def,ovy_def,toa, kind='linear',bounds_error=False,fill_value=(0,0)) # interpolant # toa_interp=interp2(rad2D_spectral_slice,movy,movx,'linear',0)

ovf=np.round(1/kernel_step)
ovx=arange(ovf,ovf*nlines+ovf/10)/ovf
ovy=arange(ovf,ovf*ncolumns+ovf/10)/ovf
toa_interp = ip2(ovx,ovy)

# Convolution
toa_conv=convolve2d(toa_interp,PSF_int_trunc)

# Return to nominal sampling
Lpsftail=int(np.floor((len(p_int)-1)/2))
idx = arange(Lpsftail,toa_conv.shape[0],int(ovf))
idy = arange(Lpsftail,toa_conv.shape[1],int(ovf))
toa_conv_sampl = np.zeros((len(idx),len(idy)))
for irow in range(len(idx)):
    for icol in range(len(idy)):
        toa_conv_sampl[irow,icol] = toa_conv[idx[irow],idy[icol]]

# Save & plot
saveas_str = 'toa_psf'
writeToa(directory, saveas_str, toa_conv_sampl)

title_str = 'TOA convolved with the PSF'
xlabel_str = ''
ylabel_str = ''
plotMat2D(toa_conv, title_str, xlabel_str, ylabel_str, directory, saveas_str)
saveas_str = 'toa_psf_1d'
plotF([], toa_conv[50,:], title_str, xlabel_str, ylabel_str, directory, saveas_str)

# FT(TOA) x System MTF and then IFFT(TOA)
# ----------------------------------------------------------------------------------------------
Hsys2 = sysMTF(ncolumns)
GE = fft2(toa)
GE_img = GE* fftshift(Hsys2) # Shift the MTF so that the 1 in in the first position
toa_ft = ifft2(GE_img)
toa_ft = np.real(toa_ft)

# Save & plot
saveas_str = 'toa_mtf'
writeToa(directory, saveas_str, toa_ft)

title_str = 'TOA multiplied with MTF'
plotMat2D(toa_ft, title_str, xlabel_str, ylabel_str, directory, saveas_str)
saveas_str = 'toa_mtf_1d'
plotF([], toa_ft[50,:], title_str, xlabel_str, ylabel_str, directory, saveas_str)

# Compare (kind of)
# ----------------------------------------------------------------------------------------------
# There are edge effects in both the PSD (half the kernels size), and the MTF
# So we compare only in the central positions
margin = 10
abstoa = toa_conv_sampl[margin:-margin,margin:-margin]-toa_ft[margin:-margin,margin:-margin]
reltoa = abstoa/toa_conv_sampl[margin:-margin,margin:-margin]
print('Absolute difference between PSF/MTF ' + str(np.max(abstoa)))
print('Relative difference between PSF/MTF ' + str(np.max(reltoa)))

luss =1
