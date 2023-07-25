import configparser
class CfgUtils:
    def __init__(self) -> None:
        pass

    def read_config(self):
        config = configparser.ConfigParser()
        try:
            config.read("cfg.ini")        
            general_cfg = {
            "address": config["NETWORK"]["ADDRESS"],
            }
            return config, general_cfg
        except FileNotFoundError as nofile:
            print(f"{nofile}")
