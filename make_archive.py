import shutil
import subprocess
import os
import sys


location_rar = r"C:\Program Files\WinRAR\rar.exe"
location_7z = r"C:\Program Files\7-Zip\7z.exe"
dirname = r'D:\shared\alternate\SQ016_SH002_v07'

import logging
class ProgressHandler(logging.StreamHandler):
    def emit(self, record):
        print "h"


logger = logging.getLogger(__name__)
logger.addHandler(ProgressHandler(sys.stdout))
logger.setLevel(logging.DEBUG)

def make_archive(dirname=dirname, format='rar'):
    '''This function 
    makes an archive
    this is a long docstring'''

    dirname = os.path.normpath(dirname)
    while dirname.endswith(os.sep):
        dirname = dirname[:-1]

    def remove(dirname, ext):
        archive = dirname + ext
        if os.path.exists(archive):
            os.remove(archive)
        return archive

    if format=='rar':
        archive = remove(dirname, '.rar')
        subprocess.check_output([location_rar, "a", "-m1", "-ep1", archive,
            dirname])

    elif format=='7z':
        archive = remove(dirname, '.7z')
        subprocess.check_output([location_7z, "a", "-t7z", "-mx=7", archive, dirname])

    elif format == 'zip':
        archive = remove(dirname, '.zip')
        shutil.make_archive(dirname, format, dirname, verbose=1, logger=logger)

    elif format == 'bztar':
        archive = remove(dirname, '.tar.bz2')
        shutil.make_archive(dirname, format, dirname, verbose=1, logger=logger)

    elif format == 'gztar':
        archive = remove(dirname, '.tar.gz')
        shutil.make_archive(dirname, format, dirname, verbose=1, logger=logger)

    return archive



def call_7z():
    ''' call 7z and record output '''

    def remove(dirname, ext):
        archive = dirname + ext
        if os.path.exists(archive):
            os.remove(archive)
        return archive

    def countFiles(dirname):
        if not os.path.exists(dirname):
            return 0
        if not os.path.isdir(dirname):
            return 1
        numfiles = 0
        for dirpath, dirnames, filenames in os.walk(dirname):
            numfiles += len(filenames)
        return numfiles

    def printProgress(done, total):
        sys.stdout.write("\r%d of %d: %f%%" % (done, total,
            done*100.0/total))

    archive = remove(dirname, '.7z')
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    command = [location_7z, "a", "-t7z", "-mx=2", archive, dirname]
    print command
    process = subprocess.Popen(command, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            bufsize=0,
            startupinfo=startupinfo,
            shell=True)


    total = countFiles(dirname)
    done = 0
    print
    printProgress(done, total)

    for line in iter(process.stdout.readline, b''):
        if line.startswith('Compressing'):
            done += 1
            printProgress(done,total)
    print
    print "Done"


if __name__ == '__main__':
    make_archive(format='zip')
