import torchvision.models as models


class MaskRCNNModelWrapper(object):
    def __init__(self, pretrained, classesPath, minSize=400):
        self.pretrained = pretrained
        self.minSize = minSize
        self.classesPath = classesPath
        # Get the list of prediction classes for mapping the prediction
        # indexes to the semantic class name.
        self.classesArray = self.getModelPredictionClasses(self.classesPath)
        self.maskRCNNModel = self.initializeMaskRCNNModel(
            self.pretrained, self.minSize)
        # Set the pretrained model in inference mode since model
        # uses batch normalization.
        self.maskRCNNModel.eval()
        print('Finished initializing mask rcnn object detector!')

    def __call__(self, predictImage, confidenceThreshold, predictorType):
        # Call method for now returns raw predictions. Adjust
        # output format later.
        rawPredictions = self.maskRCNNModel(predictImage)
        return self.extractValidPredictions(rawPredictions, confidenceThreshold, predictorType)

    def extractValidPredictions(self, rawPredictions, confidenceThreshold, predictorType):
        # A valid prediction is defined as a prediction whose
        # confidence score is greater than the confidenceThreshold
        # hyperparameter.
        validPredictionData = []
        if predictorType == "segmentor":
            return self.extractMasksAndLabels(validPredictionData, rawPredictions, confidenceThreshold)
        else:
            return self.extractBoxesAndLabels(validPredictionData, rawPredictions, confidenceThreshold)

    def extractMasksAndLabels(self, validPredictionData, rawPredictions, confidenceThreshold):
        if len(rawPredictions) == 1:
            singlePredictionData = self.extractSingleInstanceBoxesAndLabels(
                rawPredictions[0], confidenceThreshold, 'masks')
            validPredictionData.append(singlePredictionData)
            return validPredictionData
        elif len(rawPredictions) > 1:
            for currPrediction in rawPredictions:
                currPredictionData = self.extractSingleInstanceBoxesAndLabels(
                    currPrediction, confidenceThreshold, 'masks')
                validPredictionData.append(currPredictionData)
            return validPredictionData
        else:
            raise IndexError(
                'Object segmentor model returned an empty prediction array! Unexpected behaviour!')

    def extractBoxesAndLabels(self, validPredictionData, rawPredictions, confidenceThreshold):
        if len(rawPredictions) == 1:
            singlePredictionData = self.extractSingleInstanceBoxesAndLabels(
                rawPredictions[0], confidenceThreshold)
            validPredictionData.append(singlePredictionData)
            return validPredictionData
        elif len(rawPredictions) > 1:
            for currPrediction in rawPredictions:
                currPredictionData = self.extractSingleInstanceBoxesAndLabels(
                    currPrediction, confidenceThreshold)
                validPredictionData.append(currPredictionData)
            return validPredictionData
        else:
            raise IndexError(
                'Detector model returned an empty prediction array! Unexpected behaviour!')

    def extractSingleInstanceBoxesAndLabels(self, singlePrediction, confidenceThreshold, predictionType='boxes'):
        predIndexMask = singlePrediction['scores'] > confidenceThreshold
        # Need to convert boxes from float to int in order to
        # draw them on the images.
        if predictionType == 'boxes':
            validPredictions = singlePrediction[predictionType][predIndexMask].int(
            ).detach().tolist()
        else:
            validPredictions = singlePrediction[predictionType][predIndexMask, :, :, :].detach(
            )
        validClassIndexes = singlePrediction['labels'][predIndexMask].tolist()
        validClassNames = self.mapClassIndexesToClassNames(validClassIndexes)
        return validPredictions, validClassNames

    def mapClassIndexesToClassNames(self, validClassIndexes):
        validClassNames = []
        for currIndex in validClassIndexes:
            validClassNames.append(self.classesArray[currIndex])
        return validClassNames

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
