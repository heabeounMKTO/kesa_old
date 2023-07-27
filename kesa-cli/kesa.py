import os
from pathlib import Path
from urllib.parse import urljoin
import json
import requests


class Kesa:
    def __init__(self) -> None:
        pass

    def convertsingle(
        self,
        json_path: str,
        model_name: str,
        general_cfg,
        target_format: str = "yolo",
        augment: int = 0,
        save_folder="_kesatemp",
        export_folder="export",
    ):
        """
        convert single labelme json file
        to yolo .txt format
        """
        jsonFile = json.load(open(json_path))
        fullurl = urljoin(
            general_cfg["address"], f"convertLabel/{target_format}/{model_name}"
        )
        if augment == 0:
            modJson = jsonFile.copy()
            del modJson["imageData"]
            # makes copy and deletes
            # image data b64 for bandwidth savings
            # don't need image modifications
            r = requests.post(
                fullurl,
                json={
                    "labelme_json": modJson,
                    "model_name": model_name,
                    "augment": f"{augment}",
                },
            )
        else:
            r = requests.post(
                fullurl,
                json={
                    "labelme_json": jsonFile,
                    "model_name": model_name,
                    "augment": f"{augment}",
                },
            )
        result = eval(r.text)
        return result
