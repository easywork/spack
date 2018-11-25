# ==================================================
# @author: Runxin runxinw@vmware.com
#

import os 
from os.path import isfile, isdir, join

def get_all_files(dpath):
    array = []
    dirs = []

    for f in os.listdir(dpath):
        
        # ignore the hidden file
        if f.startswith('.'):
            continue
        
        fullname = join(dpath,f)
        if isfile(fullname):
            array.append(f)
        elif isdir(fullname):
            dirs.append(fullname)
    
    if len(dirs) == 0:
        return array
    else:
        for d in dirs:
            t = get_all_files(d)
            array.extend(t)
        return array  

def get_files(dpath):
    array = []
    for f in os.listdir(dpath):
        if f.startswith('.'):
            continue
            array.append(f)
    return array 


if __name__ == '__main__':
    
    import sys
    dpath = sys.argv[1]
    array = get_files(dpath)
    print array
        
