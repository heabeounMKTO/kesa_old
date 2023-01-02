from art import text2art
import argparse
import typer
import imgutils
from pathlib import Path

def main():
    format = typer.prompt(text2art("kesa-img", font="Slanted"), "enter data format")
    
    if format == "yolov7":
        print("converting to v7 format...")
        data_folder = typer.prompt("enter LabelMe path")
        data_folder = Path(data_folder)

app = typer.Typer()

@app.command()
def greyscale(img, save_file=False):
    print("img", img)
    # gs = imgutils.toGreyScale(img)
    # return gs
    

@app.command()
def flip(img, save_file=False):
    print("img", img)
    # gs = imgutils.toGreyScale(img)
    # return gs
    
    

while True:
    typer.run(main)
    