# ==================================================
# @author: Runxin runxinw@vmware.com
#

import vmgmtstorage

if __name__ == '__main__':
    
    dpath = '/home/rwang/workspace/gssnsx/spack'
    array = vmgmtstorage.get_all_files(dpath)
    print array