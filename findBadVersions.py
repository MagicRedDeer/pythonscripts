import sys
sys.path.append(r'r:\Pipe_Repo\Projects\TACTIC')
sys.path.append(r'r:\Python_Scripts\plugins')

import auth.user
auth.user.login('tactic', 'tactic123')

import app.util as util
import os, re, shutil

util.get_server().set_project('mansour_s03')
asset_path = r'P:\external\Al_Mansour_Season_03\assets'
prod_path = r'P:\external\Al_Mansour_Season_03\02_production'

version_pattern = re.compile(r'.*v\d{3}.*')
swatch_pattern = re.compile(r'.*swatch.*', re.I)
link_pattern = re.compile(r'.*\.link')
bak_pattern = re.compile(r'.*\.bak')
def findBadVersions(startpath):
    bad_versions = []
    for dirpath, dirnames, filenames in os.walk(startpath):

        for name in ['archive', 'sources']:
            try: dirnames.remove(name)
            except: pass

        for fn in filenames:

            if swatch_pattern.match(fn):
                continue
            if link_pattern.match(fn):
                continue

            if version_pattern.match(fn):
                fp = os.path.join(dirpath, fn)
                fobj = util.get_fileobj_from_path(fp)
                if not fobj:
                    bad_versions.append(fp)
                    yield fp

def backup(path):
    dirname, fn = os.path.split(path)

    archdir = os.path.join(dirname, 'archive')
    if not os.path.exists(archdir):
        os.mkdir(archdir)
    try:
        shutil.move(path, os.path.join(archdir, fn))
    except Exception as e:
        print 'Error', e, path

# for ver in findBadVersions(asset_path):
    # print ver
    # backup(ver)

for ver in findBadVersions(prod_path):
    print ver
    # backup(ver)

