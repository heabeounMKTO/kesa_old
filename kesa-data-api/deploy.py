from flask import Flask, request, jsonify, render_template
import cv2
import json
import numpy as np
import base64
import os
import torch
import configparser
import label_img
from utils.torch_utils import select_device
from models.common import DetectMultiBackend

"""
reads config file 
"""


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
    return general_cfg


general_config = read_config()
print(f"starting detect server with settings: \n { general_config }")
cudaselectdevice = select_device(general_config["cuda_device"])
app = Flask(__name__)


@app.route("/")
def ayylmao():
    checkcuda = torch.cuda.is_available()
    return render_template("index.html", cuda=checkcuda)


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
