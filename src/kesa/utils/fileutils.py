import os 
from pathlib import Path
import shutil


class FileUtils():
    def __init__(self, destinationFolder):
        self.destinationFolder = destinationFolder


    def createOutputFolder(self):
        
