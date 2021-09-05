from config.ismConfig import ismConfig
from ism.src.mtf import mtf
from common.plot.plotMat2D import plotMat2D
from common.plot.plotF import plotF
import numpy as np
from numpy.fft import fft, fftshift, ifftshift, ifft
from numpy import real, zeros, imag, arange, abs
import matplotlib.pyplot as plt

# Inputs
# ----------------------------------------------------------------

directory = '/home/luss/EODP/eodp/ism/test/ut01/output'




# Create a 2D TOA
# ----------------------------------------------------------------
lines = 20
cols = 30
of = 40#60
toa = np.ones((lines*of,cols*of))
du = ismConfig().pix_size # [m] ACT
dv = ismConfig().pix_size # [m] ALT
nu = toa.shape[1]
nv = toa.shape[0]


# Aux
# ----------------------------------------------------------------
# Init class
myMtf = mtf([])

f_nyq_u = 1/(2*dv/of)
f_nyq_v = 1/(2*dv/of)
print('Nyquist freq ACT ' + str(f_nyq_u))
print('Nyquist freq ALT ' + str(f_nyq_v))

# Optics cut-off frequency
fc = myMtf.optics_cut_off_freq(ismConfig().D,ismConfig().f,ismConfig().wv)
print('Optics cut-off frequency ' + str(fc))

of_th_u = fc*2*du
of_th_v = fc*2*dv
print('Oversampling factor fny=fc act ' + str(of_th_u))
print('Oversampling factor fny=fc alt ' + str(of_th_v))
print('Oversampling applied ' + str(of))

# Calculate OTFs
# ----------------------------------------------------------------
# 1D relative frequencies
v, dfv = myMtf.spatial_freq(dv/of, nv)
u, dfu = myMtf.spatial_freq(du/of, nu)

# Calculate the 1D diffraction MTF
u_rel = u/fc
u_rel[np.where(abs(u_rel) > 1)] = 0
v_rel = v/fc
v_rel[np.where(abs(v_rel) > 1)] = 0
otf_u = myMtf.mtf_diffract(u_rel)
otf_u = otf_u/max(otf_u)
otf_v = myMtf.mtf_diffract(v_rel)
otf_v = otf_v/max(otf_v) # otf[0]

# Check
print('otf_max_u '+ str(myMtf.mtf_diffract(u_rel[-1])))
if f_nyq_u<fc:
    print('OTF at the Nyquist freq '+ str(myMtf.mtf_diffract(f_nyq_u/fc)))
else:
    print('Nyquist freq higher than the cut-off')

title_str = 'u_rel'
xlabel_str = ''
ylabel_str = ''
saveas_str = 'u_rel_of' + str(of)
plotF([], u_rel, title_str, xlabel_str, ylabel_str, directory, saveas_str)
title_str = 'v_rel'
saveas_str = 'v_rel_of' + str(of)
plotF([], v_rel, title_str, xlabel_str, ylabel_str, directory, saveas_str)

title_str = 'OTF_u'
xlabel_str = 'f/fc [-]'
ylabel_str = 'OTF [-]'
saveas_str = 'otf_u_of' + str(of)
plotF(u_rel, otf_u, title_str, xlabel_str, ylabel_str, directory, saveas_str)
title_str = 'OTF_v'
saveas_str = 'otf_v_of' + str(of)
plotF(v_rel, otf_v, title_str, xlabel_str, ylabel_str, directory, saveas_str)

# Apply the OTFs (FLEX)
# ----------------------------------------------------------------
# First in the ALT direction
toa_img = zeros(toa.shape)
toa2 = zeros(toa.shape)

for iact in range(nu):

    GE = fft(ifftshift( toa[:,iact] ))
    GE_img = GE* otf_v * dv
    E_img = fftshift(ifft(GE_img))
    toa_img[:,iact] = real(E_img)

# Then in the ACT direction
for ialt in range(nv):

    E_slit_u = toa_img[ialt,:]
    GE_slit_u = fft(ifftshift(E_slit_u))

    GE_u = GE_slit_u * otf_u * du # [W/m]

    E_u = fftshift(ifft(GE_u))
    toa2[ialt,:] = real(E_u)

# falta el spatial integration

# Calculate the PSF
# ----------------------------------------------------------------
lsf_u = fftshift(ifft(otf_u))
lsf_v = fftshift(ifft(otf_v))


# LUSS TEST >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Diff and plot
fig = plt.figure(figsize=(10, 7))
plt.plot(real(ifft(otf_u)), '-b',label='real(ifft(otf_u)')
plt.plot(real(ifft(fftshift(otf_u))), '-r',label='real(ifft(fftshift(otf_u)))')
plt.plot(real(fftshift(ifft(fftshift(otf_u)))), '-g',label='real(fftshift(ifft(fftshift(otf_u))))')
plt.title('OFT', fontsize=20)
plt.xlabel('', fontsize=16)
plt.ylabel('OTF [-]', fontsize=16)
plt.grid()
plt.legend()
saveas_str = 'oft_fftshift_real_of' + str(of)
savestr = directory + "/" + saveas_str
plt.savefig(savestr)
plt.close(fig)
print("Saved image " + savestr)

fig = plt.figure(figsize=(10, 7))
plt.plot(imag(ifft(otf_u)), '--b',label='imag(ifft(otf_u)')
plt.plot(imag(ifft(fftshift(otf_u))), '--r',label='imag(ifft(fftshift(otf_u)))')
plt.plot(imag(fftshift(ifft(fftshift(otf_u)))), '--g',label='imag(fftshift(ifft(fftshift(otf_u))))')
plt.title('OFT', fontsize=20)
plt.xlabel('', fontsize=16)
plt.ylabel('OTF [-]', fontsize=16)
plt.grid()
plt.legend()
saveas_str = 'oft_fftshift_imag_of' + str(of)
savestr = directory + "/" + saveas_str
plt.savefig(savestr)
plt.close(fig)
print("Saved image " + savestr)

# Convolve the image with the PSF
# ----------------------------------------------------------------





# Convolve the image with the PSF
# ----------------------------------------------------------------

luss=1



