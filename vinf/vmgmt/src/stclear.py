#!/usr/bin/env python
#from __future__ import print_function
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim
import sys, getopt
# from __builtin__ import None

#import pyVmomi

'''
Refs:
http://vthinkbeyondvm.com/pyvmomi-tutorial-how-to-get-all-the-core-vcenter-server-inventory-objects-and-play-around/
'''

MAX_DEPTH = 10

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
        '''
        s=ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        s.verify_mode=ssl.CERT_NONE
        si= SmartConnect(host="10.192.3.2", user="Administrator@vsphere.local", pwd="$h1vKamal",sslContext=s)
        content=si.content
        '''
        try:
            if self.port != None:
                self.session = SmartConnectNoSSL(host=self.host,user=self.user,pwd=self.password,port=int(self.port))
            else:
                self.session = SmartConnectNoSSL(host=self.host,user=self.user,pwd=self.password) 
        
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
                vms.update({managed_object_ref: managed_object_ref.name})
        return vms
             

    def printvminfo(self, vm, depth=1):
        """
        Print information for a particular virtual machine or recurse into a folder
        with depth protection
        """
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


def get_stcleaner_opt():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'd:s:u:p:h', ['datastore=', 'server=', 'user=','password=', 'help'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    lst = {'datastore':None,'server':None,'user':None,'password':None}

    if len(opts) == 0:
        usage()
        sys.exit(2)  

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('-d', '--datastore'):
            lst['datastore'] = arg
        elif opt in ('-s', '--server'):
            lst['server'] = arg
        elif opt in ('-u', '--user'):
            lst['user'] = arg
        elif opt in ('-p', '--password'):
            lst['password'] = arg
        else:
            usage()
            sys.exit(2)

    if lst['datastore'] == None or lst['server'] == None or lst['user'] == None or lst['password'] == None:
        print >> sys.stderr, "One of the value in datastore, server, user or password is not set"
        sys.exit(2)

    return lst
        
def usage():
    print('-h:--help -- to get infomation')
    print('-d:--datastore -- to provide datastore')
    print('-s:--server -- to provide server IP or FQDN')
    print('-u:--user -- to provide user')
    print('-p:--password -- to provide password')

# Start program
if __name__ == "__main__":
    
    lst = get_stcleaner_opt()
    datastorage = lst['datastore']
    server = lst['server'] 
    user = lst['user']
    password = lst['password']
    #print("""datastore:%s,server:%s,user:%s,password:%s"""%(lst['datastore'],lst['server'],lst['user'],lst['password']))
    
    inventory_mgr = InventoryManager(server,user,password)
    inventory_mgr.connect_server()
    vms = inventory_mgr.get_all_vms()
    for vm in vms:
        print (vms[vm])
    