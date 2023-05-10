import os
from pathlib import Path
from labelme2yolo.labelme2yolo import Labelme2Yolo as L2Y

# from auto_label.autolabel import AutoLabel
import typer


def augmentImage(processingfolder: str, number_of_variations: int):
    print(
        f"creating augmentations in folder {processingfolder} , with {number_of_variations} of variations"
    )


def main(operationmode: str, processingfolder: str):
    operationmode.lower()
    match operationmode:
        case "augment":
            augmentImage(processingfolder)


if __name__ == "__main__":
    typer.run(main)
