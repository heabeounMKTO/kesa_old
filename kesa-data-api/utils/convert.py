import json


class Convert:
    def __init__(self) -> None:
        return None

    def xyxy2xywh(self, xyxy, w, h):
        x1, y1 = xyxy[0]
        x2, y2 = xyxy[1]
        x_center = ((x1 + x2) / 2) / w
        y_center = ((y1 + y2) / 2) / h
        bbox_w = (x2 - x1) / w
        bbox_h = (y2 - y1) / h
        return x_center, y_center, bbox_w, bbox_h
