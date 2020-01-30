import subprocess
import sys
import string


proc = subprocess.Popen(['time'], stdout=subprocess.PIPE, shell=True)

while 1:
    line = ''
    while 1:
        data = proc.stdout.read(1)
        sys.stdout.write(data)
        if data in '\n':
            break
        if data != '\r':
            line += data
    if len(line)==0:
        print ( 'BREAK' )
        break
    proc.kill()

