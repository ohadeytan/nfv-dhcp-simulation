# server.py 
import socket                                         
import time

# create a socket object
serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = '0.0.0.0'                        

port = 9999                                           

# bind to the port
serversocket.bind((host, port))                                  

# queue up to 5 requests
serversocket.listen(5)                                           

clientsocket,addr = serversocket.accept()      

while True:
    # establish a connection

    print(clientsocket.recv(1024))

clientsocket.close()
