import gc
import os
from kesa_print import kesaError
import configparser
from models.common import DetectMultiBackend
from utils.torch_utils import select_device


class ModelUtils:
    def __init__(self) -> None:
        pass

    def getAllModelInfoFromConfig(self, config_file):
        """
        get all model info from config object
        """
        try:
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
        except FileNotFoundError as nofile:
            kesaError(f"{nofile}")

class CfgUtils:
    def __init__(self) -> None:
        pass

    def read_config(self):
        config = configparser.ConfigParser()
        try:
            config.read("configs/auto-labelcfg.ini")        
            general_cfg = {
            "longhu": config["MODEL"]["LONGHU"],
            "longhu-back": config["MODEL"]["LONGHU_BACK"],
            "confidence_thresh": float(config["INFERENCE_CONFIG"]["CONFIDENCE"]),
            "iou_thresh": float(config["INFERENCE_CONFIG"]["IOU"]),
            "cuda_device": int(config["DEVICE_SETTINGS"]["CUDA_DEVICE"]),
            }
            return config, general_cfg
        except FileNotFoundError as nofile:
            kesaError(f"{nofile}")

