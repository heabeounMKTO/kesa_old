import json 
import os
from CutLabel import labelCut
import yaml


loadJson = labelCut("imgs", "random").lookForJson()

def getLabels():
    labels_list = []
    for jsonfile in loadJson:
        jsonfile = json.load(open(jsonfile))
        for labels in jsonfile["shapes"]:
           labels_list.append(labels["label"])
    labels_list = list(dict.fromkeys(labels_list))
    labels_list = sorted(labels_list)
    return labels_list

def writeLabelList():
    labels = getLabels()
    with open('labels.yaml', 'w') as file:
         yaml.dump(labels, file)
writeLabelList()
