from art import text2art
import argparse
import typer
import imgutils


def main():
    typer.prompt(text2art("kesa", font="Slanted"))
    
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
    