#!/usr/bin/env python

# ==================================================
# @author: Runxin runxinw@vmware.com
#

import os

def deploy_ova(ova, ip, hostname, portgroup, user, password):
    cmd = 'ovftool --acceptAllEulas'
    net =  '--net:"OVF-Builder"='+portgroup
    disk = '--diskMode=thin'
    name = '--name='+ hostname
    ova = ova + ' vi://root:pass@10.10.10.10'
    os.system(cmd)
    
if __name__ == '__main__':
    pass