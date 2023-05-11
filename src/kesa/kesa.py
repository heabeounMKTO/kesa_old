import os
from pathlib import Path
from labelme2yolo import Labelme2Yolo as L2Y
from autolabel import AutoLabel
import typer
from fileutils import fileUtils as fu
import json


class Kesa:
    def __init__(self) -> None:
        return None

    def setMode(self, mode):
        self.mode = mode
        print(f"kesa starting in {self.mode} mode")

    def kesaAutoLabel(self, input, confidence_thresh=0.9, iou_thresh=0.7):
        label = AutoLabel(input, confidence_thresh, iou_thresh)
        label.Label()

    def kesaConvertLabelme2Yolo(self, input, output):
        def kesaInitConversionFolder(processFolder, exportFolder):
            file_utils = fu(processFolder, exportFolder)
            file_utils.createExportFolder()
            file_utils.createLabelListFromFolder()
            return file_utils

        conversion = kesaInitConversionFolder(input, output)
        label_list = conversion.loadLabelList()
        for file in os.listdir(input):
            if file.endswith(".json"):
                loadjson = json.load(open(os.path.join(input, file)))
                convertLM = L2Y(loadjson, label_list, input)
                convertLM.convert2YOLO()
        conversion.moveAnnotationsToFolder()

    def kesaEnd2EndConversion(
        self, input, output, confidence_thresh=0.9, iou_thresh=0.7
    ):
        self.kesaAutoLabel(input, confidence_thresh, iou_thresh)
        self.kesaConvertLabelme2Yolo(input, output)
