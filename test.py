import os
import cv2
import json
from pathlib import Path
import numpy as np
import random
import uuid

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
        print(jsons)
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
            imageName = ""
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
        print(self.jsonArray)
        for index, label in enumerate(self.jsonArray): 
            loadjson = json.load(open(label))
            try:
                pts = loadjson["shapes"][index]["points"]
                mask = np.array(pts, np.int32)
                img = cv2.imread(self.imageArray[index])
                blackbg = np.zeros((img.shape[0], img.shape[1], 3))
                gg = cv2.fillPoly(blackbg, pts = [mask], color=(255,255,255))
                gg = gg.astype(np.uint8)
                
                result = cv2.cvtColor(cv2.bitwise_and(img, gg), 1)
                _,alpha = cv2.threshold(result, 0, 255, cv2.THRESH_BINARY)
                
                cv2.imwrite(f"test/t{uuid.uuid4()}.png", alpha)
                alpha = cv2.cvtColor(alpha, cv2.COLOR_BGR2GRAY)
                b,g,r = cv2.split(img)
                rgba = [b,g,r,alpha]
                dst = cv2.merge(rgba,4)
                
                loadrandimg = cv2.imread(randomimg[random.randint(0, len(randomimg))])
                loadrandimg = cv2.resize(loadrandimg, (img.shape[1], img.shape[0]))
                
                alpha = cv2.merge([alpha,alpha,alpha])
                front = dst[:,:,0:3]
                result = np.where(alpha==(0,0,0), loadrandimg, front)
                    
            except:
                continue

test = labelCut(folder="imgs", randomImgFolder="random")
test.randomBgFromLabelme()
