import json 
import os
from CutLabel import labelCut
import yaml


class convertLabelme:
    def __init__(self,imgfolder, jsonList=None, label_list=None):
        self.jsonList = labelCut(imgfolder,None).lookForJson()
    
    def loadLabelFile(self):
        with open("labels.yaml") as file:
            labellist = yaml.load(file, Loader=yaml.FullLoader)
        self.label_list = labellist

    def getLabels(self):
        labels_list = []
        for jsonfile in self.jsonList:
            jsonfile = json.load(open(jsonfile))
            for labels in jsonfile["shapes"]:
               labels_list.append(labels["label"])
        labels_list = list(dict.fromkeys(labels_list))
        labels_list = sorted(labels_list)
        return labels_list

    def writeLabelList(self):
        labels = self.getLabels()
        with open('labels.yaml', 'w') as file:
             yaml.dump(labels, file)
        self.loadLabelFile()

    def convert2YOLO(self):
        labels = []
        """look for labels.yml"""
        if not os.path.exists("labels.yaml"):
            print("create label file from data")
            self.writeLabelList()
        else:
            self.loadLabelFile()
        
        """normalize coordinates to picture and convert to yolo"""

        for json_file in self.jsonList:
            lmjson = json.load(open(json_file))
            shape = lmjson["shapes"]
            for i in range(len(shape)):
                label = self.label_list.index(shape[i]["label"])
                labels.append([str(label)])
                for points in shape[i]["points"]:
                    xNorm = points[0]/lmjson["imageWidth"]
                    yNorm = points[1]/lmjson["imageHeight"]
                    labels[i].append(str(xNorm))
                    labels[i].append(str(yNorm))
            filename = os.path.splitext(lmjson["imagePath"])[0]
            with open(f"c/{filename}.txt", "w") as file:
                for i in range(len(labels)):
                    for x in labels[i]:
                        file.write(x)
                        print(x)
                        file.write(" ")
                    file.write('\n')

        # print(len(labels))
        # print(labels)

cv = convertLabelme("imgs").convert2YOLO()
