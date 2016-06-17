from __future__ import division

from scipy import ndimage
from scipy.signal import argrelextrema, savgol_filter, medfilt2d
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from skimage import data, color, io
from skimage.filters import threshold_otsu, threshold_adaptive, rank, gaussian_filter,sobel_v
from skimage.filters.rank import mean_bilateral, autolevel, autolevel_percentile, median
from skimage.morphology import disk, reconstruction, watershed, dilation, rectangle


class Process():

	def __call__(self, *args, **kwargs):
		return self

	def cropImage(self, image, rectShape):
			return image[rectShape[1]:rectShape[3], rectShape[0]:rectShape[2]]

	def backgroundRemoval(self,img):
			bg2 = median(img, rectangle(21,30))
			# io.imshow(bg2)
			# io.show()
			mask = img < bg2 - (255*0.2)
			# io.imshow(np.where(mask, img/255,1))
			# io.show()
			return np.where(mask, img/255,1)

	def computeThresholdImage(self, image):
		thresh = threshold_otsu(image)
		binary = image > thresh
		return binary, thresh

	def newThresholdImage(self, imageOriginal, thresh):
		binary = imageOriginal > thresh
		return binary

	def globalThresholdSelection(self, thresh, img):
		x = []
		y = []
		for i in range(thresh-1, 255, 1):
			labeled, nr_objects = ndimage.label(img > i)
			x.append(i)
			y.append(nr_objects)
		return thresh+np.argmin(np.array(y))

	def binarization(self,image):
		thresImage_res, thres_res = self.computeThresholdImage(image)
		# thresh = self.globalThresholdSelection(int(thres_res),image)
		# img = self.newThresholdImage(image, thresh)
		io.imshow(thresImage_res)
		io.show()
		return thresImage_res

	def edgeDetection(self, image) :
		return sobel_v(image)**2

	def openImageFile(self,path):
		return io.imread(path)

	def saveImage(self, path,name,image):
		io.imsave(path+name,image)
		return 0

	def drawContourDoc(self, image, rect):

		fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
		ax.imshow(image, interpolation='nearest', cmap=plt.cm.gray)
		ax.add_patch(Rectangle((rect[0], rect[1]), rect[2], rect[3], alpha=1,
		                       edgecolor='red', facecolor='none'))
		plt.show()



# img = openImageFile('./title-50.png')
# img2 = openImageFile('./TH-OC-50-052.jpg')
#
# io.imshow(backgroundRemoval(img2))
# io.show()
#
# io.imshow(binarization(img2))
# io.show()

