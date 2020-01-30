import os
import json
from collections import OrderedDict

import requests
import webbrowser
import urlparse
import urllib

appdata = {
"key": "09a4f53ad33237315071ec225addf4e7",
"secret": "05fd0465d26ae98cb514fa477dfdb78f267b0b13792d9444ac7c9d1975fb121e",
'token':'387ab0444983f2bdf263b0a0e2721f7de9d94827f29f1cd50e4b9ca9568c863d'
}


class TriceConfig(object):
    rcfile = os.path.join(os.path.expanduser('~'), '.tricerc')
    data = appdata.copy()

    def __init__(self):
        self.readFromFile()

    def writeToFile(self):
        with open(self.rcfile, 'w') as myrc:
            json.dump(self.data, myrc, indent=2)

    def readFromFile(self):
        try:
            with open(self.rcfile) as myrc:
                self.data = json.load(myrc)
        except (IOError, ValueError):
            pass


class Trice():
    baseurl = 'https://trello.com/1/'

    def __init__(self):
        self.conf = TriceConfig()

    def authorize(self):
        url = urlparse.urljoin(self.baseurl, 'authorize?')
        params = OrderedDict()
        params['key'] = self.conf.data['key']
        params['name'] = 'Trice'
        params['expiration'] = 'never'
        params['scope'] = 'read,write'
        params['response_type'] = 'token'
        url += '?' + urllib.urlencode(params)
        webbrowser.open_new_tab(url)

        token = raw_input("Enter token: ")
        self.conf.data['token'] = token
        self.conf.writeToFile()

    def getBoards(self):
        url = urlparse.urljoin(self.baseurl, '/'.join(['members', 'my',
            'boards']))
        params = OrderedDict()
        params['key'] = self.conf.data['key']
        params['token'] = self.conf.data['token']
        params['fields']='name'
        boards_requests = requests.get(url, params=params)
        data = boards_requests.json()
        print len(data), 'boards'
        for board in data:
            print board['name']

if __name__ == '__main__':
    trice = Trice()
    trice.getBoards()
