from __future__ import division

from scipy import ndimage
from scipy.signal import argrelextrema, savgol_filter, medfilt2d
import numpy as np
from skimage import data, color, io
from skimage.filters import threshold_otsu, threshold_adaptive, rank, gaussian_filter,sobel_v
from skimage.filters.rank import mean_bilateral, autolevel, autolevel_percentile, median
from skimage.morphology import disk, reconstruction, watershed, dilation, rectangle




def cropImage( image, rectShape):
		return image[rectShape[1]:rectShape[3], rectShape[0]:rectShape[2]]

def backgroundRemoval( img):
		bg2 = median(img, rectangle(7,10))
		mask = img < bg2 - (255*0.2)
		return np.where(mask, img/255,1)

def computeThresholdImage(image):
	thresh = threshold_otsu(image)
	binary = image > thresh+25
	return binary, thresh

def newThresholdImage(imageOriginal, thresh):
	binary = imageOriginal > thresh
	return binary

def globalThresholdSelection(thresh, img):
	x = []
	y = []

	for i in range(thresh-1, 255, 1):
		labeled, nr_objects = ndimage.label(img > i)
		x.append(i)
		y.append(nr_objects)

	yhat = np.gradient(np.array(savgol_filter(y,3,1)))
	print('seuil global trouve : ',thresh+np.argmax(np.array(y)))
	return thresh+np.argmin(np.array(y))


def binarization(image):
	thresImage_res, thres_res = computeThresholdImage(image)
	thresh = globalThresholdSelection(int(thres_res),image)
	return newThresholdImage(image, thresh)

def edgeDetection(image) :
	return sobel_v(image)**2

def openImageFile(path):
	return io.imread(path)

def saveImage(path,name, image):
	io.imsave(path+name,image)
	return 0


img = openImageFile('./title-50.png')
img2 = openImageFile('./TH-OC-50-052.jpg')

io.imshow(backgroundRemoval(img2))
io.show()

io.imshow(binarization(img2))
io.show()

