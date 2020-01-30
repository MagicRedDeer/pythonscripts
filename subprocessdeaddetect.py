import subprocess
import os

def communicate(proc):
    while 1:
        if proc.poll() is not None:
            break
        line = proc.stdout.readline()
        print line

def launch_process():
    command = [
            # 'python',
            r"c:\Program Files\Autodesk\Maya2015\bin\mayapy.exe",
            '-c',
            '''
import time
import sys
for i in range(10):
    time.sleep(2)
    sys.stdout.write( "line %d\\r\\n" % i )
    sys.stdout.flush()
''']
    print command
    print command[2]
    startupinfo = None
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    proc = subprocess.Popen(command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE, startupinfo=startupinfo)

    return proc

if __name__ == "__main__":
    proc = launch_process()
    communicate(proc)
    print 'done'
