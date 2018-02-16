"""
Python Project
TODO: add team membres here

Libs used:
https://docs.python.org/2/library/re.html
https://docs.python.org/3/library/ipaddress.html
"""

import re
import ipaddress
import sys


from GetRouterID import GetRouterID
from PingObject import PingObject

"""
Method allowing to read ip addresses from a file
"""
def readRange(filenameRange):
    up_hosts = set()
    try:
        with open(filenameRange) as file:
            content = file.readlines()

            # Save ranges into a list
            ranges = [x.strip() for x in content]

            # Iterate over each range
            for ip_add in ranges:
                # Use ipaddress module to check the validity of ip range
                ip_network = ipaddress.ip_network(unicode(ip_add, "UTF-8"), strict = False)
                # Add all discovered devices into a set
                up_hosts.update(getUpHosts(ip_network))

            return up_hosts

    except ValueError:
        print 'Invalid IP address format'
        sys.exit(0)
    except IOError:
        print 'The file' + filenameRange + ' couldn\'t be found'
        sys.exit(0)

"""
Method allowing to compute broadcast_address and to ping hosts that are up
"""
def getUpHosts(ip_network):
    # Get broadcast_address from ip network
    broadcast_address = ip_network.broadcast_address

    # Ping all devices from the broadcast address using subprocess
    pingObject = PingObject(broadcast_address)
    return pingObject.pingHosts()

"""
Method allowing to read passwords from a file
"""
def readPasswords(filenamePwd):
    try:
        with open(filename_pwd) as file:
            content = file.readlines()

        # Return all the passwords as a list
        return [x.strip() for x in content]
    except IOError:
        print 'The file' + filenamePwd + ' couldn\'t be found'
        sys.exit(0)

# 1. Read range first
filename_range = 'range.txt'
up_hosts = readRange(filename_range)
if up_hosts is None:
    print 'Couldn\'t ping devices'
    sys.exit(0)
else:
    #TODO remove (just for display)
    for host in up_hosts:
        print host

# 2. Read passwords file
filename_pwd = 'password.txt'
passwords = readPasswords(filename_pwd)
if passwords is None:
    print 'Empty passwords list'
    sys.exit(0)
else:
    #TODO remove (just for display)
    for password in passwords:
        print password

# 3. Connect and collect info
GetRouterID = GetRouterID (up_hosts, passwords)
dev = GetRouterID.connect()
print dev


"""
#Test for visualize the network
#Add the following Libs
#import networkx as nx
#import matplotlib.pyplot as plt
print '-------\n\n'
G = nx.Graph()
dico = {}
up_hosts.add("192.168.1.2")
up_hosts.add("192.168.1.4")
for host in up_hosts:
dico[host] = list()
dico[host].append(str(host) + " neighbor 1")
dico[host].append(str(host) + " neighbor 2")
G.add_node(host)
for values in dico[host]:
G.add_edge(host, values)

nx.draw(G, with_labels=True, font_weight='bold')
plt.show()
plt.savefig("topology.png")
"""
