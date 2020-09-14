import PIL
from PIL import ImageDraw


class ImagePainter(object):
    def __init__(self, boxWidth, textPixelShift, textStrokeWidth, colorChoice):
        self.boxWidth = boxWidth
        self.textPixelShift = textPixelShift
        self.textStrokeWidth = textStrokeWidth
        self.colorChoice = colorChoice
        if self.colorChoice == 'random':
            # Fetch a color sampling method.
            self.colorSampler = self.sampleColorFromColorSpace
        else:
            # We assign a uniform color to
            # be used for drawing.
            self.drawColor = self.colorChoice

    def __call__(self, imageList, predictionData):
        pass

    def sampleColorFromColorSpace(self):
        pass

    def openColorSpaceFromFile(self):
        pass
