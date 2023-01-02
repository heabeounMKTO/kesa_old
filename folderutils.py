from pathlib import Path
import os


def get_image_files(path):
    image_list = list()
    for root, dir, files in os.walk(Path(path)):
        for file in files:
            image_list.append(Path(root+file))
            

    return image_list


get_image_files("F:\\kesa\\tests\\yolov67\\train\\images")
