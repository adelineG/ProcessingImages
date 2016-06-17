import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.signal import argrelextrema, argrelmin
from skimage import data, color, io
from skimage.filters import threshold_otsu, threshold_adaptive, rank, gaussian_filter
from skimage.filters.rank import mean_bilateral, autolevel, autolevel_percentile
from skimage.morphology import disk, reconstruction, rectangle

import preproccess

class ExtractDoc:
	def __init__(self):
		self.test = True
		# self.path = 'C:/Users/E083318N/Documents/ADExCHM/chronologie'
		self.imageShape = []
		self.rectShape = []
		self.process = preproccess.Process()

	def __call__(self, *args, **kwargs):
		"""

		:type self: object
		"""
		return self

	def histogramPixel(self, image):
		self.vectX = np.sum(image, axis=1)
		self.vectY = np.sum(image, axis=0)


	def horizontalHistogramPixel(self, image):
		self.vectY = np.sum(image, axis=0)

	def verticalHistogramPixel(self, image):
		self.vectX = np.sum(image, axis=1)


	# http://scikit-image.org/docs/dev/auto_examples/color_exposure/plot_regional_maxima.html#example-color-exposure-plot-regional-maxima-py
	def dilatedImage(self, image):
		h = 0.4
		image = gaussian_filter(image, 1)

		seed = np.copy(image)
		seed[1:-1, 1:-1] = image.min()
		mask = image

		seed = image - h
		dilated = reconstruction(seed, mask, method='dilation')
		hdome = image - dilated
		return hdome, mask

	def displayRes(self, image, thres_res, newOriginalImage):
		fig = plt.figure(figsize=(8, 2.5))
		ax1 = plt.subplot(1, 3, 1, adjustable='box-forced')
		ax2 = plt.subplot(1, 3, 2)
		ax3 = plt.subplot(1, 3, 3, sharex=ax1, sharey=ax1, adjustable='box-forced')

		ax1.imshow(image, cmap=plt.cm.gray)
		ax1.set_title('Original')
		ax1.axis('off')

		ax2.hist(image)
		ax2.set_title('Histogram')
		ax2.axvline(thres_res, color='r')

		ax3.imshow(newOriginalImage, cmap=plt.cm.gray)
		ax3.set_title('Thresholded')
		ax3.axis('off')

		plt.show()

	## redo !!!!!
	def searchExtrema(self, vect, i, inv, ind1, ind2, imageShape, rectShape, lim):
		tmp = []
		min = argrelextrema(vect, np.less, order=150)
		ind = ind1
		limit = imageShape[i] * ind

		for a in min[0]:
			if vect[a] < limit:
				tmp.append(a)

		# print('----1----- ',min, vect[min], ' limit = ',limit, tmp, vect.mean())
		if len(tmp) == 0:
			# print(min, vect[min], limit, tmp, vect.mean())

			limitExtrem = ((vect.mean() - limit) / 2) + limit

			for a in min[0]:
				if vect[a] < limitExtrem:
					tmp.append(a)

		elif len(tmp) > 2:
			ind = ind2
			# if i == 1:
			# 	ind = ind2
			# else:
			# 	ind = ind2
			# limit = imageShape[i] * ind
			tmp = []

			for a in min[0]:
				# print('zzzzzz ++++ ', not(imageShape[inv] * (1-ind) < a <imageShape[inv] * ind), vect[a] < limit,  vect[a], limit, imageShape[inv] * (1-ind), imageShape[inv] * ind)
				if vect[a] < limit and not (imageShape[inv] * (1-ind)< a < imageShape[inv] * ind):
					# print(a)
					tmp.append(a)

		# print('----2----- ',min, vect[min], limit, tmp, vect.mean())
		# suivant si la valeur est plus près d un bout que de l autre on adapte la taille du rectangle
		if len(tmp) == 1:
			if tmp[0] >= (imageShape[inv] - tmp[0]) and imageShape[inv] - tmp[0] < imageShape[inv] * lim:
				rectShape[i + 2] = tmp[0] - rectShape[i]
			elif tmp[0] < imageShape[inv] * lim:
				rectShape[i] = tmp[0]

		elif len(tmp) == 2:
			if tmp[0] < (imageShape[inv] - tmp[0]) and tmp[0] < imageShape[inv] * lim:
				rectShape[i] = tmp[0]
			if tmp[1] > (imageShape[inv] - tmp[1]) and imageShape[inv] - tmp[1] < imageShape[inv] * lim:
				rectShape[i + 2] = tmp[1] - rectShape[i]

		return rectShape

	def computeCoordRect(self):

		# initialisation du rectangle avec les coodonnees de l image
		self.rectShape = [0, 0, self.imageShape[1], self.imageShape[0]]

		# recherche des minimum locaux sur une distance de 200 pixels de séparation
		self.rectShape = self.searchExtrema(self.vectX, 1, 0, 0.850, 0.75, self.imageShape, self.rectShape, 0.1)
		self.rectShape = self.searchExtrema(self.vectY, 0, 1, 0.850, 0.75, self.imageShape, self.rectShape, 0.1)



try:

	clusterImg = ExtractDoc()

	print(clusterImg.path + '/TH-OC-50-222.jpeg')
	image = io.imread(clusterImg.path + '/TH-OC-50-222.jpg')
	clusterImg.imageShape = np.shape(image)
	smooth = autolevel(image.astype(np.uint16), disk(10))

	thresImage_res, thres_res = clusterImg.computeThresholdImage(smooth)
	newOriginalImage = clusterImg.newThresholdImage(image, thres_res)

	# détection de la page dans le document
	clusterImg.histogramPixel(gaussian_filter(newOriginalImage, sigma=1))
	clusterImg.computeCoordRect()
	#clusterImg.drawContourDoc(image, clusterImg.rectShape)



except:
	print('fail !!!!')
