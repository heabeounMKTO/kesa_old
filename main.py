from art import text2art
import argparse
import typer
import imgutils
from pathlib import Path
from folderutils import get_image_files

def main():
    format = typer.prompt(text2art("kesa-img", font="Slanted"), "enter data format")
    
    if format == "yolov7":
        
        data_folder = typer.prompt("enter LabelMe labeled data path")
        data_folder = Path(data_folder)
        print("found images: ", len(get_image_files(data_folder)), f"in path: {data_folder}")
        
        
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
    