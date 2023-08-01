import json
import os
import uuid
from pathlib import Path
import io
import albumentations as A
import cv2
import numpy as np
import base64


class augmentImage:
    def __init__(self) -> None:
        return None

    def applyAugmentation(
        self, input, labellist, bbox_coords, resize=640, fromb64=True
    ):
        """
        augments image from input, reads from local filepath, OR
        you can send a base64 (for web thingz)
        note : this is probably not good error handling lol,
        but it works for now , will fix it later
        if i dont forget about it lol
        """
        if not fromb64:
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
                    format="yolo", label_fields=["categeory_id"]
                    ,min_area=0.0
                ),
            )
            transformed = transform(
                image=image, bboxes=bboxes, categeory_id=categeory_id
            )
            one = [transformed["image"], transformed["bboxes"]]
            return one
        else:
            """
            reads base64 image as bytes in utf8 then
            into a nparray then into a openCV mat, there is
            probably a better way but for now this works.
            """
            img2bytes = bytes(input, "utf8")
            nparr = np.frombuffer(base64.b64decode(img2bytes), np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            # converts to RGB cos everything is read as BGR in openCV
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # ok im not sure
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
            transformed = transform(
                image=image, bboxes=bboxes, categeory_id=categeory_id
            )
            one = [transformed["image"], transformed["bboxes"]]
            return one
