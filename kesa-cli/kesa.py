import requests
import configparser
from urllib.parse import urljoin, urlparse
import json
from functools import reduce 
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--config', type=str)


def read_config():
    config = configparser.ConfigParser()
    config.read("cfg.ini")        
    general_cfg = {
    "address": config["NETWORK"]["ADDRESS"],
    }
    return config, general_cfg

_penis , bussy = read_config()


def getAllModels():
    fulladdr = urljoin(bussy.get("address"), '/modelinfo')
    kdouyayeas = requests.get(fulladdr)
    result = json.loads(kdouyayeas.text)
    print(result["available_models"])

getAllModels()
    


