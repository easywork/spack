#!/usr/bin/env python

# ==================================================
# @author: Runxin runxinw@vmware.com
#

import requests
from requests.auth import HTTPBasicAuth
from xml.etree import ElementTree


class NsxManager(object):

    def __init__(self, ip, fqdn, user, password, vc):
        self.ip = ip
        self.fqdn = fqdn
        self.user = user
        self.password = password
        self.vc = vc
        
    def getapi(self, url):
        basic_auth = HTTPBasicAuth(self.user, self.password)
        response = requests.get(url, auth=basic_auth, verify=False)
    
        if(response.ok):
            print "return code " + str(response.status_code)
            rootElement = ElementTree.fromstring(response.content)     
            return rootElement
        else:
            response.raise_for_status()

    def postapi(self, url, xml):
        basic_auth = HTTPBasicAuth(self.user, self.password)
        response = requests.post(url, auth=basic_auth, verify=False)
    
        if(response.ok):
            print "return code " + str(response.status_code)
            rootElement = ElementTree.fromstring(response.content)     
            return rootElement
        else:
            response.raise_for_status()     
     
        
    def putapi(self, url, xml):
        basic_auth = HTTPBasicAuth(self.user, self.password)
        response = requests.put(url, auth=basic_auth, verify=False)
    
        if(response.ok):
            print "return code " + str(response.status_code)
            rootElement = ElementTree.fromstring(response.content)     
            return rootElement
        else:
            response.raise_for_status()     


def get_instance(filename):
    fl = open(filename, 'r')
    M = {}
    for line in fl.readlines():
        X = line.strip().split(':')
        M.update({X[0]:X[1]})
    fl.close()
    mgr = NsxManager(M.get('ip'), M.get('fqdn'), M.get('user'), M.get('password'), M.get('vc'))
    return  mgr


if __name__ == '__main__':
    import sys
    
    nsx = get_instance(sys.argv[1])
    print nsx.ip
    print nsx.fqdn
    print nsx.user
    print nsx.password 