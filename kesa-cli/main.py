import os
from pathlib import Path
import typer
import json
import requests
from utils.config import CfgUtils
from urllib.parse import urljoin
from utils.convert import Labelme2Yolo as L2Y

app = typer.Typer()
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
def convertsingle(json_path: str, model_name: str, target_format: str = "yolo", augment: int = 0):
    """
    convert single labelme json file 
    to yolo .txt format
    """
    jsonFile = json.load(open(json_path)) 
    fullurl = urljoin(general_cfg["address"]
                      ,f'convertLabel/{target_format}/{model_name}')
    r = requests.post(fullurl, 
                      json={"labelme_json":jsonFile, 
                            "model_name":model_name, 
                            "augment":f"{augment}"})        
    
    print(r.text)


if __name__ == "__main__":
    app()
