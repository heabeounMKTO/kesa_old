import os
from CutLabel import labelCut 
from art import *

print(text2art("kesa"))


def main():
    checkOutputFolder()
    test = labelCut("imgs", "random")
    test.randomBgFromLabelme()


def checkOutputFolder():
    folders = ["random", "output"]
    print("looking for required folders")
    for folder in folders:
        if not os.path.exists(folder):
            print("folder ", folder, " not found, creating..")
            os.makedirs("folder")
        else: 
            print("folder ", folder, " found, skipping creation..")


if __name__ == "__main__":
    main()
