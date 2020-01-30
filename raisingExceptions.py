import types
import traceback
import sys


class MyException(Exception):

    def __init__(self, *args):
        print 'MyException ::', args
        super(MyException, self).__init__(args[0])

    def __str__(self, args):
        pass

def investigate(ex):
    for thing in dir(ex):
        print thing,
        if thing.startswith('_'):
            print
            continue
        attr = getattr(ex, thing)
        if hasattr(attr, '__call__'):
            print attr()
        else:
            print repr(attr)

try:
    # raise MyException('just raising!')
    raise MyException, 'just raising', sys.exc_info
    # raise Exception('just raising', 'doing something ', 'papaa')
    # raise MyException('just raising', 'doing something ', 'papaa')
except Exception as e:
    investigate(e)
    print sys.exc_info()[2]

