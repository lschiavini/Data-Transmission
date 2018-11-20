import socket
import threading
import sys
import time
from random import randint

class Server:
    PORT = 10000
    ADDRESS = '0.0.0.0' 
        #   make server available to any IP address that is 
        #   configured on the server 
    connections = []
    peers = []

    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #   init conection: AF_INET -> IPv4
        #                   SOCK_STREAM -> TCP connection
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #   Makes possible to connect to the same ADDRESS that was in use
        sock.bind((self.ADDRESS, self.PORT))
        sock.listen(1)
        print("Server running ....")

        while True:
            c, a = sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c,a))
            cThread.daemon = True 
                #   lets close the program even if other 
                #   threads are still running
            cThread.start()
            self.connections.append(c)
            self.peers.append(a[0])
            
            print(str(a[0]) + ": " + str(a[1]) + " connected")
            self.sendPeers()      


    def handler(self, c, a):
        global connections
        while True:
            data = c.recv(1024)
            #   c is connection
            #   recv  = receiving data from the connection
            #   arg is number of bytes
            if not data:
                print(str(a[0]) + ": " + str(a[1]) + " disconnected")
                self.connections.remove(c)
                self.peers.remove(a[0])   
                try:
                    self.sendPeers()
                except:
                    pass
                c.close()
                break
            
            for connection in self.connections:
                try:
                    connection.send(bytes(data))
                except(ConnectionResetError):
                    #   Checks if connection was closed by peer
                    pass
    def sendPeers():
        p = ""
        for peer in self.peers:
            p = p + peer + ","
        for connection in self.connections:
            connection.send(b'\x11' + bytes(p, "utf-8"))

class Client:
    def sendMsg(self, sock):
        while True:
            try:
                sock.send(bytes(input(""), 'utf-8'))
            except (KeyboardInterrupt, SystemExit):
                break;  

    def __init__(self, address):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((address,10000))
        print("You are connected ...")

        iThread = threading.Thread(target=self.sendMsg, args = (sock,))
        iThread.daemon = True
        iThread.start()
        while True:
            data = sock.recv(1024)
            if not data:
                break
            if data[0:1] == b'\x11': 
                #print("got peers")
                self.updatePeers(data[1:])
            print(str(data, 'utf-8'))

    def updatePeers(self, peerData):
        p2p.peers = str(peerData, "utf-8").split(",")[:-1]

class p2p:
    peers = ['127.0.0.1']

while True:
    try:
        print("Trying to connect ...")
        time.sleep(randint(1,5))
        for peer in p2p.peers:
            try:
                client = Client(peer)
            except (KeyboardInterrupt):
                sys.exit(0);
            except:
                pass
            try:
                server = Server()
            except KeyboardInterrupt:
                sys.exit(0);
            except:
                print("Couldn't start the server ...")
                pass
            
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)