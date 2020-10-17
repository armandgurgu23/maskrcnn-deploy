from detector.detectorModel import MaskRCNNModelWrapper
from detector.config.detectorDefaults import getDetectorYamlConfig
from imagePainter.config.painterDefaults import getPainterYamlConfig
from imageHandler.imageHandler import ImageHandler
from imagePainter.imagePainter import ImagePainter

# Not a real server. Just a wrapper to handle serving predictions
# in the application server.


class ModelServer(object):
    def __init__(self):
        self.detectorConfig, self.painterConfig = self.getModelConfigurations()
        self.detectorWrapper = self.initializeDetectorWrapper(self.detectorConfig)
        self.imageHandlerWrapper = self.initializeImageHandlerWrapper(self.detectorConfig)
        self.imagePainterWrapper = self.initializeImagePainterWrapper(self.painterConfig)
        print('Object detection model ready for serving!')

    def __call__(self, imageFileObject):
        uploadedImage = self.imageHandlerWrapper(dynamicImagePath=imageFileObject)
        predictionData = self.detectorWrapper(
            uploadedImage, self.detectorConfig.detectorModel.confidenceThreshold)
        uploadedImage = self.imageHandlerWrapper.transformTorchImageToPIL(uploadedImage)
        # To do: Add ability to draw predicted class name.
        self.imagePainterWrapper(uploadedImage, predictionData)
        self.imagePainterWrapper.showImages(uploadedImage)
        # To do: add a way to map the PIL Image object back to a file-like
        # object before returning.
        return uploadedImage

    def getModelConfigurations(self):
        detectorConfig = getDetectorYamlConfig()
        painterConfig = getPainterYamlConfig()
        return detectorConfig, painterConfig

    def initializeDetectorWrapper(self, detectorConfig):
        return MaskRCNNModelWrapper(
            pretrained=detectorConfig.detectorModel.pretrained,
            minSize=detectorConfig.detectorModel.minSize,
            classesPath=detectorConfig.detectorModel.predictionClassesPath)

    def initializeImageHandlerWrapper(self, detectorConfig):
        return ImageHandler(
            staticPredictions=detectorConfig.detectorModel.staticPredictions)

    def initializeImagePainterWrapper(self, painterConfig):
        return ImagePainter(boxWidth=painterConfig.imagePainter.boxWidth,
                            textPixelShift=painterConfig.imagePainter.textPixelShift,
                            textStrokeWidth=painterConfig.imagePainter.textStrokeWidth,
                            colorChoice=painterConfig.imagePainter.colorChoice,
                            colorFilePath=painterConfig.imagePainter.colorFile)
