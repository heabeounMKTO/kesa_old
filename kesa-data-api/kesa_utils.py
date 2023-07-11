import gc
import os

from models.common import DetectMultiBackend
from utils.torch_utils import select_device


class ModelUtils:
    def __init__(self) -> None:
        pass

    def getAllModelInfoFromConfig(self, config_file):
        """
        get all model info from config object
        """
        models_dict = dict(config_file["MODEL"])
        modelInfoDict = {}
        for model in models_dict:
            model_filename = os.path.join("label_models", models_dict[model])

            ## loads model to CPU
            loadModel = DetectMultiBackend(
                model_filename, select_device("cpu"), dnn=False, data=None, fp16=True
            )
            # add model class info to dict
            modelInfoDict[model] = loadModel.names
        # free memory from CPU
        gc.collect()
        return modelInfoDict
