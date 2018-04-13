import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from AutoDW import *


class SearchEngineBase(MyAbstractClass):
    abstract_methods = ('search', 'parse_magnet_results', 'parse_torrent_results')
