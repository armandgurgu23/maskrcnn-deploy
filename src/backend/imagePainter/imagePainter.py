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
        for imageIndex, currImage in enumerate(imageList):
            currDrawColor = self.colorSampler()
            currCanvas = ImageDraw.Draw(currImage)
            imagePredData = predictionData[imageIndex]
            # To Do: Complete logic in this function.
            self.drawPredictionsOnCanvas(currCanvas, imagePredData, currDrawColor)
        return

    def drawPredictionsOnCanvas(self, currCanvas, predictionData, currDrawColor):
        predictedBoxes = predictionData[0]
        predictedClasses = predictionData[1]
        for indexPred, currBox in enumerate(predictedBoxes):
            print('Pred index {} has box {}'.format(indexPred, currBox))
            leftCorner = self.extractLeftCornerCoordinates(currBox)
            leftCorner = self.applyPixelShiftToTextCoordinates(leftCorner, self.textPixelShift)
            self.drawBoundingBox(currCanvas, currBox, currDrawColor)
            # predClass = predictedClasses[indexPred]
            # print('Pred index {} has class {}'.format(indexPred, predClass))
            # self.drawPredictedClassForBox(predClass, leftCorner, currCanvas, currDrawColor)
        return

    def applyPixelShiftToTextCoordinates(self, corner, pixelShift):
        return corner[0], corner[1] - pixelShift

    def drawPredictedClassForBox(self, className, textCorner, currCanvas, textColor):
        currCanvas.text(xy=textCorner, text=className, fill=textColor,
                        stroke_width=self.textStrokeWidth)
        return

    def drawBoundingBox(self, currCanvas, box, color):
        currCanvas.rectangle(box, outline=color, width=self.boxWidth)
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
