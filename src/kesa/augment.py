import albumentations as A
import cv2
import uuid 
from labelme2yolo import Labelme2Yolo as L2Y
import json

class augmentImage:
    def __init__(self, imagePath, bbox_coords, labellist, readFromFile=False):
        self.image = cv2.imread(imagePath)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.bbox_coords = bbox_coords
        self.labellist = labellist
        self.imagePath = imagePath
        if readFromFile != False:
            for label in json.load(open(imagePath))["shapes"]:
                print(label)

    def applyAugmentation(self):
        bboxes = self.bbox_coords
        categeory_id = self.labellist
        transform = A.Compose(
            [
                A.ChannelDropout(),
                A.Flip(always_apply=True),
                A.Resize(640, 640, always_apply=True),
                A.HorizontalFlip(),
                A.VerticalFlip(),
                A.RandomRain(),
            ],
            bbox_params=A.BboxParams(
                format="yolo", label_fields=["categeory_id"], min_area=0.0
            ),
        )
        transformed = transform(
            image=self.image, bboxes=bboxes, categeory_id=categeory_id
        )
        self.saveAugmentedImage(transformed)


    def saveAugmentedImage(self,augmentedImageData):
        print(augmentedImageData)
        print(self.imagePath)

test = augmentImage("labeltest/testimg1.jpeg")
