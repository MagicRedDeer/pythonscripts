import sys

sys.path.append(r'D:\talha.ahmed\workspace\pyenv_maya\tactic')

from threading import Thread
import threading

import tactic_client_lib

def make_stub():
    return tactic_client_lib.TacticServerStub(login='talha.ahmed',
            password="lovethywife", server='tacticvm',
            project='captain_khalfan')

class Doer(Thread):
    def __init__(self, func, *args):
        Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)

class Counter(object):
    def __init__(self):
        self.rlock = threading.RLock()
        self.count = 0

    def inc(self):
        with self.rlock:
            self.count += 1

    def get(self):
        return self.count

count = Counter()

def get_icon_snap(sobject):
    stub = make_stub()
    snap = stub.get_snapshot(sobject, context='icon')
    print sobject['__search_key__'], True if snap else False
    count.inc()

stub = make_stub()
objs = stub.query('vfx/asset')

from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=20)
#pool.map(get_icon_snap, objs)

for obj in objs:
    #d=Doer(get_icon_snap, obj)
    pool.apply_async(get_icon_snap, args=(obj,))

import time
while(count.get() < len(objs)):
    time.sleep(0.1)

