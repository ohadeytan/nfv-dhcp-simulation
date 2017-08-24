from datetime import datetime
from random import Random
from optparse import OptionParser
from pydhcplib.dhcp_packet import DhcpPacket
from pydhcplib.dhcp_network import DhcpClientOld as DhcpClient
from pydhcplib.type_hw_addr import hwmac
from pydhcplib.type_ipv4 import ipv4
import socket
import sys
import time

r = Random()
r.seed()

# the 3 following functions was taken from:
# https://github.com/dyninc/DHCPTest-python/blob/master/dhcp_test.py
# generamte a random mac address
def genmac():
        i = []
        for z in xrange(6):
                i.append(r.randint(0,255))
        return ':'.join(map(lambda x: "%02x"%x,i))

#generate a random xid
def genxid():
        decxid = r.randint(0,0xffffffff)
        xid = []
        for i in xrange(4):
                xid.insert(0, decxid & 0xff)
                decxid = decxid >> 8
        return xid

#set up a dhcp packet, this defaults to the discover type
def preparePacket(xid=None,giaddr='0.0.0.0',chaddr='00:00:00:00:00:00',ciaddr='0.0.0.0', yiaddr='0.0.0.0', msgtype='discover'):
        req = DhcpPacket()
        req.SetOption('op',[1])
        req.SetOption('htype',[1])
        req.SetOption('hlen',[6])
        req.SetOption('hops',[0])
        req.SetOption('xid',xid)
        req.SetOption('giaddr',ipv4(giaddr).list())
        req.SetOption('chaddr',hwmac(chaddr).list() + [0] * 10)
        req.SetOption('ciaddr',ipv4(ciaddr).list())
        if msgtype == 'request':
                mt = 3
        elif msgtype == 'release':
                mt = 7
        else:
                mt = 1
        if mt == 3:
                req.SetOption('yiaddr', ipv4(yiaddr).list())
                req.SetOption('request_ip_address', ipv4(yiaddr).list())
        req.SetOption('dhcp_message_type',[mt])
        return req

recvPort = 60000 + int(sys.argv[1])
sendPort = 50000 + int(sys.argv[1])
netoptC = {'client_listen_port': recvPort,
           'server_listen_port': sendPort,
           'listen_address':"0.0.0.0"}

class Client(DhcpClient):
    def __init__(self, options):
        DhcpClient.__init__(self,options["listen_address"],
                            options["client_listen_port"],
                            options["server_listen_port"])
         
    def HandleDhcpOffer(self, packet):
	TransformToDhcpRequestPacket(packet)
	self.SendDhcpPacketTo(packet, '255.255.255.255', sendPort)
    def HandleDhcpAck(self, packet):
	pass
    def HandleDhcpNack(self, packet):
	pass
    def HandleDhcpAll(self, packet):
        if packet.GetOption("xid") != xid:
             #print("Ignored")
             packet.SetOption("dhcp_message_type",[0])
        else:
             pass
             #print packet.str()

def TransformToDhcpRequestPacket(packet):
	packet.SetOption("dhcp_message_type",[3])
	packet.SetOption("op",[1])

client = Client(netoptC)
client.BindToAddress()
mac = genmac()
xid = genxid()

def main():
	start = datetime.now()

	packet = preparePacket(xid, '0.0.0.0', mac, '0.0.0.0', '0.0.0.0', 'discover')

	client.SendDhcpPacketTo(packet, '255.255.255.255', sendPort)

	while not packet.IsDhcpAckPacket():
		packet = client.GetNextDhcpPacket()

	end = datetime.now()
        print('Got ip: {:20}    Latency: {:15}'.format(str(packet.GetOption("yiaddr")) ,end - start))

main()

