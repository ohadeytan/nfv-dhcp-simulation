# server.py 
import socket                                         
import time
import cPickle as pickle
from pydhcplib.type_ipv4 import ipv4
from pydhcplib.dhcp_packet import *
from pydhcplib.dhcp_network import *
import collections

# create a socket object
serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = '0.0.0.0'                        

port_host = 9999                                           

# bind to the port
serversocket.bind((host, port_host))                                  

# queue up to 5 requests
serversocket.listen(5)                                           

clientsocket,addr = serversocket.accept()      

d = collections.defaultdict(dict)
def chooseIp(port, mac):
    if not d.get(port):
        d[port]['subnet'] = len(d)
    if not d[port].get(mac):
        d[port][mac] = len(d[port])
    return '{}.{}.{}.{}'.format(128+d[port]['subnet'] // 256, d[port]['subnet'] % 256, d[port][mac] // 256, d[port][mac] % 256)  

while True:
    packet, port = pickle.loads(clientsocket.recv(4096))
    if packet.IsDhcpDiscoverPacket():
	packet.TransformToDhcpOfferPacket()
	packet.SetOption('yiaddr', ipv4(chooseIp(port, str(packet.GetOption("chaddr")))).list())
	packet.SetOption('siaddr', ipv4(addr[0]).list())
	clientsocket.send(pickle.dumps((packet, port)))

    if packet.IsDhcpRequestPacket():
	packet.TransformToDhcpAckPacket()
	clientsocket.send(pickle.dumps((packet, port)))

    print(packet.str())
    print(port)

clientsocket.close()
