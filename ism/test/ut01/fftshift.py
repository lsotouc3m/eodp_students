
# Understand the use of fftshift and ifftshift
# https://uk.mathworks.com/matlabcentral/fileexchange/25473-why-use-fftshift-fft-fftshift-x-in-matlab-instead-of-fft-x

# CONCLUSION:
# fftshift is necessary so that the fft is nice and positive (and not alternating positive and negative values)
# fftshift is the same than ifftshift when there are an EVEN number of frequency points
# We need an EVEN number of frequency values so that the fft is real (imag part negligible).

from numpy.fft import fft, fftshift, ifftshift, ifft
from numpy import real, zeros, imag, arange, abs, sqrt, exp
from math import pi, log
import matplotlib.pyplot as plt


# Inputs
# ----------------------------------------------------------------
directory = '/home/luss/EODP/eodp/ism/test/ut01/output'

Bx = 50
A = sqrt(log(2))/(2*pi*Bx)
fs = 451# 500 (even) 451 (odd) #sampling frequency
dt = 1/fs #time step
T=1 #total time window
t = arange(-T/2,T/2,dt) #time grids
df = 1/T #freq step
Fmax = 1/2/dt #freq window
f=arange(-Fmax,Fmax,df) #freq grids, not used in our examples, could be used by plot(f, X)

# Try FFT with fftshift
# ----------------------------------------------------------------
x = exp(-t**2/(2*A*A))
Xan = A*sqrt(2*pi)*exp(-2*(pi*f*A)*(pi*f*A)) #X(f), analytical Fourier transform of x(t), real
Xfft = dt * fft(x) #directly using fft()
print('Imaginary part of Xfft: ' + str(max(imag(Xfft))))

Xfftshift = dt * fft(fftshift(x)) #using fftshift() before fft()
print('Imaginary part of Xfftshift: ' + str(max(imag(Xfftshift))))
# The fftshift basically moves the centre of the spectrum to the fist indexes

Xfinal = dt * fftshift(fft(ifftshift(x))) #identical with analytical X(f), also note dt
print('The imaginary part is negligible Xfinal: ' + str(max(imag(Xfinal))))
# -> CORRECT fftshift(fft(ifftshift(x))).
# The fftshift(fft(fftshift(x))) gives the same result for even number of values in x, but not for odd

# Diff and plot
fig = plt.figure(figsize=(10, 7))
plt.plot(f,real(Xfft), '--y', label='real(Xfft)')
plt.plot(f,real(Xfftshift), '--c', label='real(Xfftshift)')
plt.plot(f,Xan, '-r', label='analitical FT')
plt.plot(f,real(Xfinal), '--k', label='real(Xfinal)')

plt.title('FFT with fftshift and ifftshift', fontsize=20)
plt.xlabel('Frequency [m-1]', fontsize=16)
plt.ylabel('X(f) [-]', fontsize=16)
plt.grid()
plt.legend()
saveas_str = 'fftshift_n' + str(f.size)
savestr = directory + "/" + saveas_str
plt.savefig(savestr)
plt.close(fig)
print("Saved image " + savestr)

# Do fftshift analytically
# ----------------------------------------------------------------

Xfft = dt * fft(x) #directly using fft()

aux=zeros(x.size)
for ii in range(aux.size):
    aux[ii] = (-1)**ii

Xfftshift = dt * fft(fftshift(x)) #using fftshift() before fft()
Xifftshift = dt * fft(ifftshift(x)) # EQUAL if x is even. Not equal if x is odd.
Xfftaux = dt * fft(x)*aux # EQUAL

Xfinal = dt * fftshift(fft(ifftshift(x))) #identical with analytical X(f), also note dt
Xfinal2 = dt * fft(x)*aux #identical with analytical X(f), also note dt

# Diff and plot
fig = plt.figure(figsize=(10, 7))
plt.plot(f,real(Xfinal), '--k', label='real(Xfinal)')
plt.plot(f,real(Xfinal2), '--c', label='real(Xfinal2)')
plt.title('FFT with fftshift and ifftshift', fontsize=20)
plt.xlabel('Frequency [m-1]', fontsize=16)
plt.ylabel('X(f) [-]', fontsize=16)
plt.grid()
plt.legend()
saveas_str = 'fftshift_Xfinal_n' + str(f.size)
savestr = directory + "/" + saveas_str
plt.savefig(savestr)
plt.close(fig)
print("Saved image " + savestr)

# Diff and plot
fig = plt.figure(figsize=(10, 7))
plt.plot(f,x, '-k', label='x')
plt.plot(f,fftshift(x), '-r', label='fftshift(x)')
plt.plot(f,ifftshift(x), '-c', label='ifftshift(x)')
plt.title('fftshift and ifftshift', fontsize=20)
plt.xlabel('Frequency [m-1]', fontsize=16)
plt.ylabel('[-]', fontsize=16)
plt.grid()
plt.legend()
saveas_str = 'fftshift2_n' + str(f.size)
savestr = directory + "/" + saveas_str
plt.savefig(savestr)
plt.close(fig)
print("Saved image " + savestr)

# Diff and plot
fig = plt.figure(figsize=(10, 7))
plt.plot(f,real(fft(fftshift(x))), '-r', label='real(fft(fftshift(x)))')
plt.plot(f,real(fft(ifftshift(x))), '-c', label='real(fft(ifftshift(x)))')
plt.plot(f,imag(fft(fftshift(x))), '--r', label='imag(fft(fftshift(x)))')
plt.plot(f,imag(fft(ifftshift(x))), '--c', label='imag(fft(ifftshift(x)))')
# plt.plot(f,real(fft(x)), '--y', label='fft(x)')
plt.title('Real part FFT of fftshift and ifftshift', fontsize=20)
plt.xlabel('Frequency [m-1]', fontsize=16)
plt.ylabel('[-]', fontsize=16)
plt.grid()
plt.legend()
saveas_str = 'fftshift3_n' + str(f.size)
savestr = directory + "/" + saveas_str
plt.savefig(savestr)
plt.close(fig)
print("Saved image " + savestr)






luss=1
