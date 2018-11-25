# ==================================================
# @author: Runxin runxinw@vmware.com
#


import requests
# from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth
# import json
from xml.etree import ElementTree


def exe_getapi(url):
    # response = requests.post(url)
    # headers = {'Content-Type':'application/xml'}
    # response = requests.get(url,auth=HTTPDigestAuth(raw_input("username: "), raw_input("Password: ")), verify=True)
    user = 'admin'
    password = 'VMware123'
    basic_auth = HTTPBasicAuth(user, password)
    response = requests.get(url, auth=basic_auth, verify=False)
    
    if(response.ok):
        print "return code " + str(response.status_code)
        #print response.content
        root = ElementTree.fromstring(response.content)     
        for dvsID in root.findall("./vdsContext/switch/objectId"):
	    print "dvsID " + str(dvsID.text)	
        # jdata = json.loads(response.content)
        # for key in jdata:
        #    print key + " : " + jdata[key]
        #tree = ElementTree.fromstring(response.content)
        #events = ElementTree.iterparse(response.raw)
        #for event, elem in events:
        #    print event
    else:
        response.raise_for_status()


def test_getapi(filename):
    fh = open(filename, 'r')
    lines = []
    for line in fh.readlines():
        lines.append(line.strip())
    fh.close()
    exe_getapi(lines[0])


if __name__ == '__main__':
    import sys
    
    test_getapi(sys.argv[1])
