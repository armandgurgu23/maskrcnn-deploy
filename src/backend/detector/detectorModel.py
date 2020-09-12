import torchvision.models as models


class MaskRCNNModelWrapper(object):
    def __init__(self, pretrained, classesPath, minSize=400):
        self.pretrained = pretrained
        self.minSize = minSize
        self.classesPath = classesPath
        # Get the list of prediction classes for mapping the prediction
        # indexes to the semantic class name.
        self.classesArray = self.getModelPredictionClasses(self.classesPath)
        self.maskRCNNModel = self.initializeMaskRCNNModel(self.pretrained, self.minSize)
        # Set the pretrained model in inference mode since model
        # uses batch normalization.
        self.maskRCNNModel.eval()
        print('Finished initializing mask rcnn object detector!')

    def __call__(self, predictImage):
        # Call method for now returns raw predictions. Adjust
        # output format later.
        rawPredictions = self.maskRCNNModel(predictImage)
        print(rawPredictions)
        print('\nThe raw predictions are above!\n')
        print(self.classesArray)
        print('\n\nThe vocabulary is shown above!\n\n')
        raise NotImplementedError('Barrier to output! Add predictions processing handler.')
        # return

    def initializeMaskRCNNModel(self, pretrained, minSize):
        return models.detection.maskrcnn_resnet50_fpn(pretrained=pretrained, min_size=minSize)

    def getModelPredictionClasses(self, classesPath):
        # Used to initialize a list of classes that the mask-rcnn
        # model supports. This is used to map the prediction indexes
        # of the mask-rcnn model to its semantic class names.
        # (ie: index 1 --> person class).
        classesArray = []
        with open(classesPath, 'r') as classesFile:
            for currLine in classesFile:
                currLine = currLine.strip('\n')
                classesArray.append(currLine)
        return classesArray
