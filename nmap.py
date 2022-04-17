import socket
import json
import nmap3
nmap = nmap3.Nmap()


ip_list = ['172.16.7.202', '172.16.7.211', '172.16.3.15']
"""
for x in ip_list:
    result = socket.gethostbyaddr(x)
    print(result[0], '=', x)
"""
for x in ip_list:
    result = json.dumps(nmap.nmap_os_detection(x), indent=4)
    print(result)
