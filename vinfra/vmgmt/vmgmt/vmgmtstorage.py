'''
Created on 11 Nov 2018

@author: rwang
'''

import os 


def get_all_files(dpath):
    from os.path import isfile, isdir, join
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


if __name__ == '__main__':
    
    dpath = '/home/rwang/workspace/gssnsx/spack'
    array = get_all_files(dpath)
    print array
        