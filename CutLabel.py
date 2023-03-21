import os
import cv2
import json
from pathlib import Path
import numpy as np
import random
import uuid
import tqdm

class labelCut:
    def __init__(self, folder,randomImgFolder,randomImageArray=None, jsonArray=None,imageArray=None):
        self.folder = folder
        self.jsonArray = jsonArray
        self.imageArray = imageArray
        self.randomImgFolder = randomImgFolder
        
    def lookForJson(self, folder):
        folder = Path(self.folder)
        jsons = []
        for roots, dir, files in os.walk(folder):
            for file in files:
                if file.endswith(".json"):
                    h=(os.path.join(os.getcwd(), folder))
                    jsons.append(os.path.join(h, file))
        self.jsonArray = jsons
        
        return self.jsonArray


    def readImageFromLabelme(self):
        imagefiles = []
        
        jsons = self.lookForJson(self.folder)
        '''
        handles image path reading errors... some of my files are not
        from the same machine so the local paths are different.. feel free to modify the 
        codes, or just open and save your labeled images in the same machine 
        '''
        for jsonfile in jsons:
            imagePath = ""
            # extension = os.path.splitext(Path(json.load(open(jsonfile))['imagePath']))[1]       
            localDir = Path(json.load(open(jsonfile))['imagePath'])
            if localDir != "":
                imagePath = (json.load(open(jsonfile))['imagePath']) 
            else:
                continue        
            frontpath = Path(os.path.join(os.getcwd(),self.folder))
            
            fullpath = os.path.join(frontpath, imagePath)
            imagefiles.append(fullpath)
        print("found ", len(imagefiles), " images")
        self.imageArray = imagefiles
        return imagefiles
     
    def getRandomBackground(self):
        randomimg = []
        imgfmts = (".jpg", ".jpeg", ".png")
        for root, dirs, files in os.walk(self.randomImgFolder):
            for file in files:
                if file.endswith(imgfmts):
                    randomimg.append(os.path.join(os.getcwd(), (self.randomImgFolder + "/" + file)))
        print(f"found {len(randomimg)} images from random index")
        return randomimg


    def randomBgFromLabelme(self):
        self.readImageFromLabelme() #load json
        randomimg = self.getRandomBackground()
        count = 0
        for index, label in enumerate(tqdm.tqdm(self.jsonArray)): 
            loadjson = json.load(open(label))
            filename = os.path.splitext(loadjson["imagePath"])[0]
            imgpath = os.path.join(self.folder, loadjson["imagePath"])
            img = cv2.imread(imgpath)
            blackbg = np.zeros((img.shape[0], img.shape[1], 3))
            shape = loadjson["shapes"]            
            for label in shape:
                pts = label["points"]
                mask = np.array(pts, np.int32)
                alpha = cv2.fillPoly(blackbg, pts = [mask], color=(255,255,255))
                _, alpha = cv2.threshold(alpha, 0,255,cv2.THRESH_BINARY)
                alpha = alpha.astype(np.uint8)
                alpha = cv2.cvtColor(alpha, cv2.COLOR_BGR2GRAY)
                cAlpha = cv2.merge([alpha,alpha,alpha])
                b,g,r = cv2.split(img)
                ptCutout = cv2.merge([b,g,r,alpha], 4)
                front = ptCutout[:,:,0:3] 
                try:
                    randimg = cv2.imread(randomimg[random.randint(0,8)])
                except:
                    randimg = cv2.imread(randomimg[0])
                randimg = cv2.resize(randimg,(img.shape[1], img.shape[0]))
                result = np.where(cAlpha==(0,0,0), randimg, front)
                cv2.imwrite(f"output/{filename}.png", result)


            
