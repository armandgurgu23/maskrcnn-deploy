
# Class that is used to read in an image and perform
# the necessary pre-processing to make the image
# compatible with the detector's requirements.
# (ie: scaling to minimum resolution, normalizing
# pixel intensity to 0-1 range etc.)
import os
import PIL
from PIL import Image
import torchvision
from torchvision import transforms


class ImageHandler(object):
    def __init__(self, staticPredictions):
        self.staticPredictions = staticPredictions
        self.imagePreprocessor = self.initializeImageTransformer()

    def initializeImageTransformer(self):
        return transforms.Compose(self.getImageTransforms())

    def getImageTransforms(self):
        transformsArray = []
        transformsArray.append(self.getPILImageToTorchTensorTransform())
        # To do: Add other image transforms later if different vision
        # models require them. (add below)
        return transformsArray

    def getPILImageToTorchTensorTransform(self):
        # This transform converts a PIL Image object
        # to a torch.Tensor and normalizes pixel intensities
        # to [0,1] range.
        return transforms.ToTensor()

    def __call__(self, staticPredictionsPath=None, dynamicImagePath=None):
        if self.staticPredictions:
            return self.runStaticPredictionsHandler(staticPredictionsPath)
        else:
            return self.runDynamicPredictionsHandler(dynamicImagePath)

    def runStaticPredictionsHandler(self, staticPredictionsPath):
        imagePaths = self.getImageFilenamesFromPath(staticPredictionsPath)
        imageObjects = self.openImagesFromImageFiles(imagePaths, staticPredictionsPath)
        imageObjects = self.preprocessPILImages(imageObjects)
        return imageObjects

    def runDynamicPredictionsHandler(self, dynamicImagePath):
        raise NotImplementedError(
            'Revisit this once frontend is implemented for image upload and transmission.')

    def preprocessPILImages(self, imageObjects):
        processedImages = []
        for currImage in imageObjects:
            currProcessedImage = self.imagePreprocessor(currImage)
            processedImages.append(currProcessedImage)
        return processedImages

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

    def transformTorchImageToPIL(self, imageArrayTorch):
        imageArrayPil = []
        pilImageMapper = transforms.ToPILImage()
        for currImage in imageArrayTorch:
            imageArrayPil.append(pilImageMapper(currImage))
        return imageArrayPil
