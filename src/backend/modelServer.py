from maskRCNN.modelWrapper import MaskRCNNModelWrapper
from maskRCNN.config.modelDefaults import getModelYamlConfig
from imagePainter.config.painterDefaults import getPainterYamlConfig
from imageHandler.imageHandler import ImageHandler
from imagePainter.imagePainter import ImagePainter
import io
# Not a real server. Just a wrapper to handle serving predictions
# in the application server.


class ModelServer(object):
    def __init__(self):
        self.detectorConfig, self.painterConfig = self.getModelConfigurations()
        self.detectorWrapper = self.initializeDetectorWrapper(self.detectorConfig)
        self.imageHandlerWrapper = self.initializeImageHandlerWrapper(self.detectorConfig)
        self.imagePainterWrapper = self.initializeImagePainterWrapper(self.painterConfig)
        print('Object detection model ready for serving!')

    def __call__(self, imageFileObject, imageExtension, predictorType):
        uploadedImage = self.imageHandlerWrapper(dynamicImagePath=imageFileObject)
        predictionData = self.detectorWrapper(
            uploadedImage, self.detectorConfig.detectorModel.confidenceThreshold, predictorType)
        uploadedImage = self.imageHandlerWrapper.transformTorchImageToPIL(uploadedImage)
        # To do: Add ability to draw predicted class name.
        self.imagePainterWrapper(uploadedImage, predictionData)
        # Helpful method to visualize predictions on the backend side.
        # self.imagePainterWrapper.showImages(uploadedImage)
        return self.serializeImageToResponseByteString(uploadedImage, imageExtension)
    
    def serializeImageToResponseByteString(self, uploadedImage, extension):
        # io.BytesIO() can be used to stream any non-text
        # data. The input data to BytesIO must be a byte-string.
        imageBuffer = io.BytesIO()
        uploadedImage[0].save(imageBuffer, format=extension)
        # Apparently seek(0) is needed if you are using PIL/Skimage.
        # https://stackoverflow.com/questions/55873174/how-do-i-return-an-image-in-fastapi/55905051#55905051
        imageBuffer.seek(0)
        return imageBuffer

    def getModelConfigurations(self):
        detectorConfig = getModelYamlConfig()
        painterConfig = getPainterYamlConfig()
        return detectorConfig, painterConfig

    def initializeDetectorWrapper(self, detectorConfig):
        return MaskRCNNModelWrapper(
            pretrained=detectorConfig.detectorModel.pretrained,
            minSize=detectorConfig.detectorModel.minSize,
            classesPath=detectorConfig.detectorModel.predictionClassesPath,
            applyMaskProcessor=detectorConfig.segmentorModel.applyMaskProcessor)

    def initializeImageHandlerWrapper(self, detectorConfig):
        return ImageHandler(
            staticPredictions=detectorConfig.detectorModel.staticPredictions)

    def initializeImagePainterWrapper(self, painterConfig):
        return ImagePainter(boxWidth=painterConfig.imagePainter.boxWidth,
                            textPixelShiftWidth=painterConfig.imagePainter.textPixelShiftWidth,
                            textPixelShiftHeight=painterConfig.imagePainter.textPixelShiftHeight,
                            textStrokeWidth=painterConfig.imagePainter.textStrokeWidth,
                            colorChoice=painterConfig.imagePainter.colorChoice,
                            colorFilePath=painterConfig.imagePainter.colorFile,
                            fontSize=painterConfig.imagePainter.fontSize,
                            fontName=painterConfig.imagePainter.fontName,
                            fontRefWidth=painterConfig.imagePainter.fontRefWidth)
