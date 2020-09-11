
# Class that is used to read in an image and perform
# the necessary pre-processing to make the image
# compatible with the detector's requirements.
# (ie: scaling to minimum resolution, normalizing
# pixel intensity to 0-1 range etc.)


class ImageHandler(object):
    def __init__(self, staticPredictions):
        self.staticPredictions = staticPredictions

    def __call__(self, staticPredictionsPath=None, dynamicImagePath=None):
        if self.staticPredictions:
            return self.runStaticPredictionsHandler(staticPredictionsPath)
        else:
            return self.runDynamicPredictionsHandler(dynamicImagePath)

    def runStaticPredictionsHandler(self, staticPredictionsPath):
        pass

    def runDynamicPredictionsHandler(self, dynamicImagePath):
        raise NotImplementedError(
            'Revisit this once frontend is implemented for image upload and transmission.')
