import PIL
from PIL import ImageDraw
import random


class ImagePainter(object):
    def __init__(self, boxWidth, textPixelShift, textStrokeWidth, colorChoice, colorFilePath):
        self.boxWidth = boxWidth
        self.textPixelShift = textPixelShift
        self.textStrokeWidth = textStrokeWidth
        self.colorChoice = colorChoice
        self.colorFilePath = colorFilePath
        # Open the list of colors that can be sampled for drawing.
        if self.colorChoice == 'random':
            # Fetch a color sampling method.
            self.colorSpace = self.openColorSpaceFromFile(self.colorFilePath)
            self.colorSampler = self.sampleColorFromColorSpace
        else:
            # We assign a uniform color to
            # be used for drawing.
            self.colorSpace = self.colorChoice

    def __call__(self, imageList, predictionData):
        self.drawPredictionsOnImages(imageList, predictionData)
        return

    def drawPredictionsOnImages(self, imageList, predictionData):
        for imageIndex, currImage in imageList:
            currDrawColor = self.colorSampler()
            currCanvas = ImageDraw.Draw()
            # To Do: Complete logic in this function.
        pass

    def drawBoxesOnCanvas(self, currCanvas, predictedBoxes):
        pass

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
