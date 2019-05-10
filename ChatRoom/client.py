import socket
import threading
import sys
from sys import argv, stdout, exit

import random                                                      
import os

from room import *
from file import *

class Client:
    

    sendMessageFlag = True
    sendFileFlag = False
    currentMsg = ""

    charStartFileTrans = "!"
    filesVector = []
        #   Object type File
    CHUNK_SIZE = 1024*8
    SIZEMESSAGE = 1024*4

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def sendFileS(self):
        
        fileName = self.currentMsg

        if self.testFileExists(fileName):
            newFile = File(fileName)
            path = newFile.getLocalDir()
            filePath = path + newFile.getName()
            print("Local: Sending Files")

            sendName = fileName.strip() + "\n"
                
            self.sock.send(bytes(sendName, 'utf-8'))
                #2 - Sends FileName
            with open(filePath, 'rb') as f:
                self.sock.sendfile(f, 0)
            f.close()
                #3 - Sends File
            endString = "$endFile"
            endFile = endString.encode('utf-8').strip()
            self.sock.send(endFile)
                #4 - Sends EndFile
            print("Done sending")
        else: 
            print("DEBUG: $cancel")
            #cancelString = "$cancel"
            #cancelFile = cancelString.encode('utf-8').strip()
            #self.sock.send(cancelFile)
            self.currentMsg = "$cancel"
            self.sock.send(bytes("$cancel", 'utf-8'))
            
        
        self.sendFileFlag = False
        self.sendMessageFlag = True

    def receiveFile(self):
        data = self.sock.recv(self.SIZEMESSAGE)
        fileName = data.decote('utf-8')

        if (fileName != "$cancel"):
            newFile = File(fileName)
            
            filePath = newFile.getServerDir() +  newFile.getName()    
            
            with open(filePath, 'wb') as f:
                print ('File opened')                
                while True:
                    print('receiving data...')
                    data = self.sock.recv(self.CHUNK_SIZE)
                    msg = repr(data)

                    if msg.find("$endFile") != -1:
                        data = data[:-8]
                        f.write(data)
                        break
                    if (not data):
                        break
                    f.write(data)
            print("Got File")
            f.close()
            self.filesVector.append(newFile)
            return newFile
        else:
            return None

    def sendMsg(self):
        
        while True:
            try:
                if self.sendMessageFlag:
                    print("DEBUG:SENDING MSG")
                    self.currentMsg = input("")
                    self.sock.send(bytes(self.currentMsg, 'utf-8'))
                elif self.sendFileFlag:
                    print("DEBUG:SENDING FILE")
                    self.sendFileS()

            except (KeyboardInterrupt, SystemExit):
                stdout.flush()
                print ('\nConnection to server closed.')   #Close server
                break
    
    def recvMsg(self):
        while True:
            try:
                data = self.sock.recv(self.SIZEMESSAGE)
                condData = data.decode('utf-8')

                if not data:
                    break
                elif data[0] == ord(self.charStartFileTrans):
                    self.receiveFileFServer()
                elif (condData == "$nameFile"):
                    print("Sending Files...")
                    self.sendMessageFlag = False
                    self.sendFileFlag = True
                else:
                    message = data.decode('utf-8')#, 'utf-8')
                    print(message)
            except (KeyboardInterrupt, SystemExit):
                stdout.flush()
                print ('\nConnection to server closed.')   #Close server
                break

    def testFileExists(self, fileName):
        if os.path.isfile("LocalFiles/"+fileName):
            return True
        else:
            print("File doesn't exist...\n")
            return False   

    def sendFile2Server(self):
        fileName = ""
       
        fileName = "TD_work.pdf"
        path = self.createLocalDir()
        filePath = path + "/" + fileName
        
        startFileTrans = bytes(self.charStartFileTrans,'utf-8')
        c.send(startFileTrans)
        print("Sending Files")

        with open(filePath, 'rb') as f:
            c.sendfile(f, 0)
        f.close()
        endString = "$endFile"
        endFile = endString.encode('utf-8').strip()
        c.send(endFile)
        print('Done sending')

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

                if msg.find("$endFile") != -1:
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

    def createLocalDir(self):
        dir = ""
        dir = os.path.join(dir, 'LocalFiles')
        if not os.path.exists(dir):
            os.makedirs(dir)
        return dir


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
