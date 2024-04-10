import cv2
import skimage.io as io
import matplotlib.pyplot as plt
import numpy as np
from skimage.exposure import histogram, equalize_hist
from matplotlib.pyplot import bar
from skimage.color import rgb2gray,rgb2hsv,hsv2rgb,rgba2rgb
from skimage.transform import hough_line, hough_line_peaks

from scipy.signal import convolve2d
from scipy import fftpack
import math

from skimage.util import random_noise
from skimage.filters import median, sobel_h, sobel, sobel_v,roberts, prewitt, gaussian
from skimage.feature import canny

from skimage.morphology import binary_erosion, binary_dilation, binary_closing,skeletonize, thin, dilation

from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

# Shows the images with their titles
def show_images(images,titles=None):
    n_ims = len(images)
    if titles is None: titles = ['(%d)' % i for i in range(1,n_ims + 1)]
    fig = plt.figure()
    n = 1
    for image,title in zip(images,titles):
        a = fig.add_subplot(1,n_ims,n)
        if image.ndim == 2: 
            plt.gray()
        plt.imshow(image)
        a.set_title(title)
        n += 1
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_ims)
    plt.show() 

# Show the histogram of the image
def show_hist(img):
    plt.figure()
    imgHist = histogram(img, nbins=256)
    bar(imgHist[1].astype(np.uint8), imgHist[0], width=0.8, align='center')

# Reads the image from the path
def read_image(image_path):
    image = io.imread(image_path)
    return image

# Shows one image
def show_image(image):
    io.imshow(image)
    io.show()


