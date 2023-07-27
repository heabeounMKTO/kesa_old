import albumentations
import cv2
import json
from convert.augment import augmentImage as Aug
import os
import uuid
import base64
import numpy as np

class Labelme2Yolo:
    def __init__(self, json_file, labellist):
        self.jsonFile = json.dumps(json_file, indent=4)
        self.jsonFile = json.loads(self.jsonFile)
        self.labellist = labellist

    def getImageDimensions(self):
        imageWidth = self.jsonFile["imageWidth"]
        imageHeight = self.jsonFile["imageHeight"]
        self.imageDimensions = [imageWidth, imageHeight]
        return self.imageDimensions

    def xyxy2xywh(self, xyxy):
        x1, y1 = xyxy[0]
        x2, y2 = xyxy[1]
        x_center = ((x1 + x2) / 2) / self.imageDimensions[0]
        y_center = ((y1 + y2) / 2) / self.imageDimensions[1]
        _w = (x2 - x1) / self.imageDimensions[0]
        _h = (y2 - y1) / self.imageDimensions[1]
        return x_center, y_center, _w, _h

    def convert2Yolo(self):
        # will be subjected to change
        self.getLabelsFromJson()
        filename = os.path.splitext(self.jsonFile["imagePath"])[0]
        unique_n = self.createUniqueFileName(filename)
        return self.yoloarr

    def convert2Yolo_aug(self, b64img, times):
        self.getLabelsFromJson_aug()
        filename = os.path.splitext(self.jsonFile["imagePath"])[0]
        unique_n = self.createUniqueFileName(filename)
        augmentRounds = []
        total = []
        augmentImage = Aug()

        for i in range(0, times):
            result = augmentImage.applyAugmentation(
                b64img, self.yoloarr[0], self.yoloarr[1]
            )
            augmentRounds.append(result)
        for results in augmentRounds:
            filename = os.path.splitext(self.jsonFile["imagePath"])[0]
            unique_n = self.createUniqueFileName(filename)
            total_coords = []
            print("res", results[0])        
            for classid, coords in zip(self.yoloarr[0], results[1]):
                combined = [classid, coords[0], coords[1], coords[2], coords[3]]
                # collect coords
                total_coords.append(combined)
            augment_dict = {
                "label": total_coords,
                "base64img": str(self.mat2b64(results[0])),
                "unique_name": unique_n,
            }
            total.append(augment_dict)

        return total

    def createUniqueFileName(self, inputFilename):
        unique_id = str(uuid.uuid4().hex)
        file = os.path.splitext(inputFilename)
        unique_name = file[0] + unique_id
        return unique_name

    def getLabelsFromJson(self):
        self.yoloarr = []
        self.getImageDimensions()
        for labels in self.jsonFile["shapes"]:
            x1y1 = labels["points"][0]
            x2y2 = labels["points"][1]
            x, y, w, h = self.xyxy2xywh((x1y1, x2y2))
            labelclass = self.labellist.index(labels["label"])
            self.yoloarr.append([labelclass, x, y, w, h])
        return self.yoloarr

    def mat2b64(self, cvmat):
        """
        opencv matrix -> base64
        """
        # cv2.imwrite("penistest.jpg", cvmat)
        _, img_arr = cv2.imencode(".jpg", cvmat)
        # print("imgarr",_, img_arr, len(img_arr))
        b64encoded = base64.b64encode(img_arr.tobytes()) 
        return b64encoded 

    def getLabelsFromJson_aug(self):
        coords_bundle = []
        class_bundle = []
        self.getImageDimensions()
        for labels in self.jsonFile["shapes"]:
            x1y1 = labels["points"][0]
            x2y2 = labels["points"][1]
            x, y, w, h = self.xyxy2xywh((x1y1, x2y2))
            x, y, w, h = abs(x), abs(y), abs(w), abs(h)
            # for some reason wome of the coords are negative!
            # i will look into this later
            coords_bundle.append((x, y, w, h))
            class_bundle.append(str(self.labellist.index(labels["label"])))
        self.yoloarr = [class_bundle, coords_bundle]
        return self.yoloarr
