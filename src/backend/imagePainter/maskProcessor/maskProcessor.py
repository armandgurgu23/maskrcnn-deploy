

class MaskProcessor(object):
    def __init__(self, transparencyFactor):
        self.transparencyFactor = transparencyFactor
        self.transparencyHandlers = {'constantScaling': self.applyConstantScalingToObjectMaskHandler,
                                     'padConstant': self.padConstantToObjectMaskHandler}

    def __call__(self, objectMask, processorMethod):
        # Returns a new object transparency mask by applying
        # a processor method to the predicted object mask.
        handlerToApply = self.transparencyHandlers[processorMethod]
        return handlerToApply(objectMask)

    def applyConstantScalingToObjectMaskHandler(self, objectMask):
        # We will try a scaling of the form factor * x where
        # x represents non-zero intensities.
        raise NotImplementedError('Insert log')

    def padConstantToObjectMaskHandler(self, objectMask):
        objectMask[objectMask > 0.0] = self.transparencyFactor
        objectMask[objectMask == 0.0] = 1.0
        return objectMask
