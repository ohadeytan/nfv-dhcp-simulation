# server.py 
from pydhcplib.type_ipv4 import ipv4
from pydhcplib.dhcp_packet import *
from pydhcplib.dhcp_network import *
from pydhcplib.dhcp_constants import *
import collections
from time import sleep
import SocketServer

'''
This script should run on the cloud server.
'''

def log(packet, port):
    print("Type: {:15}      Home: {:3}     Ip: {:15}".format(DhcpFieldsName['dhcp_message_type'][str(packet.GetOption("dhcp_message_type")[0])], int(port)-50000, packet.GetOption("yiaddr")))

'''
Ip is given according to class B spec.
Port number used as the subnet id.
d[port]['subnet'] contains the allocated subnet.
d[port][mac] is the device host.
'''
def chooseIp(port, mac):
    if not d.get(port):
        d[port]['subnet'] = len(d)
    if not d[port].get(mac):
        d[port][mac] = len(d[port])
    return '{}.{}.{}.{}'.format(128+d[port]['subnet'] // 256, d[port]['subnet'] % 256, d[port][mac] // 256, d[port][mac] % 256)  

'''
Handle all the packets 
'''
class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        ackCounter = 0
        # self.request is the TCP socket connected to the client
	while True:
            # DHCP packet size is 244, HomeId size is 5
            data_raw = self.request.recv(249, socket.MSG_WAITALL)
            if len(data_raw) < 249:
                #sleep(1)
                continue
            data, port = data_raw[:244], data_raw[-5:]
            packet = DhcpPacket()
            packet.DecodePacket(data) 
            log(packet, port)
            if packet.IsDhcpDiscoverPacket():
	        packet.TransformToDhcpOfferPacket()
	        packet.SetOption('yiaddr', ipv4(chooseIp(port, str(packet.GetOption("chaddr")))).list())
	        packet.SetOption('siaddr', ipv4(self.client_address[0]).list())
                extPacket = packet.EncodePacket() + port
	        self.request.send(extPacket)

            if packet.IsDhcpRequestPacket():
	        packet.TransformToDhcpAckPacket()
                extPacket = packet.EncodePacket() + port
                self.request.send(extPacket)
                ackCounter += 1

            log(packet, port)
            if ackCounter % 100 == 0: 
                print("-------> Ack Counter = " + str(ackCounter))

d = collections.defaultdict(dict)

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
