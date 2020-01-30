import os

path_template = r'P:\external\Al_Mansour_Season_03\02_production\ep%02d\ASSETS'
ep_assets_paths = [path_template%d for d in range(1, 12)]


for path in ep_assets_paths:
    for dirpath, dirnames, filenames in os.walk(path):
        if os.path.basename(dirpath) == 'archive':
            files = [os.path.join(dirpath, f) for f in filenames]
            for fn in files:
                print fn
