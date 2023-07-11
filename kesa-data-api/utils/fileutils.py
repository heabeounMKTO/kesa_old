import os
import shutil
from pathlib import Path


class FileUtils():
    def __init__(self, destinationFolder):
        self.destinationFolder = destinationFolder


    def createOutputFolder(self):
        
