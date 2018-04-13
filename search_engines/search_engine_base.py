import sys
import os
MAIN_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
sys.path.append(MAIN_DIRECTORY)
from auto_cascade import *


class SearchEngineBaseClass(MyAbstractClass):
    abstract_methods = ('search', 'parse_magnet_results', 'parse_torrent_results')
