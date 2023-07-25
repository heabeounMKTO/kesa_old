import albumentations
import cv2
import json
from convert.augment import augmentImage as Aug
import os
import uuid


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
        
        filename = os.path.splitext(self.jsonFile["imagePath"])[0]
        unique_n = self.createUniqueFileName(filename) 
        
        return unique_n, self.getLabelsFromJson()

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
