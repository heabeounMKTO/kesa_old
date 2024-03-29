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
from art import text2art
from flask import Flask, jsonify, render_template, request
from kesa_print import color, kesaError, kesaLog, kesaPrintDict
from kesa_utils import ModelUtils, CfgUtils
from models.common import DetectMultiBackend
from utils.torch_utils import select_device
from convert.labelme2yolo import Labelme2Yolo as L2Y


## the important part, the people must know
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


##

rawcfg, general_config = CfgUtils().read_config()


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


@app.route("/convertLabel/yolo/<modelname>", methods=["POST"])
def convert2yolo(modelname):
    r = request
    label_data = r.json["labelme_json"]
    convert = L2Y(label_data, MODEL_INFO_DICT[modelname])
    if int(r.json["augment"]) <= 0:
        unique_name, labels = convert.convert2Yolo()
        return jsonify({"unique_name": unique_name, "labels": labels})
    else:
        """
        sends back augmented images in base64 format
        according to the times mentioned, b64 is encoded as string
        ples read as bytes
        """
        label_aug = convert.convert2Yolo_aug(
            r.json["labelme_json"]["imageData"], int(r.json["augment"])
        )
        return jsonify({"label_multi": label_aug})


@app.route("/modelinfo")
def get_all_models():
    return jsonify({"available_models": f"{list(MODEL_INFO_DICT.keys())}"})


@app.route("/modelinfo/<modelname>", methods=["GET"])
def get_model_info(modelname):
    return jsonify(
        {
            "status": "success",
            "class_names": MODEL_INFO_DICT[modelname],
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
