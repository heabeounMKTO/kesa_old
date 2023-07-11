import albumentations
import cv2


class Labelme2Yolo:
    def __init__(self, json):
        self.jsonFile = json
