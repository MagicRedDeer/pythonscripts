import pprint 
from shotgun_api3 import Shotgun

def test():
    print Shotgun

    SERVER_PATH = 'https://iceanimations.shotgunstudio.com'
    SCRIPT_NAME = 'TestScript'     
    SCRIPT_KEY = '446a726a387c5f8372b1b6e6d30e4cd05d022475b51ea82ebe1cff34896cf2f2'
    PROXY = '10.10.0.212:8080'

    print "hello1"
    sg = Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY, PROXY)
    print "hello2"
    pprint.pprint([symbol for symbol in sorted(dir(sg)) if not symbol.startswith('_')])
    print "Hello3"
test()
