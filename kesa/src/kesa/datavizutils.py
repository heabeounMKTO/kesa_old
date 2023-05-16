import psycopg2
import os
import json
import random
from sqlutils import SqlUtils
import uuid
import tqdm
class DataVizUtils():
    def __init__(self, input):
        self.input = input

    def getAllLabelsInFolder(self):
        for root,dirs,files in os.walk(self.input):
            for file in tqdm.tqdm(files):
                if file.endswith(".txt"):
                    info_dict = {
                            "labelid":uuid.uuid4().hex,
                            "labels": "test",
                            "label_count": random.randint(0,20),
                            "game_type": "penis"
                            }
                    db = SqlUtils()
                    db.insertData(info_dict)
                    # print(info_dict)


testfolder = "exports"
test = DataVizUtils(testfolder)
test.getAllLabelsInFolder()
