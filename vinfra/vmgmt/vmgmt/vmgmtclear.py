#!/usr/bin/env python
import sys, getopt
import vmgmtbase


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
if __name__ == "__main__":
    
    lst = _getopt()
    datastorage = lst['datastore']
    server = lst['server'] 
    user = lst['user']
    password = lst['password']
    #print("""datastore:%s,server:%s,user:%s,password:%s"""%(lst['datastore'],lst['server'],lst['user'],lst['password']))
    
    inventory_mgr = vmgmtbase.InventoryManager(server,user,password)
    inventory_mgr.connect_server()
    vms = inventory_mgr.get_all_vms()
    for vm in vms:
        print (vms[vm])
    