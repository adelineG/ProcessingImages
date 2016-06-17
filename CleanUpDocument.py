# from __future__ import *
import os
import csv
import ExtractDocument
import numpy as np
from skimage import data, color, io, img_as_uint
from skimage.filters import threshold_otsu, threshold_adaptive, rank, gaussian_filter
from skimage.filters.rank import mean_bilateral, autolevel, autolevel_percentile
from skimage.morphology import disk, reconstruction


class CleanUpDocument:
	def __init__(self, path):
		self.path = path
		self.pathSave = './crop50_gray/'
		self.extract = ExtractDocument.ExtractDoc()
		# self.filePath = 'C:/Users/E083318N/Documents/ADExCHM/chronologie/docCoord.csv'
		self.filePath = './docCoord-50.csv'
		csvFile = open(self.filePath, 'w')
		self.spamwriter = csv.writer(csvFile, delimiter=' ',
		                             quotechar='|', quoting=csv.QUOTE_MINIMAL)

	def __call__(self, *args, **kwargs):
		return self

	def cropAllDocument(self,image,img):
		# init doc's chape

		self.extract.imageShape = np.shape(image)
		# smooth = autolevel(image.astype(np.uint16), disk(10))

		# binarization
		imageBack = self.extract.process.backgroundRemoval(image)
		# newOriginalImage = self.extract.process.binarization(autolevel(image.astype(np.uint16), disk(10)))

		# compute histogram of pixel using gaussian filter
		self.extract.histogramPixel(gaussian_filter(imageBack, sigma=1))
		# define new coord
		self.extract.computeCoordRect()

		# save data in csv
		self.spamwriter.writerow(
			[img, self.extract.rectShape[0], self.extract.rectShape[1], self.extract.rectShape[2],
			 self.extract.rectShape[3]])
		# save new image
		io.imsave(self.pathSave + img, self.extract.process.cropImage(image,self.extract.rectShape))
		# self.clusterPi.drawContourDoc(image)

	def deleteBackgroundAllDoc(self,image, img):
		imageBack = self.extract.process.backgroundRemoval(image)
		io.imsave(self.pathSave + img, imageBack)

	def binarizationAllDoc(self,image,img):
		# imageBack = self.extract.process.backgroundRemoval(image)
		imageBin = self.extract.process.binarization(image)
		io.imsave(self.pathSave + img, img_as_uint(imageBin))


	def main(self):

		listFile = os.listdir(self.path)

		for img in listFile:

			image = io.imread(self.path + img)
			print(self.path + img)

			# make sure size of image
			if len(np.shape(image)) == 3:
				image = color.rgb2gray(image)

			self.cropAllDocument(image,'crop/'+img)

			# self.deleteBackgroundAllDoc(image,'/back/'+img)



	if __name__ == 'main':
		main()

		# cl = CleanUpDocument('C:/Users/E083318N/Documents/ADExCHM/chronologie/')
		# cl.main()
