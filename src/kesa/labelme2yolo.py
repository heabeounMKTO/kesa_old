import os
import math
from typing import final
import tqdm
from augment import augmentImage
import uuid
import json
import numpy as np
import cv2
from fileutils import fileUtils as fu


class Labelme2Yolo:
    def __init__(self, json, labellist, processingFolder):
        self.jsonFile = json
        self.labellist = labellist
        self.processingFolder = processingFolder
        self.imagePath = os.path.join(self.processingFolder, self.jsonFile["imagePath"])
        self.imageExtension = os.path.splitext(self.jsonFile["imagePath"])[1]

    def convert2YOLO(self):
        self.getLabelsFromJson()
        self.getFilename()
        self.writeYOLOtoFile(
            self.yoloarr, os.path.join(self.processingFolder, self.filename)
        )

    # def convert2YOLO_aug(self, times):
    #     self.getLabelsFromJson4aug()
    #     self.getFilename()
    #     print(self.imagePath)
    #     augmentimage = augmentImage(self.imagePath,self.yoloarr[1],self.labellist, times)
    #     result = augmentimage.applyAugmentation()
    #     for x in range(0, (len(results)-1)):
    #         uni_fn = self.createUniqueFileName(self.imagePath)
    #         results[x][0] = cv2.cvtColor(results[x][0], cv2.COLOR_BGR2RGB)
    #         cv2.imwrite(uni_fn[1], results[x][0])
    #         pair_coords = []
    #         for classid,coords in zip(self.yoloarr[0],results[x][1]):
    #             combined = [classid, coords[0],coords[1],coords[2],coords[3]]
    #             pair_coords.append(combined)
    #             self.writeYOLOtoFile(pair_coords, uni_fn[0])
    def convert2YOLO_aug(self,times):
        self.getLabelsFromJson4aug()
        self.getFilename()
        augmentRounds = []
        augmentimage = augmentImage()
        # print(self.imagePath,self.yoloarr[1],"\n")
        for i in range(0, times): 
            result = augmentimage.applyAugmentation(self.imagePath,self.yoloarr[0], self.yoloarr[1])
            augmentRounds.append(result) 
        for results in augmentRounds:
            uni_fn = self.createUniqueFileName(self.imagePath) 
            results[0] = cv2.cvtColor(results[0], cv2.COLOR_BGR2RGB)
            cv2.imwrite(uni_fn[1], results[0])
            pair_coords = []
            for classid,coords in zip(self.yoloarr[0],results[1]):
                combined = [classid, coords[0],coords[1],coords[2],coords[3]]
                pair_coords.append(combined)
                self.writeYOLOtoFile(pair_coords, uni_fn[0])
                
    def createUniqueFileName(self, inputFilename):
        unique_id = str(uuid.uuid4().hex)
        file = os.path.splitext(inputFilename)
        final_txt = file[0] + unique_id + ".txt"
        final_img = file[0] + unique_id + self.imageExtension
        return [final_txt, final_img]

    def getFilename(self):
        self.filename = os.path.splitext(self.jsonFile["imagePath"])[0] + ".txt"
        return self.filename

    def arrayToPairs(self, array, chunk_size):
        pair = []
        for i in range(0, len(array), chunk_size):
            yield array[i : i + chunk_size]

    def xyxy2xywh(self, xyxy):
        x1, y1 = xyxy[0]
        x2, y2 = xyxy[1]
        x_center = ((x1 + x2) / 2) / self.imageDimensions[0]
        y_center = ((y1 + y2) / 2) / self.imageDimensions[1]
        _w = (x2 - x1) / self.imageDimensions[0]
        _h = (y2 - y1) / self.imageDimensions[1]
        return x_center, y_center, _w, _h

    def getImageDimensions(self):
        imageWidth = self.jsonFile["imageWidth"]
        imageHeight = self.jsonFile["imageHeight"]
        self.imageDimensions = [imageWidth, imageHeight]
        return self.imageDimensions

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

    def getLabelsFromJson4aug(self):
        # final_bundle = []
        coords_bundle = []
        class_bundle = []
        self.getImageDimensions()
        for labels in self.jsonFile["shapes"]:
            x1y1 = labels["points"][0]
            x2y2 = labels["points"][1]
            x, y, w, h = self.xyxy2xywh((x1y1, x2y2))
            x, y, w, h = abs(x), abs(y), abs(w), abs(h) 
            # for some reason wome of the coords are negative! 
            # will investigate lateer!
            coords_bundle.append((x, y, w, h))
            class_bundle.append(str(self.labellist.index(labels["label"])))
        self.yoloarr = [class_bundle, coords_bundle]
        return self.yoloarr

    def writeYOLOtoFile(self, yololabels, filename):
        print("Writing annoations to File...")
        with open(filename, "w") as f:
            for annotations in tqdm.tqdm(yololabels):
                f.write(str(annotations[0]))
                f.write(" ")
                f.write(str(annotations[1]))
                f.write(" ")
                f.write(str(annotations[2]))
                f.write(" ")
                f.write(str(annotations[3]))
                f.write(" ")
                f.write(str(annotations[4]))
                f.write("\n")


# def initFolders(input, output):
#     file_utils = fu(input, output)
#     file_utils.createExportFolder()
#     file_utils.createLabelListFromFolder()
#     return file_utils

# def convertaugTest(input, output):
#     conversion = initFolders(input, output)
#     label_list = conversion.loadLabelList()
#     for file in os.listdir(input):
#         if file.endswith(".json"):
#             loadjson = json.load(open(os.path.join(input, file)))
#             convertLM = Labelme2Yolo(loadjson,label_list, input)
#             convertLM.convert2YOLO_augtest(1)
#     conversion.moveAnnotationsToFolder()
# file = "labeltest"
# convertaugTest(file, file)
# test = Labelme2Yolo("labeltest/tiger-1683001948246.jpeg",["1","3"],"labeltest")
# test.convert2YOLO_augtest()
