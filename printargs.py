import sys
import time
import threading

from PyQt4.QtCore import QThread

def printstuff(*args):
    print sys.version
    print sys.argv
    print sys.executable

class Thread(QThread):
    def run(self):
        printstuff()

if __name__ == '__main__':
    printstuff()
    t = threading.Thread(target=printstuff)
    t.start()
    time.sleep(1)


