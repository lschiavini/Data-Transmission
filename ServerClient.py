import socket
import threading
import sys

class Server:
    PORT = 10000
    ADDRESS = '0.0.0.0' 
        #   make server available to any IP address that is 
        #   configured on the server 
    connections = []

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #   init conection: AF_INET -> IPv4
        #                   SOCK_STREAM -> TCP connection
    def __init__(self):
        self.sock.bind((self.ADDRESS, self.PORT))
        self.sock.listen(1)

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
                c.close()
                break
            
            for connection in self.connections:
                try:
                    connection.send(bytes(data))
                except(ConnectionResetError):
                    #   Checks if connection was closed by peer
                    pass

    def run(self):
        while True:
            c, a = self.sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c,a))
            cThread.daemon = True 
                #   lets close the program even if other 
                #   threads are still running
            cThread.start()
            self.connections.append(c)
            print(str(a[0]) + ": " + str(a[1]) + " connected")

class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def sendMsg(self):
        while True:
            try:
                self.sock.send(bytes(input(""), 'utf-8'))
            except (KeyboardInterrupt, SystemExit):
                break;    
    def __init__(self, address):
        self.sock.connect((address,10000))

        iThread = threading.Thread(target=self.sendMsg)
        iThread.daemon = True
        iThread.start()
        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            print(str(data, 'utf-8'))

if(len(sys.argv) > 1):
    #if there is more than 1 argument, you want to be the client
    client = Client(sys.argv[1])
else:
    server = Server()
    server.run()