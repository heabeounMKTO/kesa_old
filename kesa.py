import os
from pathlib import Path
from labelme2yolo.labelme2yolo import Labelme2Yolo as L2Y 
from auto_label.autolabel import AutoLabel
import typer


class Kesa:
    def __init__(self,mode):
        self.mode = mode

    def kesaAutoLabel(self, autoLabelFolder, confidence_thresh, iou_thresh):
        label = AutoLabel(autoLabelFolder)
        print(label)



test = Kesa("augment")
test.kesaAutoLabel("test", 0.4,0.5)

