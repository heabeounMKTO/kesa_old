from models.common import DetectMultiBackend




class ModelUtils:
    def __init__(self) -> None:
        pass

    def getAllModelInfoFromConfig(self, config_file):
        '''
        get all model info from config object 
        '''
        models_dict = dict(config_file["MODEL"])
        for models in models_dict:
            print(models)

