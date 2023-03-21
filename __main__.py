import os
from CutLabel import labelCut 
from art import *

print(text2art("kesa"))

def checkOutputFolder():
    folders = ["random", "output"]
    print("looking for required folders")
    for folder in folders:
        if not os.path.exists(folder):
            print("folder ", folder, " not found, creating..")
            os.makedirs("folder")
        else: 
            print("folder ", folder, " found, skipping creation..")



checkOutputFolder()
test = labelCut("imgs", "random")
test.randomBgFromLabelme()
