import socket
import threading
import sys
import os.path


class Server:
    PORT = 10000
    ADDRESS = '0.0.0.0' 
        #   make server available to any IP address that is 
        #   configured on the server 
    connections = []
    charStartFileTrans = "!"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #   init conection: AF_INET -> IPv4
        #                   SOCK_STREAM -> TCP connection
    def __init__(self):
        self.sock.bind((self.ADDRESS, self.PORT))
        self.sock.listen(1)
        print("Server Connected...")


    def createServerDir(self):
        dir = ""
        dir = os.path.join(dir, 'ServerFiles')
        if not os.path.exists(dir):
            os.makedirs(dir)
        return dir

    def sendFiles2Client(self,c,a):
        fileName='TD_work.pdf' #In the same folder or path is this file running must the file you want to tranfser to be
        path = self.createServerDir()
        filePath = path + "/" + fileName
        
        startFileTrans = bytes(self.charStartFileTrans,'utf-8')
        c.send(startFileTrans)
        print("Sending Files")

        with open(fileName, 'rb') as f:
            c.sendfile(f, 0)
        f.close()
        endString = "@endfile"
        endFile = endString.encode('utf-8').strip()
        c.send(endFile)
        print('Done sending')

    def receiveFileFClient(self,c,a):

        fileName='TD_work.pdf' #In the same folder or path is this file running must the file you want to tranfser to be
        path = self.createServerDir()
        filePath = path + "/" + fileName
        
        with open(filePath, 'wb') as f:
            print ('File opened')                
            while True:
                print('receiving data...')
                data = c.recv(self.CHUNK_SIZE)
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
            if data[0] == ord(self.charStartFileTrans):
                self.sendFiles2Client(c,a)
            
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
    charStartFileTrans = "!"

    CHUNK_SIZE = 1024*8
    SIZEMESSAGE = 1024*4
    
    def sendMsg(self):
        while True:
            try:
                self.sock.send(bytes(input(""), 'utf-8'))
            
            except (KeyboardInterrupt, SystemExit):
                break;    


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
        while True:
            fileName = input("Write the name of the file: ")
            if testFileExists(fileName):
                break
            else:
                yesNo = input("File doesn't exist, try again? (Y/n)")
                condNo = (yesNo == "N") or (yesNo == "n") 
                condYes = (yesNo == "Y") or (yesNo == "y")
                if condYes:
                    continue
                elif condNo:
                    return False
        #SEND ROUTINE        
        fileName = "TD_work.pdf"
        path = self.createLocalDir()
        filePath = path + "/" + fileName
        
        startFileTrans = bytes(self.charStartFileTrans,'utf-8')
        c.send(startFileTrans)
        print("Sending Files")

        with open(fileName, 'rb') as f:
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
        self.actualDir = ""
        self.sock.connect((address,10000))

        iThread = threading.Thread(target=self.sendMsg)
        iThread.daemon = True
        iThread.start()

        iThread = threading.Thread(target=self.recvMsg)
        iThread.daemon = True
        iThread.start()


        print("Connected...")
        while True:
            try:   
                pass
            except (KeyboardInterrupt, SystemExit):
                stdout.flush()
                print ('\nConnection to server closed.')   #Close server
                break


if(len(sys.argv) > 1):
    #if there is more than 1 argument, you want to be the client
    client = Client(sys.argv[1])
else:
    server = Server()
    server.run()