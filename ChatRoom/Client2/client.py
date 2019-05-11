import socket
import threading
import sys
from sys import argv, stdout, exit

import random                                                      
import os

from room import *
from file import *

class Client:
    
    addressCurr = ""
    sendMessageFlag = True
    sendFileFlag = False
    currentMsg = ""

    charStartFileTrans = "!"
    filesVector = []
        #   Object type File
    CHUNK_SIZE = 1024*8
    SIZEMESSAGE = 1024*4

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def setAddress(self,address):
        self.addressCurr = address

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
            self.currentMsg = "$cancel"
                #/\ I don't remember why this line(52) was needed, but it is
            self.sock.send(bytes("$cancel", 'utf-8'))
        
        self.sendFileFlag = False
        self.sendMessageFlag = True

    def receiveFile(self):
        data = self.sock.recv(self.SIZEMESSAGE)
        try:
            fileName = data.decode('utf-8')
        except Exception:
            fileName = "None.none"
        newFile = File(fileName)
        
        filePath = newFile.getLocalDir() +  newFile.getName()    
        with open(filePath, 'wb') as f:
            print ('File opened')                
            while True:
                print('receiving data...')
                data = self.sock.recv(self.CHUNK_SIZE)
                msg = repr(data)

                if msg.find("$endFile") != -1:
                    data = data[:-8]
                    f.write(data)
                    print("Got File")
                    break
                if msg.find("$cancel") != -1:
                    print("Cancel")
                    os.remove(filePath)
                    newFile.setName("None.none")
                    break
                if (not data):
                    break
                f.write(data)
        f.close()
        self.filesVector.append(newFile)
        return newFile
        
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
                try:
                    condData = data.decode('utf-8')
                except Exception:
                    condData = None

                if not data:
                    break
                elif data[0] == ord(self.charStartFileTrans):
                    self.receiveFile()
                elif (condData[:5] == "/send"):
                    print("Sending Files...")
                    message = data.decode('utf-8')#, 'utf-8')
                    print(message[6:])
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

    def createLocal(self):
        if os.path.isdir("LocalFiles"):
            pass
        else:
            os.mkdir("LocalFiles")
    
    def __init__(self, address):
        self.sock.connect((address,10000))
        self.setAddress(address)
        self.createLocal()

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
