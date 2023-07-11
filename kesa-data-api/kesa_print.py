import pprint

import rich

"""
this file is unnecessary but i need it ok
"""


class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def kesaLog(msg, bold=False):
    if bold != False:
        print(color.BOLD + color.GREEN + "[🍑 INFO]: " + color.END + msg + color.END)
    else:
        print(color.GREEN + "[🍑 INFO]: " + color.END + msg)


def kesaError(msg):
    print(color.RED + "[🚨 ERROR]: " + color.END + msg)


def kesaPrintDict(notify_string, input_dict):
    """
    this fucking function is not used
    for anything else other than config printing smh ,
    will refactor later (maybe? idk im lazy)
    """
    kesaLog(notify_string)
    for items in input_dict.items():
        print(f"\033[1m{color.YELLOW}[💞 CONFIG] {items[0]} : {items[1]} \033[0m ")
