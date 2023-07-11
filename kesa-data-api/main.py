from flask import Flask, request, jsonify, render_template
import cv2
import json
import numpy as np
import base64
import os
import torch
import configparser
import label_img
import ast
import convert.labelme2yolo
from art import *
from utils.torch_utils import select_device
from models.common import DetectMultiBackend


## the important part
print("---------------------------------------------------------------")
print(text2art("processing"))
print("---------------------------------------------------------------")
print(text2art("kesa", font="isomertic1"))
print("---------------------------------------------------------------")
print(text2art("conversion"))
print("---------------------------------------------------------------")
"""
reads config file 
"""
def print_dict(notify_string ,input_dict):
    print(notify_string)
    for items in input_dict.items():
        print(f"\033[1mL🍑GGER: {items[0]} : {items[1]} \033[0m ")

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


rawcfg, general_config = read_config()
print_dict( "\033[1m Starting Kesa with Configurations: \033[0m ", general_config)
# print(f"\033[1m starting kesa with settings: \n { general_config }\033[0m")
cudaselectdevice = select_device(general_config["cuda_device"])
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
    yeah = dict(rawcfg.items("MODEL"))
    return jsonify({"available_models": list(yeah.keys())})


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


app.run(port=6969, debug=True)
