from yacs.config import CfgNode as CN


class ConfigDefaults(object):
    def __init__(self):
        self.defaultConfig = self.makeDefaultConfig()

    def __call__(self, yamlFilePath):
        self.defaultConfig.merge_from_file(yamlFilePath)
        self.defaultConfig.freeze()
        return self.defaultConfig

    def makeDefaultConfig(self):
        _config = CN()
        _config.detectorModel = CN()
        _config.detectorModel.pretrained = True
        _config.detectorModel.minSize = 100
        _config.detectorModel.predictionClassesPath = ''
        _config.detectorModel.staticPredictions = True
        _config.detectorModel.staticPredictionsConfig = CN()
        _config.detectorModel.staticPredictionsConfig.staticPredictionsInputPath = ''
        _config.detectorModel.staticPredictionsConfig.staticPredictionsOutputPath = ''
        _config.detectorModel.confidenceThreshold = 0.1
        return _config.clone()


def getModelYamlConfig(yamlFilePath='maskRCNN/config/modelConfig.yaml'):
    configObject = ConfigDefaults()
    return configObject(yamlFilePath)
