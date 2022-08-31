
import os.path
from enum import Enum

ROOT_DIR= os.path.dirname(os.path.abspath(__file__))
CONF = {}
LOGGER_CONF = {}
FORCE_RELOAD:bool = False
USE_PROXY:bool = False
MULTIPLE_BPNS:bool = False  

class Status(Enum):
    NEW = 1
    TWINLOADED = 2
    TESTED = 3

def set_conf(test):
    global CONF
    CONF = test

def set_force_reload(b:bool):
    global FORCE_RELOAD
    FORCE_RELOAD = b

def set_use_proxy(p:bool):
    global USE_PROXY
    USE_PROXY = p

def set_multiple_bpns(c:bool):
    global MULTIPLE_BPNS
    MULTIPLE_BPNS = c

def set_logger_conf(conf):
    global LOGGER_CONF
    LOGGER_CONF = conf