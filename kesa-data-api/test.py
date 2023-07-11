import configparser

from kesa_utils import ModelUtils

config = configparser.ConfigParser()
config.read("configs/auto-labelcfg.ini")

test = ModelUtils().getAllModelInfoFromConfig(config)
