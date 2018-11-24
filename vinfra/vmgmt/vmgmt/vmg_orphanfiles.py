#!/usr/bin/env python

# ==================================================
# @author: Runxin runxinw@vmware.com
#

import sys, getopt
import vmg_inventory
import vmg_dstore

def _getopt():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'd:s:u:p:h', ['datastore=', 'server=', 'user=','password=', 'help'])
    except getopt.GetoptError:
        _usage()
        sys.exit(2)

    lst = {'datastore':None,'server':None,'user':None,'password':None}

    if len(opts) == 0:
        _usage()
        sys.exit(2)  

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            _usage()
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
            _usage()
            sys.exit(2)

    if lst['datastore'] == None or lst['server'] == None or lst['user'] == None or lst['password'] == None:
        print >> sys.stderr, "One of the value in datastore, server, user or password is not set"
        sys.exit(2)

    return lst
        
def _usage():
    print('-h:--help -- to get infomation')
    print('-d:--datastore -- to provide datastore')
    print('-s:--server -- to provide server IP or FQDN')
    print('-u:--user -- to provide user')
    print('-p:--password -- to provide password')

# Start program
def main(server, user, password, store):
    # The return results
    results = []  
    # the inventory    
    inventory_mgr = vmg_inventory.InventoryManager(server,user,password)
    inventory_mgr.connect_server()
    vm_objects = inventory_mgr.get_all_vms()
    vm_names = vm_objects.values()
   
    files = vmg_dstore.get_files(store)
 
    for filename in files:
        orphan = True
        for vmname in vm_names:
            if filename.find(vmname) != -1:
                print "skip VM file " + filename
                orphan = False
                break
        if orphan == True:
            results.append(filename)

    return results

             
if __name__ == "__main__":

    lst = _getopt()
    store = lst['datastore']
    server = lst['server']
    user = lst['user']
    password = lst['password']
    results = main(server,user,password,store)
    for r in results:
        print r
