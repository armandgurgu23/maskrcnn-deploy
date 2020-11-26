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
        _config.imagePainter = CN()
        _config.imagePainter.boxWidth = 1
        _config.imagePainter.textPixelShiftWidth = 0.1
        _config.imagePainter.textPixelShiftHeight = 0.1
        _config.imagePainter.textStrokeWidth = 0.1
        _config.imagePainter.colorChoice = ''
        _config.imagePainter.colorFile = ''
        _config.imagePainter.fontName = ''
        _config.imagePainter.fontRefWidth = 10
        _config.imagePainter.fontSize = 1
        _config.imagePainter.objectMasks = CN()
        _config.imagePainter.objectMasks.applyMaskProcessor = False
        _config.imagePainter.objectMasks.objectTransparencyFactor = 0.1
        _config.imagePainter.objectMasks.processorMethod = ''
        return _config.clone()


def getPainterYamlConfig(yamlFilePath='imagePainter/config/painterConfig.yaml'):
    configObject = ConfigDefaults()
    return configObject(yamlFilePath)
