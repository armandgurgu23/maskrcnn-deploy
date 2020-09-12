import torchvision.models as models


class MaskRCNNModelWrapper(object):
    def __init__(self, pretrained, minSize=400):
        self.pretrained = pretrained
        self.minSize = minSize
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
        raise NotImplementedError('Barrier to output! Add predictions processing handler.')
        # return

    def initializeMaskRCNNModel(self, pretrained, minSize):
        return models.detection.maskrcnn_resnet50_fpn(pretrained=pretrained, min_size=minSize)
