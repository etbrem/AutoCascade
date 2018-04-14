import sys
import os
MAIN_DIRECTORY = os.path.dirname(os.path.dirname(__file__)) or ".."
sys.path.append(MAIN_DIRECTORY)
from auto_cascade import *
from downloader_base import DownloaderBaseClass

import requests


class Downloader(DownloaderBaseClass):
    HOST = 'localhost'
    PORT = 8080

    def __init__(self, host=HOST, port=PORT, username='', password=''):
        self.host = host
        self.port = port
        self.url = 'http://{host}:{port}/'.format(**locals())
        self.username = username
        self.password = password
        self.cookies = {}

        if self.username:
            params = {
                'username': self.username,
                'password': self.password
                }

            response = requests.post(self.url + 'login', data=params)
            if response.text == "Ok.":
                self.cookies = response.cookies
            else:
                raise Exception("qBittorrent authentication failed")

    def add_torrent_file(self, path):
        pass

    def add_magnet_link(self, magnet, **kargs):
        params = {
            'urls': magnet.link,
            'root_folder': True
        }

        if 'destination' in kargs:
            params['savepath'] = kargs['destination']

        if 'rename' in kargs:
            params['rename'] = kargs['rename']
        else:
            params['rename'] = magnet.title

        response = requests.post(self.url + 'command/download', cookies=self.cookies, data=params, files=dict(foo='bar'))
        if response.text != "Ok.":
            return False
        return True

if __name__ == "__main__":
    link = r'magnet:?xt=urn:btih:264886d841442158b3efc861bbfca5ef91d8f68b&dn=Mr.Robot.S02E01.720p.WEBRip.AAC2.0.H.264-KNiTTiNG%5Bettv%5D&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Fzer0day.ch%3A1337&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969'
    magnet = Magnet('test', link)

    a = Downloader(username='admin', password='abcd1234')
    a.add_magnet_link(magnet)

