import sys
import os
MAIN_DIRECTORY = os.path.dirname(os.path.dirname(__file__)) or ".."
sys.path.append(MAIN_DIRECTORY)
from auto_cascade import *


class DownloaderBaseClass(MyAbstractClass):
    abstract_methods = ('add_magnet_link', 'add_torrent_file')


