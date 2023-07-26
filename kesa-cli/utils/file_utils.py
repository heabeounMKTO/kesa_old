import json
import os
from pathlib import Path
import tqdm
import shutil
import math
import yaml
import uuid
import cv2
import base64
import numpy as np
import PIL as Image


ext = [".jpeg", ".jpg", ".png"]


class KesaFileCli:
    def __init__(self) -> None:
        pass

    def setLabelList(self, LabelList):
        self.LabelList = LabelList

    def setProcessingFolder(self, processingFolder):
        self.processingFolder = processingFolder

    def setExportFolder(self, exportFolder):
        self.exportFolder = exportFolder

    def getProcessingFolder(self):
        return self.processingFolder

    def getExportFolder(self):
        return self.exportFolder

    def createExportFolder(self, processingFolder, exportFolder):
        self.setProcessingFolder(processingFolder)
        self.setExportFolder(exportFolder)
        # THIS IS FOR EASY CHANGING OF NAMES OK
        images = "images"
        labels = "labels"
        print(f"creating test folder {self.exportFolder}")
        try:
            os.makedirs(os.path.join(f"{self.exportFolder}/test", images))
            os.makedirs(os.path.join(f"{self.exportFolder}/test", labels))
        except FileExistsError:
            print("folder already exists!")
        print(f"creating train folder at {self.exportFolder}")
        try:
            os.makedirs(os.path.join(f"{self.exportFolder}/train", images))
            os.makedirs(os.path.join(f"{self.exportFolder}/train", labels))
        except FileExistsError:
            print("folder already exists!")
        print(f"creating valid folder {self.exportFolder}")
        try:
            os.makedirs(os.path.join(f"{self.exportFolder}/valid", images))
            os.makedirs(os.path.join(f"{self.exportFolder}/valid", labels))
        except FileExistsError:
            print("folder already exists!")

    def createLabelList(self):
        """
        creates data.yaml file for folder
        """
        jsonlist = self.LabelList
        with open(os.path.join(self.exportFolder, "data.yaml"), "w") as file:
            ayylmao = dict(
                names=jsonlist,
                nc=len(jsonlist),
                train=f"/{self.exportFolder}/train/images",
                val=f"/{self.exportFolder}/valid/images",
                test=f"/{self.exportFolder}/test/images",
            )

    def loadLabelList(self, exportFolder) -> list:
        exportFolder = self.exportFolder
        with open(os.path.join(self.exportFolder, "data.yaml")) as file:
            data_yaml = yaml.safe_load(file)
            labellist = data_yaml["names"]
            return labellist

    def createLabelListFromFolder(self):
        """
        seldom used, will be replaced with just a label request from `kesa-data-api`
        """
        jsonlist = []
        for roots, dirs, files in os.walk(self.processingFolder):
            for file in files:
                if file.endswith(".json"):
                    jsonFile = json.load(open(os.path.join(roots, file)))
                    for label in jsonFile["shapes"]:
                        jsonlist.append(label["label"])
        jsonlist = sorted(set(jsonlist))

        with open(os.path.join(self.exportFolder, "data.yaml"), "w") as file:
            ayylmao = dict(
                names=jsonlist,
                nc=len(jsonlist),
                train=f"/{self.exportFolder}/train/images",
                val=f"/{self.exportFolder}/valid/images",
                test=f"/{self.exportFolder}/test/images",
            )
            yaml.dump(ayylmao, file, default_flow_style=None)

    def moveToFolder(self, jsonList, destinationFolder):
        def moveLabelandImage(annotation, foldername):
            orig_labels_path = os.path.join(self.processingFolder, annotation)
            matchedImage = str(findMatchingImage(annotation))
            orig_images_path = os.path.join(self.processingFolder, matchedImage)
            dest_labels_path = os.path.join(
                self.exportFolder, os.path.join(foldername, "labels")
            )

            dest_images_path = os.path.join(
                self.exportFolder, os.path.join(foldername, "images")
            )
            full_dest_label_path = os.path.join(dest_labels_path, annotation)
            full_dest_image_path = os.path.join(dest_images_path, matchedImage)

            if os.path.exists(orig_images_path):
                shutil.copy(orig_images_path, full_dest_image_path)
            else:
                pass
            if os.path.exists(orig_labels_path):
                shutil.copy(orig_labels_path, full_dest_label_path)
            else:
                pass

        def findMatchingImage(annotation):
            for file in self.allfiles:
                if file.endswith(tuple(ext)):
                    if os.path.splitext(file)[0] == os.path.splitext(annotation)[0]:
                        if file != None:
                            return file

        match destinationFolder:
            case "train":
                print("train set")
                for index in tqdm.tqdm(range(0, self.train_number - 1)):
                    moveLabelandImage(jsonList[index], "train")
            case "valid":
                print("valid set")
                for index in tqdm.tqdm(
                    range(
                        (self.train_number), (self.train_number + self.val_number) - 1
                    )
                ):
                    moveLabelandImage(jsonList[index], "valid")
            case "test":
                print("test set")
                for index in tqdm.tqdm(
                    range(
                        (self.train_number + self.val_number),
                        (self.train_number + self.val_number + self.test_number) - 1,
                    )
                ):
                    moveLabelandImage(jsonList[index], "test")

    def moveAnnotationsToFolder(self, train_split=75, val_split=15, test_split=10):
        jsonfiles = []
        self.allfiles = []
        for file in os.listdir(self.processingFolder):
            self.allfiles.append(file)
            if file.endswith(".txt"):
                jsonfiles.append(file)
        self.train_number = math.ceil((len(jsonfiles)) * train_split / 100)
        self.val_number = math.floor((len(jsonfiles)) * val_split / 100)
        self.test_number = math.floor((len(jsonfiles)) * test_split / 100)

        self.moveToFolder(jsonfiles, "train")
        self.moveToFolder(jsonfiles, "valid")
        self.moveToFolder(jsonfiles, "test")

    def writeYoloAnnotationsToTXT(
        self,
        file_name,
        annotation_list,
    ) -> None:
        """
        writes annotation list to txt file
        Args:
            file_name (_type_): file name NO EXTENSIONS
            annotation_list (_type_): the converted label list
        """
        with open(file_name, "w") as f:
            for annotations in annotation_list:
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

    def writeBase64ToImage(self, file_name, b64_img):
        im_bytes = base64.b64decode(b64_img)
        print(im_bytes)
        nparr = np.frombuffer(im_bytes, dtype=np.uint8)\
        