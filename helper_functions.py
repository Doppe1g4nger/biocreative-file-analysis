import os.path as path
from os import listdir


def get_all_files(fpath):
    return [path.join(fpath, f) for f in listdir(fpath) if path.isfile(path.join(fpath, f))]
