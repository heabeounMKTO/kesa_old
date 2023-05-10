import albumentations as A
import cv2


class augmentImage:
    def __init__(self, imagePath,bbox_coords,labellist):
        self.image = cv2.imread(imagePath)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.bbox_coords = bbox_coords
        self.labellist = labellist



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
        return transformed
