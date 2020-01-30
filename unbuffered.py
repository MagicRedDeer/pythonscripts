'''a module'''
import subprocess
import os

def blurt(data):
    '''prints stuff'''
    print data.strip()


COMMAND = ['python', 'subprogram.py']

# os.chdir(r'd:\shared')
# COMMAND = [r"C:\Program Files\WinRAR\rar.exe", "a", "-m1", "EP002.rar", "EP002"]

CHILD = subprocess.Popen(COMMAND, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

for line in iter(CHILD.stdout.readline, b''):
    blurt(line)

