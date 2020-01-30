#mainmodule.py
import os
import sys
import inspect
import __main__

try:
    print __file__
except:
    print 'error'

print os.curdir
print sys.argv
print inspect.getfile(__main__)
print __main__.__file__

