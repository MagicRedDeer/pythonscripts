import sys
import subprocess
import time
import functools
import os

def producer():
    print os.isatty(sys.stdout.fileno())
    for f in range(100):
        print "\b\b\b\b%d%%"%f,
        time.sleep(0.1)
    print "\b\b\b\b100%"

def consumer():
    child = subprocess.Popen([sys.executable, __file__],
            stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    func = functools.partial(child.stdout.read, 1)
    for b in iter(func, b''):
        sys.stdout.write(b)

if __name__ == '__main__':
    if '1' in sys.argv:
        consumer()
    else:
        producer()

