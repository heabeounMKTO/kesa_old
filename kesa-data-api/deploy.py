import ast
import base64
import configparser
import json
import os

import convert.labelme2yolo
import cv2
import label_img
import numpy as np
import torch
from art import *
from flask import Flask, jsonify, render_template, request
from kesa_print import color, kesaError, kesaLog, kesaPrintDict
from kesa_utils import ModelUtils
from models.common import DetectMultiBackend
from utils.torch_utils import select_device

## the important part
print("ᐠ⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝ᐟᐠ⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝ᐟᐠ⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝ᐟ^⸜ˎ_ˏ⸝ᐟ^⸜ˎ")
print(text2art("processing"))
print("===========================|**|===================================")
print("\033[1m HEA⚡BEOUN's \033[0m")
print(text2art("kesa", font="isometric4"))
print("===========================|**|===================================")
print(text2art("conversion"))
print("ᐠ⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝ᐟᐠ⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝ᐟᐠ⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝ᐟ^⸜ˎ_ˏ⸝ᐟ^⸜ˎ")
###############################

"""
reads config file 
"""
# utils


def getdevice():
    try:
        cudaselectdevice = select_device(general_config["cuda_device"])
        kesaLog(f'GPU index {general_config["cuda_device"]} ,selected')
    except:
        kesaError("Failed in getting GPU, falling back to CPU...")
        cudaselectdevice = select_device("cpu")
    return cudaselectdevice


def read_config():
    config = configparser.ConfigParser()
    config.read("configs/auto-labelcfg.ini")
    general_cfg = {
        "longhu": config["MODEL"]["LONGHU"],
        "longhu-back": config["MODEL"]["LONGHU_BACK"],
        "confidence_thresh": float(config["INFERENCE_CONFIG"]["CONFIDENCE"]),
        "iou_thresh": float(config["INFERENCE_CONFIG"]["IOU"]),
        "cuda_device": int(config["DEVICE_SETTINGS"]["CUDA_DEVICE"]),
    }
    return config, general_cfg


##

rawcfg, general_config = read_config()


print("ᐠ⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝ᐟᐠ⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝ᐟᐠ⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝ᐟ^⸜ˎ_ˏ⸝ᐟ^⸜ˎ")
kesaPrintDict(
    "\033[1m Starting Kesa server with configurations: \033[0m ", general_config
)
print("ᐠ⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝ᐟᐠ⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝ᐟᐠ⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝^⸜ˎ_ˏ⸝ᐟ^⸜ˎ_ˏ⸝ᐟ^⸜ˎ")
kesaLog("Fetching model info..")
MODEL_INFO_DICT = ModelUtils().getAllModelInfoFromConfig(rawcfg)
kesaLog("Model info loaded!")

# select cuda device
cudaselectdevice = getdevice()

app = Flask(__name__)


@app.route("/")
def ayylmao():
    checkcuda = torch.cuda.is_available()
    yeah = dict(rawcfg.items("MODEL"))
    return render_template("index.html", cuda=checkcuda, models=list(yeah.keys()))


@app.route("/convertLabel", methods=["POST"])
def convert2yolo():
    r = request
    label_data = str(r.json["labeljson"])
    for annotations in ast.literal_eval(label_data)["shapes"]:
        print(annotations["points"])
    return jsonify({"ayy": "lmao"})


@app.route("/modelinfo")
def get_all_models():
    return jsonify({"available_models": f"{list(MODEL_INFO_DICT.keys())}"})


@app.route("/modelinfo/<modelname>", methods=["GET"])
def get_model_info(modelname):
    model2load = os.path.join("label_models", general_config[str(modelname)])
    loadModel = DetectMultiBackend(
        model2load, cudaselectdevice, dnn=False, data=None, fp16=True
    )
    return jsonify(
        {
            "status": "success",
            "class_names": loadModel.names,
            "model_stride": loadModel.stride,
            "isit_pt": loadModel.pt,
        }
    )


@app.route("/autolabel", methods=["POST"])
def labelshit():
    r = request
    convert2bytes = bytes(r.json["data"], "utf8")
    d_model = r.json["type"]
    # print(d_model)
    nparr = np.frombuffer(base64.b64decode(convert2bytes), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # load model
    model2load = os.path.join("label_models", general_config[str(d_model)])
    loadModel = DetectMultiBackend(
        model2load, cudaselectdevice, dnn=False, data=None, fp16=True
    )

    # label
    detectPt = label_img.imageDetect(
        img,
        general_config["cuda_device"],
        loadModel,
        general_config["confidence_thresh"],
    )
    label_result = detectPt.detect()

    return jsonify({"status": "success", "labelmejson": f"{label_result}"})


def create_app():
    return app
