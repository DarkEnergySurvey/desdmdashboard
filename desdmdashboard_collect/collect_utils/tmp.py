
import os


DEFAULT_TEMPDIR = '~/.desdmdashboard_collect/tmp/'


def find_or_create_tmp_dir(path=DEFAULT_TEMPDIR):
    if not os.path.exists(path): os.makedirs(path)
    return path 

def open_tmp_file(filename, path=DEFAULT_TEMPDIR):
    fid = open('r')

    return (exists, fid)

