
# Test the effect of a filter on an image.
# Based on https://en.wikipedia.org/wiki/Kernel_(image_processing)

import imageio
import matplotlib.pyplot as plt
import numpy as np
from numpy import zeros
from scipy.ndimage.filters import convolve

# Inputs
# ---------------------------------------------------------------------------------
# Full path to input image
lenna = 'Lenna.png'

# output directory
outputdir = '/home/luss/EODP/eodp/ism/test/ut01/output'

# Kernel
k_identity = np.array([[0,0,0],
                       [0,1,0],
                       [0,0,0]])

k_edge = np.array([[+1, 0,-1],
                   [ 0, 0, 0],
                   [-1, 0,+1]])

k_edge2 = np.array([[-1,-1,-1],
                    [-1, 8,-1],
                    [-1,-1,-1]])

k_sharp = np.array([[0,-1,0],
                    [-1,5,-1],
                    [0,-1,0]])

k_box_blur = 1/9*np.array([[1,1,1],
                           [1,1,1],
                           [1,1,1]])

k_gauss_blur = 1/256*np.array([[1,4,6,4,1],
                               [4,16,24,16,4],
                               [6,24,36,24,6],
                               [4,16,24,16,4],
                               [1,4,6,4,1]])

k_gauss_unsharp = -1/256*np.array([[1,4,6,4,1],
                                   [4,16,24,16,4],
                                   [6,24,-476,24,6],
                                   [4,16,24,16,4],
                                   [1,4,6,4,1]])

# Aux
# ---------------------------------------------------------------------------------
def plotImage(im2d, cmap_str, name_str):
    fig, ax = plt.subplots(figsize=(7,7))
    pos = ax.imshow(im2d, cmap=cmap_str)
    fig.colorbar(pos, ax=ax)# add the colorbar
    plt.savefig(outputdir + '/' + name_str)
    plt.close(fig)
    print("Figure saved: " + outputdir + '/' + name_str)

def applyfilter(im, k):
    im_conv = zeros(im.shape)

    if (len(im.shape)==3):
        for kk in range(im.shape[2]): #RGB
            im_conv[:,:,kk] = convolve(im[:,:,kk], k, mode='constant', cval=0.0)

    else: # 2D
        im_conv = convolve(im, k, mode='constant', cval=0.0)

    return im_conv


# Read Lenna
# ---------------------------------------------------------------------------------

im = imageio.imread(lenna)
print("Shape Lenna " + str(im.shape))
# def f(x):
#     return np.float(x)
# f2 = np.vectorize(f)
# im = f2(im)

# Natural colour image:
plotImage(im, 'jet', 'Lenna_natural.png')

# RGB
im_red = im[:, :, 0]
# im_gre = im[:, :, 1]
# im_blu = im[:, :, 2]

# Slice
plotImage(im_red, 'Reds_r', 'Lenna_red.png')
# plotImage(im_gre, 'Greens_r', 'Lenna_green.png')
# plotImage(im_blu, 'Blues_r', 'Lenna_blue.png')

# Filter
# ---------------------------------------------------------------------------------
# Apply convolution
# convolve(test, k_identity, mode='constant', cval=0.0)
im_red_conv = convolve(im_red, k_edge, mode='constant', cval=0.0)
plotImage(im_red_conv, 'Reds_r', 'Lenna_red_edge.png')

im_red_conv = convolve(im_red, k_edge2, mode='constant', cval=0.0)
plotImage(im_red_conv, 'Reds_r', 'Lenna_red_edge2.png')

# Sharpen
im_sharp = applyfilter(im_red, k_sharp)
plotImage(im_sharp, 'Reds_r', 'Lenna_red_sharp.png')

# Box blur
im_box_blur = applyfilter(im_red, k_box_blur)
plotImage(im_box_blur, 'Reds_r', 'Lenna_red_box_blur.png')

# Gaussian blur
im_gauss_blur = applyfilter(im_red, k_gauss_blur)
plotImage(im_gauss_blur, 'Reds_r', 'Lenna_red_gauss_blur.png')

# Gaussian unsharpening
im_gauss_unsharp = applyfilter(im_red, k_gauss_unsharp)
plotImage(im_gauss_unsharp, 'Reds_r', 'Lenna_red_gauss_unsharp.png')

# Apply the sharpening to the previously blurred image and see if we
# get the original image
im_retrieved = applyfilter(im_gauss_blur, k_gauss_unsharp)
plotImage(im_retrieved, 'Reds_r', 'Lenna_red_gauss_retrieved.png')

im_diff = im_retrieved - im_red
plotImage(im_diff, 'Reds_r', 'Lenna_red_gauss_retrieved_diff.png')

histo=np.histogram(im_diff, bins=10)

# Diff and plot
fig = plt.figure(figsize=(20,10))
plt.plot(histo[1][0:-1], histo[0])
plt.title("Histogram of the retrieved differences", fontsize=20)
plt.xlabel('[DN]', fontsize=16)
# plt.ylabel(ylabel_str, fontsize=16)
plt.grid()
saveas_str = "Lenna_red_gauss_retrieved_histo"
savestr = outputdir + "/" + saveas_str
plt.savefig(savestr)
plt.close(fig)
print("Saved image " + savestr)

# Se va de rango 0-255:
# Edge
# im_edge = applyfilter(im, k_edge)
# plotImage(im_edge, 'jet', 'Lenna_edge.png')
#
# # Sharpen
# im_sharp = applyfilter(im, k_sharp)
# plotImage(im_sharp, 'jet', 'Lenna_sharp.png')
#
# # Gaussian blur
# im_gauss_blur = applyfilter(im, k_gauss_blur)
# plotImage(im_gauss_blur, 'jet', 'Lenna_gauss_blur.png')

luss=1
