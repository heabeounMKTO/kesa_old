import os
from pathlib import Path
import typer
import json
import requests
from utils.config import CfgUtils
from urllib.parse import urljoin
from utils.file_utils import KesaFileCli as KFC
from kesa import Kesa

app = typer.Typer()
from pathlib import Path
rawcfg, general_cfg = CfgUtils().read_config()
                

@app.command()
def getAvailableModels():
    """
    get all available models from server
    """
    full_url = urljoin(general_cfg["address"], 'modelinfo')
    r = requests.get(full_url)
    resJson = json.loads(r.text)
    resJson = eval(resJson["available_models"])
    # needs eval for multiple params
    # will explain later (maybe? lol).
    for x in resJson:
        print(x)
    return resJson


@app.command()
def getModelInfo(model_name: str):
   """
   get labels for specific model
   """
   full_url = urljoin(general_cfg["address"], f'modelinfo/{model_name}')
   # print(full_url)
   r = requests.get(full_url)
   resJson = json.loads(r.text)["class_names"]
   print(resJson)
   return resJson
@app.command()
def convertLabel(input: str, 
                 model_name: str, 
                 target_format: str = "yolo",
                 augment: int = 0,
                 save_folder = "_kesatemp",
                 export_folder = "export" 
                ):
    """
    Args:
        input (str): input annotations folder 

        target_format (str, optional): target conversion format. Defaults to "yolo".
        augment (int, optional): how many times to augment the annotations. Defaults to 0.
        save_folder (str, optional): temporary folder for storing the processed images. Defaults to "_kesatemp".
        export_folder (str, optional): final export folder. Defaults to "export".
    """
    KesaFile = KFC()
    KesaFile.createExportFolder(save_folder, export_folder)
    for file in os.listdir(Path(input)):
        if file.endswith(".json"):
            full_pth = os.path.join(input, file)
            result = Kesa().convertsingle(
                                        full_pth, 
                                        model_name, 
                                        general_cfg,
                                        augment = augment
                                        )
            # MFW NO MATCH STATEMENT COS COMPATIBILITY
            if augment == 0:
                anno_filename = os.path.join(input 
                                             ,(os.path.splitext(file)[0] + ".txt")) 
                print(result["label"]) 
                KesaFile.writeYoloAnnotationsToTXT(anno_filename, 
                                                   result["label"]) 
    
if __name__ == "__main__":
    app()
