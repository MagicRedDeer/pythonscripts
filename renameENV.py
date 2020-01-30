import glob

import os

# print glob.glob(os.path.abspath( os.curdir ) + "/**/ENV")

def func( *args, **kwargs ):
    print args
    print kwargs

# print os..walk( os.curdir, func, [] )


def renameEnv():
    for folder, dirs, files in os.walk(os.curdir):
        for _dir in dirs:
            if 'ENV' in _dir:
                old = os.path.join(os.path.abspath(folder), _dir)
                new = os.path.join(os.path.abspath(folder), _dir.replace('ENV',
                    'environ'))
                # os.rename( old, new )
                print 'rename', old, '=>', new

if __name__ == "__main__":
    renameEnv()
