import requests
import configparser
import os
from urllib.parse import urljoin, urlparse
import json




def read_config():
    config = configparser.ConfigParser()
    config.read("cfg.ini")        
    general_cfg = {
    "address": config["NETWORK"]["ADDRESS"],
    }
    return config, general_cfg

_penis , bussy = read_config()

def getAddrFromCfg():
    return bussy.get("address") 

def getAllModels():
    kdouyayeas = requests.get('http://localhost:6969/modelinfo')
    print(kdouyayeas.text)
getAllModels()
    


