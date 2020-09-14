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
        _config.imagePainter.textPixelShift = 1
        _config.imagePainter.textStrokeWidth = 1
        _config.imagePainter.colorChoice = ''
        _config.imagePainter.colorFile = ''
        return _config.clone()


def getPainterYamlConfig(yamlFilePath='imagePainter/config/painterConfig.yaml'):
    configObject = ConfigDefaults()
    return configObject(yamlFilePath)
