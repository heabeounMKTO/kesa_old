import gc
import os
from kesa_print import kesaLog, kesaError
import configparser
from models.common import DetectMultiBackend
from utils.torch_utils import select_device
import pathlib
from pathlib import Path
class FileUtils:
    def __init__(self) -> None:
        pass

    def validateFileExists(self, file_path):
        kesaLog(f"checking if file {file_path} exists")
        file_path = os.path.join(os.getcwd(), file_path) 
        if pathlib.Path(file_path).is_file():
            kesaLog(f"file: {file_path} found", logtype="ok")
            return True
        else:
            kesaError(f"file: {file_path} NOT FOUND !?, please check & re-check")
            return False 
    


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
                

                #check if the mf file even exist before try lodaing LMAO
                if FileUtils().validateFileExists(model_filename):
                ## loads model to CPU
                    loadModel = DetectMultiBackend(
                        model_filename, select_device("cpu"), dnn=False, data=None, fp16=True
                    )
                    # add model class info to dict
                    modelInfoDict[model] = loadModel.names
                else:
                    kesaLog(f"couldnt load file: {model_filename}", logtype="aight")
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

