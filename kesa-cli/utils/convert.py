import os
import math
import tqdm
from utils.file_utils import kesaFileCliUtils as KFC 



class Labelme2Yolo:
    def __init__(self) -> None:
        pass
    def convert_single_request(self,json_file):
        image_path , image_b64 = KFC().getImagePathandBase64FromJson(json_file)
        return image_path, image_b64 
        
