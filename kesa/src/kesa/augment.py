import albumentations as A
import cv2
import uuid
import json
import os
from pathlib import Path
import numpy as np



class augmentImage:
    def __init__(self) -> None:
        return None

    def applyAugmentation(self, input,labellist, bbox_coords, resize=640):
        image = cv2.imread(input)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        bboxes = bbox_coords
        categeory_id = labellist 
        transform = A.Compose(
            [
                A.ChannelDropout(),
                A.Flip(always_apply=True),
                A.Resize(resize, resize, always_apply=True),
                A.HorizontalFlip(),
                A.VerticalFlip(),
                A.RandomRain(),
            ],
            bbox_params=A.BboxParams(
                format="yolo", label_fields=["categeory_id"], min_area=0.0
            ),
        )
        transformed = transform(image=image, bboxes=bboxes, categeory_id=categeory_id)
        one = [transformed["image"], transformed["bboxes"]]
        return one

# testimage = "labeltest/tiger-1683001948246.jpeg"
# labellist = ["1", "8"]
# bbx = [
#     (0.3569937369519833, 0.3190675017397356, 0.4154488517745303, 0.1885873347251218),
#     (0.39718162839248433, 0.5549756437021572, 0.40396659707724425, 0.1579679888656924),
# ]

# testfolder = "labeltest"
# test = augmentImage()
# result = test.applyAugmentation(testimage,labellist, bbx)
# print(result)

