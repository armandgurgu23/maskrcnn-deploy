

class MaskProcessor(object):
    def __init__(self, transparencyFactor, processorMethod):
        self.transparencyFactor = transparencyFactor
        self.processorMethod = processorMethod
    
    def __call__(self, objectMask):
        # Returns a new object transparency mask by applying
        # a processor method to the predicted object mask.
        print(objectMask)
        raise NotImplementedError('Add the transparency transformation code here!')

