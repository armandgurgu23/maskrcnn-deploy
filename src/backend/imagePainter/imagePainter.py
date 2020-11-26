import PIL
from PIL import ImageDraw, ImageFont, ImageOps, Image
import random
from torchvision.transforms import ToPILImage
from imagePainter.maskProcessor.maskProcessor import MaskProcessor


class ImagePainter(object):
    def __init__(self, boxWidth, textPixelShiftWidth, textPixelShiftHeight,
                 textStrokeWidth, colorChoice,
                 colorFilePath, fontSize, fontName, fontRefWidth,
                 applyMaskProcessor, objectTransparencyFactor, processorMethod):
        self.boxWidth = boxWidth
        self.textPixelShiftWidth = textPixelShiftWidth
        self.textPixelShiftHeight = textPixelShiftHeight
        self.textStrokeWidth = textStrokeWidth
        self.colorChoice = colorChoice
        self.colorFilePath = colorFilePath
        self.fontSize = fontSize
        self.applyMaskProcessor = applyMaskProcessor
        self.processorMethod = processorMethod
        self.objectTransparencyFactor = objectTransparencyFactor
        self.fontName = fontName
        self.torchToPILConverter = ToPILImage()
        self.fontRefWidth = fontRefWidth
        # Open the list of colors that can be sampled for drawing.
        if self.colorChoice == 'random':
            # Fetch a color sampling method.
            self.colorSpace = self.openColorSpaceFromFile(self.colorFilePath)
            self.colorSampler = self.sampleColorFromColorSpace
        else:
            # We assign a uniform color to
            # be used for drawing.
            self.colorSpace = self.colorChoice
        if self.applyMaskProcessor:
            self.maskProcessor = MaskProcessor(
                self.objectTransparencyFactor)

    def __call__(self, imageList, predictionData, predictorType):
        if predictorType == 'segmentor':
            return self.drawMaskPredictionsOnImages(imageList, predictionData)
        else:
            return self.drawBoxPredictionsOnImages(imageList, predictionData)

    def drawMaskPredictionsOnImages(self, imageList, predictionData):
        paintedImages = []
        for imageIndex, currImage in enumerate(imageList):
            currDrawColor = self.colorSampler()
            imagePredictions = predictionData[imageIndex]
            currImage = self.drawObjectMasksAndClasses(
                imagePredictions[0], imagePredictions[1], currDrawColor, currImage)
            paintedImages.append(currImage)
        return paintedImages

    def drawObjectMasksAndClasses(self, objectMasks, objectClasses, drawColor, currImage):
        for currMaskIndex in range(objectMasks.size()[0]):
            currObjectMask = objectMasks[currMaskIndex, :, :, :]
            currImage = self.drawObjectMask(
                currObjectMask, currImage, drawColor)
        return currImage

    def drawObjectMask(self, currMask, currImage, drawColor):
        currMaskPIL = self.transformMaskToPILImage(currMask)
        coloredMask = self.applyColorToObjectMask(currMaskPIL, drawColor)
        transparencyMask = self.deriveTransparencyMapFromMask(
            currMask, self.processorMethod)
        return self.blendImageAndColoredObjectMask(currImage, coloredMask, transparencyMask)

    def blendImageAndColoredObjectMask(self, currImage, coloredMask, transparencyMask):
        # Performs alpha blending using specified transparency mask.
        return Image.composite(currImage, coloredMask, transparencyMask)

    def deriveTransparencyMapFromMask(self, currMask, processorMethod):
        if hasattr(self, 'maskProcessor'):
            transparencyMask = self.maskProcessor(currMask, processorMethod)
        else:
            transparencyMask = currMask
        transparencyMask = self.transformMaskToPILImage(transparencyMask)
        return transparencyMask

    def applyColorToObjectMask(self, currMask, drawColor):
        # We can set the pixels corresponding to the background pixels
        # in the object mask to any color since our aim is for those
        # regions to be opaque in the alpha blending process.
        return ImageOps.colorize(currMask, black='white', white=drawColor)

    def transformMaskToPILImage(self, currMask):
        return self.torchToPILConverter(currMask)

    def initializeTextFontConfig(self, fontName, fontSize):
        return ImageFont.truetype(fontName, fontSize)

    def computeDynamicTextFontConfig(self, fontName, fontSize, fontRefWidth, imageWidth):
        # Code to setup the text font object settings was borrowed from here:
        # https://stackoverflow.com/questions/4902198/pil-how-to-scale-text-size-in-relation-to-the-size-of-the-image
        scaledFontSize = int((imageWidth * fontSize) / fontRefWidth)
        return self.initializeTextFontConfig(fontName, scaledFontSize)

    def drawBoxPredictionsOnImages(self, imageList, predictionData):
        for imageIndex, currImage in enumerate(imageList):
            imageResolution = currImage.size
            currDrawColor = self.colorSampler()
            currCanvas = ImageDraw.Draw(currImage)
            imagePredData = predictionData[imageIndex]
            # To Do: Complete logic in this function.
            self.drawPredictionsOnCanvas(
                currCanvas, imagePredData, currDrawColor, imageResolution)
        return imageList

    def drawPredictionsOnCanvas(self, currCanvas, predictionData, currDrawColor, currResolution):
        predictedBoxes = predictionData[0]
        predictedClasses = predictionData[1]
        for indexPred, currBox in enumerate(predictedBoxes):
            leftCorner = self.extractLeftCornerCoordinates(currBox)
            leftCorner = self.applyPixelShiftToTextCoordinates(
                leftCorner, self.textPixelShiftHeight, self.textPixelShiftWidth, currResolution)
            self.drawBoundingBox(currCanvas, currBox,
                                 currDrawColor, currResolution)
            predClass = predictedClasses[indexPred]
            # print('Pred index {} has class {}'.format(indexPred, predClass))
            fontObject = self.computeDynamicTextFontConfig(
                fontName=self.fontName, fontSize=self.fontSize, fontRefWidth=self.fontRefWidth, imageWidth=currResolution[0])
            self.drawPredictedClassForBox(
                predClass, leftCorner, currCanvas, currDrawColor, currResolution, fontObject)
        return

    def applyPixelShiftToTextCoordinates(self, corner, pixelShiftHeight, pixelShiftWidth, currResolution):
        yCoordinateShift = int(currResolution[1] * pixelShiftHeight)
        xCoordinateShift = int(currResolution[0] * pixelShiftWidth)
        return corner[0] - xCoordinateShift, corner[1] - yCoordinateShift

    def drawPredictedClassForBox(self, className, textCorner, currCanvas, textColor, currResolution, fontConfig):
        scaledStrokeWidth = int(currResolution[0] * self.textStrokeWidth)
        currCanvas.text(xy=textCorner, text=className, fill=textColor,
                        stroke_width=scaledStrokeWidth, font=fontConfig)
        return

    def drawBoundingBox(self, currCanvas, box, color, currResolution):
        scaledBoxWidth = int(currResolution[0] / self.boxWidth)
        currCanvas.rectangle(box, outline=color, width=scaledBoxWidth)
        return

    def extractLeftCornerCoordinates(self, box):
        # Returned as a (x,y) tuple.
        return box[0], box[1]

    def sampleColorFromColorSpace(self):
        return random.choice(self.colorSpace)

    def openColorSpaceFromFile(self, colorPath):
        allColors = []
        with open(colorPath, 'r') as colorFile:
            for currColor in colorFile:
                currColor = currColor.strip('\n')
                allColors.append(currColor)
        return allColors

    def showImages(self, imageList):
        for currImage in imageList:
            currImage.show()
        return
