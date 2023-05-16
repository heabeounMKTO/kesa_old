import os
from pathlib import Path
from kesa import Kesa
import typer

app = typer.Typer()

KESA = Kesa()


@app.command()
def convert2yolo(input: str, output: str):
    """
    convert labelme annotations to YOLO format

    """
    KESA.setMode("convert Labelme to Yolo")
    KESA.kesaConvertLabelme2Yolo(input, output)


@app.command()
def autolabel(input: str, conf: float = 0.9, iou: float = 0.7):
    """
    auto-labels specified folder , in  labelme JSON format
    """
    KESA.setMode("autolabel")
    KESA.kesaAutoLabel(input, conf, iou)


@app.command()
def end2end(input: str, output: str, conf: float = 0.9, iou=0.7):
    """
    end to end conversion of raw images to YOLO format annotations
    """
    KESA.setMode("end to end conversion")
    KESA.kesaEnd2EndConversion(input, output, conf, iou)


@app.command()
def convert2yoloaug(input: str, output: str, time: int):
    KESA.setMode(f"convert labelme to yolo with augmentations")
    KESA.kesaConvertLabelme2Yolo_aug(input, output,time)


if __name__ == "__main__":
    app()
