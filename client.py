import socket
import threading
import sys
from sys import argv, stdout, exit

import random                                                      
import os


class Client:
    
    accessMenu = {
        "menu" : "_"
    }   #type menu


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def sendMsg(self):
        while True:
            try:
                self.sock.send(bytes(input(""), 'utf-8'))
            except (KeyboardInterrupt, SystemExit):
                stdout.flush()
                print ('\nConnection to server closed.')   #Close server
                break
    
    def recvMsg(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                print(str(data, 'utf-8'))
            except (KeyboardInterrupt, SystemExit):
                stdout.flush()
                print ('\nConnection to server closed.')   #Close server
                break

    def __init__(self, address):
        self.sock.connect((address,10000))
        
        print("You are connected ...")
        
        #Thread to send messages
        iThread = threading.Thread(target=self.sendMsg)
        iThread.daemon = True
        iThread.start()
        #Thread to receive messages
        iThread = threading.Thread(target=self.recvMsg)
        iThread.daemon = True
        iThread.start()
        
        while True:
            try:   
                pass
            except (KeyboardInterrupt, SystemExit):
                stdout.flush()
                print ('\nConnection to server closed.')   #Close server
                break


       


if __name__ == "__main__":
    
    if(len(sys.argv) > 1):
        #if there is more than 1 argument, you want to be the client
        client = Client(sys.argv[1])
    else:
        ipNumber = input("Write out the IP you want to connect into: ")
        ip = str(ipNumber)
        client = Client(ip)
