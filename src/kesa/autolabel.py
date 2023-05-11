from models.common import DetectMultiBackend
from detect import imageDetect
from utils.torch_utils import select_device
import cv2
from pathlib import Path
import os
import configparser
import json
import base64
import tqdm
from rich import print
from rich.console import Console
from rich.table import Table

# read global config file
config = configparser.ConfigParser()
config.read("auto-labelcfg.ini")


MODEL_PATH = os.path.join("detect-models", config["MODEL"]["MODEL_NAME"])
CUDA_DEVICE = select_device(str(config["DEVICE_SETTINGS"]["CUDA_DEVICE"]))
CONFIDENCE_THRESH = float(config["INFERENCE_CONFIG"]["CONFIDENCE"])
ext = [".jpeg", ".jpg", ".png"]


class AutoLabel:
    def __init__(self, processingFolder, confidence=0.9, iou=0.7):
        self.processingFolder = processingFolder
        self.confidence = confidence
        self.iou = iou
        print("config loaded:")
        print(
            f"Model: {MODEL_PATH}\nCuda Device: {CUDA_DEVICE}\nConfidence: {CONFIDENCE_THRESH}"
        )
        self.loadmodel = DetectMultiBackend(
            MODEL_PATH, CUDA_DEVICE, dnn=False, data=None, fp16=False
        )
        if self.loadmodel:
            print("Model Loaded")
        self.labeledimg = 0

    def findAllImageInFolder(self):
        imagePaths = []

        print(f"looking for files in {self.processingFolder}")
        for roots, dirs, files in os.walk(self.processingFolder):
            print(f"found {len(files)} files in {self.processingFolder}")
            for file in files:
                if file.endswith(tuple(ext)):
                    self.labeledimg += 1
                    fullimagepath = os.path.join(self.processingFolder, file)
                    imagePaths.append(fullimagepath)
            return imagePaths

    def Label(self):
        images = self.findAllImageInFolder()
        for image in tqdm.tqdm(images):
            detectLabels = imageDetect(
                image, CUDA_DEVICE, self.loadmodel, CONFIDENCE_THRESH
            )
            result = detectLabels.detect()
            json_obj = json.dumps(result, indent=2)
            fileName = os.path.splitext(os.path.basename(image))[0] + ".json"
            jsonFileExportName = os.path.join(self.processingFolder, fileName)
            # export json with same name as image file name
            with open(jsonFileExportName, "w") as json_output:
                json_output.write(json_obj)
        print("Labeling Done!\n")
        table = Table("Images Labeled")
        table.add_row(f"{self.labeledimg}")
        console = Console()
        console.print(table)
