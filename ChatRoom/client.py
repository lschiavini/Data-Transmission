import socket
import threading
import sys
from sys import argv, stdout, exit

import random                                                      
import os

from room import *

class Client:
    
    charStartFileTrans = "!"

    CHUNK_SIZE = 1024*8
    SIZEMESSAGE = 1024*4

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
                data = self.sock.recv(self.SIZEMESSAGE)

                if not data:
                    break
                elif data[0] == ord(self.charStartFileTrans):
                    self.receiveFileFServer()
                else:
                    message = data.decode('utf-8')#, 'utf-8')
                    print(message)
            except (KeyboardInterrupt, SystemExit):
                stdout.flush()
                print ('\nConnection to server closed.')   #Close server
                break



    def testFileExists(self, fileName):
        if os.path.isfile(fileName):
            return True
        else:
            print("File doesn't exist...\n")
            return False       

    def senfFile2Server(self):
        fileName = ""
        #while True:
        #    fileName = input("Write the name of the file: ")
        #    if testFileExists(fileName):
        #        break
        #    else:
        #        yesNo = input("File doesn't exist, try again? (Y/n)")
        #        condNo = (yesNo == "N") or (yesNo == "n") 
        #        condYes = (yesNo == "Y") or (yesNo == "y")
        #        if condYes:
        #            continue
        #        elif condNo:
        #            return False
        #SEND ROUTINE        
        fileName = "TD_work.pdf"
        path = self.createLocalDir()
        filePath = path + "/" + fileName
        
        startFileTrans = bytes(self.charStartFileTrans,'utf-8')
        c.send(startFileTrans)
        print("Sending Files")

        with open(filePath, 'rb') as f:
            c.sendfile(f, 0)
        f.close()
        endString = "@endfile"
        endFile = endString.encode('utf-8').strip()
        c.send(endFile)
        print('Done sending')

    def createLocalDir(self):
        dir = ""
        dir = os.path.join(dir, 'LocalFiles')
        if not os.path.exists(dir):
            os.makedirs(dir)
        return dir

    def receiveFileFServer(self):
        
        fileName = "TD_work.pdf"
        path = self.createLocalDir()
        filePath = path + "/" + fileName


        with open(filePath, 'wb') as f:
            print ('File opened')                
            while True:
                print('receiving data...')
                data = self.sock.recv(self.CHUNK_SIZE)
                msg = repr(data)

                if msg.find("@endfile") != -1:
                    data = data[:-8]
                    f.write(data)
                    #print("Out we go")
                    break
                if (not data):
                    #print("Out we go")
                    break
                
                f.write(data)

        print("Got File")
        f.close()
            

    




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
