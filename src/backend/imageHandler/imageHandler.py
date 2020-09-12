
# Class that is used to read in an image and perform
# the necessary pre-processing to make the image
# compatible with the detector's requirements.
# (ie: scaling to minimum resolution, normalizing
# pixel intensity to 0-1 range etc.)
import os
import PIL
from PIL import Image


class ImageHandler(object):
    def __init__(self, staticPredictions):
        self.staticPredictions = staticPredictions

    def __call__(self, staticPredictionsPath=None, dynamicImagePath=None):
        if self.staticPredictions:
            return self.runStaticPredictionsHandler(staticPredictionsPath)
        else:
            return self.runDynamicPredictionsHandler(dynamicImagePath)

    def runStaticPredictionsHandler(self, staticPredictionsPath):
        imagePaths = self.getImageFilenamesFromPath(staticPredictionsPath)
        imageObjects = self.openImagesFromImageFiles(imagePaths, staticPredictionsPath)
        raise NotImplementedError('Finish code for image handler here!')

    def openImagesFromImageFiles(self, imagePaths, staticPredictionsPath):
        imageObjects = []
        for currImagePath in imagePaths:
            fullImagePath = os.path.join(staticPredictionsPath, currImagePath)
            currImageObject = Image.open(fullImagePath)
            imageObjects.append(currImageObject)
        return imageObjects

    def getImageFilenamesFromPath(self, staticPredictionsPath):
        currPath = os.getcwd()
        os.chdir(staticPredictionsPath)
        allFiles = os.listdir(os.getcwd())
        assert '.DS_Store' not in allFiles, 'Found .DS_Store in list of image files! {}'.format(
            allFiles)
        os.chdir(currPath)
        return allFiles

    def runDynamicPredictionsHandler(self, dynamicImagePath):
        raise NotImplementedError(
            'Revisit this once frontend is implemented for image upload and transmission.')
