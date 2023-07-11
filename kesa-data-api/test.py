from kesa_utils import ModelUtils
import configparser


config = configparser.ConfigParser()
config.read("configs/auto-labelcfg.ini")

test = ModelUtils().getAllModelInfoFromConfig(config)
