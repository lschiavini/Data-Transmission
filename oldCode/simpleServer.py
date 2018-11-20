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
        self.sock.bind((ADDRESS, PORT))
        self.sock.listen(1)

    def handler(self, c, a):
        global connections
        while True:
            data = c.recv(1024)
            #   c is connection
            #   recv  = receiving data from the connection
            #   arg is number of bytes
            for connection in self.connections:
                connection.send(bytes(data))
            if not data:
                connections.remove(c)
                c.close()
                break
    def run(self):
        while True:
            c, a = self.sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c,a))
            cThread.daemon = True 
                #   lets close the program even if other 
                #   threads are still running
            cThread.start()
            self.connections.append(c)
            print(self.connections)


server = Server()
server.run()