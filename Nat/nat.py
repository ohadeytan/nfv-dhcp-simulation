from pydhcplib.dhcp_packet import *
from pydhcplib.dhcp_network import *
import socket
import select
from time import sleep

'''
Transfer packets from client to server and vise versa.
Add/Remove the HomeId (=port) to the packet.
''' 

# create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# AWS Public IP <---------- change to your server ip
host = '34.194.147.243'
port = 9999
# connection to hostname on the port.
server.connect((host, port))                               

socket_array = [server]
# destination port of a server start from 50000 (instead of 67)
# destination port of a client start from 60000 (instead of 68)
for i in range(1,301): # For 300 homes
    c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    c.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
    c.setblocking(0)
    c.bind(('0.0.0.0', 50000+i))
    socket_array.append(c)

while True:
    readable, writable, exceptional = select.select(socket_array, [], [], 30)
    for s in readable:
        if s is server:
            # DHCP packet size is 244, HomeId size is 5
            data_raw = s.recv(249, socket.MSG_WAITALL)
            if len(data_raw) < 249:
                #sleep(1)
                continue
            packet, port = data_raw[:244], data_raw[-5:]
            c.sendto(packet, ('255.255.255.255', int(port)+10000))
        elif s in socket_array:
            packet = s.recv(244)
            extPacket = packet + str(s.getsockname()[1])
            server.sendall(extPacket)
        else:
            print("other socket")                           

server.close()
c.close()
