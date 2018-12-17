# ==================================================
# @author: Runxin runxinw@vmware.com
#

#from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import os
from os.path import isfile, isdir, join

'''
Refs:
http://vthinkbeyondvm.com/pyvmomi-tutorial-how-to-get-all-the-core-vcenter-server-inventory-objects-and-play-around/
'''

class InventoryManager():
    
    def __init__(self,host,user,passwd):
        """
        session is the object connected to vcenter or host
        """
        self.host = host
        self.user = user
        self.password = passwd
        self.session = None 
        self.content = None
        self.port = None
    
    def set_port(self, port):
        self.port = port
        
    def get_port(self, port):
        return self.port
    
    def connect_server(self, port=None):
     
        try:
            if self.port != None:
                #self.session = SmartConnectNoSSL(host=self.host,user=self.user,pwd=self.password,port=int(self.port))
                self.session = SmartConnect(host=self.host, user=self.user, pwd=self.password, port=int(self.port))
            else:
                #self.session = SmartConnectNoSSL(host=self.host,user=self.user,pwd=self.password) 
                self.session = SmartConnect(host=self.host, user=self.user, pwd=self.password, port=443)
        
        except vim.fault.InvalidLogin:
        #except:
            raise SystemExit("Unable to connect to host with supplied credentials.")

        self.content = self.session.RetrieveContent()

    def get_all_vms(self):
        vms = {}
        vimtype = [vim.VirtualMachine]
        
        if self.session == None or self.content == None:
            raise SystemExit("session is not yet established")

        container = self.content.viewManager.CreateContainerView(self.content.rootFolder, vimtype, True)
        for managed_object_ref in container.view:
                vms.update({managed_object_ref:managed_object_ref.name})
        return vms
             
"""
  retired codes

    def printvminfo(self, vm, depth=1):
      
    # if this is a group it will have children. if it does, recurse into them
    # and then return
        if hasattr(vm, 'childEntity'):
            if depth > MAX_DEPTH:
                return
        
        vmlist = vm.childEntity
        for child in vmlist:
            self.printvminfo(child, depth+1)
        return

    def get_all_vms2(self):
        for child in self.content.rootFolder.childEntity:
            if hasattr(child, 'vmFolder'):
                datacenter = child
                vmfolder = datacenter.vmFolder
                vmlist = vmfolder.childEntity
                for vm in vmlist:
                    self.printvminfo(vm)
"""

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