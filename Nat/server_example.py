
from pydhcplib.dhcp_packet import *
from pydhcplib.dhcp_network import *
import socket
import cPickle as pickle

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# AWS Public IP
host = '34.194.147.243'
port = 9999
# connection to hostname on the port.
s.connect((host, port))                               

clientPort = 50000
netoptS = {'client_listen_port': 50001,
          'server_listen_port': clientPort,
          'listen_address':"0.0.0.0"
         }

class ToServer(DhcpServer):
    def __init__(self, options):
        DhcpServer.__init__(self,
                            options["listen_address"],
                            options["client_listen_port"],
                            options["server_listen_port"]
                           )
        
    def HandleDhcpDiscover(self, packet):
	s.send(pickle.dumps((packet, clientPort)))
    def HandleDhcpRequest(self, packet):
	s.send(pickle.dumps((packet, clientPort)))
    def HandleDhcpDecline(self, packet):
	print packet.str()        
    def HandleDhcpRelease(self, packet):
	print packet.str()        
    def HandleDhcpInform(self, packet):
	print packet.str()
    def HandleDhcpAll(self, packet):
        print packet.str()

server = ToServer(netoptS)

while True:
    server.GetNextDhcpPacket()
    packet, port = pickle.loads(s.recv(4096))
    server.SendDhcpPacketTo(packet, '255.255.255.255', 50001)
    print(packet.str())                            

s.close()

'''
netoptC = {'client_listen_port':68,
           'server_listen_port':9999,
           'listen_address':"0.0.0.0"}

class ToClient(DhcpClient):
    def __init__(self, options):
        DhcpClient.__init__(self,options["listen_address"],
                            options["client_listen_port"],
                            options["server_listen_port"])
        
    def HandleDhcpOffer(self, packet):
        print packet.str()
    def HandleDhcpAck(self, packet):
        print packet.str()
    def HandleDhcpNack(self, packet):
        print packet.str()        

client = Client(netopt)
# Use BindToAddress if you want to emit/listen to an internet address (like 192.168.1.1)
# or BindToDevice if you want to emit/listen to a network device (like eth0)
client.BindToAddress()

while True :
    client.GetNextDhcpPacket()
print client.str()
'''
