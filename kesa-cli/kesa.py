import os
from pathlib import Path
import typer
import json
import requests
from utils import CfgUtils
from urllib.parse import urljoin

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
    # will explain later.
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

# @app.command()



# def convert2yolo(input_path):
    


if __name__ == "__main__":
    app()
