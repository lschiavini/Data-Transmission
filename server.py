import socket
import threading
import sys
from sys import argv, stdout, exit
import random                                                      
import os




class Server:
    PORT = 10000
    ADDRESS = '0.0.0.0' 
        #   make server available to any IP address that is 
        #   configured on the server 
    connections = []
    rooms = []
    userDict = {}#  to test User PassW
    roomDict = {}#  to test Room RPassW

    userMenuCommand = "_"
    

    def confirmLogin(self):
        #User exists? if yes testUsrPass, else createUsr
        pass
    
    def createUsr(self):
        while True:
            pass

    def testUsrPass(self, user, passW):
        pass
    
    def testRoomPass(self, roomName, rPassW):
        pass

    def writeUsr2File(self, user, passW, roomName, rPassW):
        pass
    
    def createRoom(self, roomName, rPassW):
        pass
    
    def checkDuplicateRoom(self,  roomName, rPassW):
        pass

    
    def deleteRoom(self, roomName, rPassW):
        pass

    def enterRoom(self, roomName, rPassW):
        pass

    def showAllRooms(self):
        pass

    def menu(self, c, a):#inside handler


        command = usrListener(c, a)

        commands_dict = {
            0 : self.createUsr(),     #CREATEUSER
            1 : self.confirmLogin(),      #LOGIN
            2 : self.createRoom(roomName, rPassW),        #CREATEROOM
            3 : self.deleteRoom(roomName, rPassW),        #DELETEROOM
            5 : self.showAllRooms(),        #SEEROOMS
            6 : self.enterRoom(roomName, rPassW),        #ENTERROOM
            7 : self.sendMessage(msg, room),       #TALK
            8 : self.menu(),        #MENU
            9:  self.disconnect(c, a)       #EXITPROGRAM
            10: continue
        }.get(command)


    def usrListener(self, c, a):
        #gets user command, check if it is some of the menu comands or if he is just talking
        
        while True:
            (_, data) = self.recvMsg(c, a)
            condMenu = (data[0] == userMenuCommand)
            condDataNum = (data >= 0) and (data < 10)

            if (condMenu):
                while True:
                    (_, data) = self.recvMsg(c, a)
                    if condDataNum:
                        break
                return data
            else:#user just wants to talk
                #data = "lalalallalalalalaladasdsadsa_RoomName"
                incommingMsg = data.split('_')
                msg = incommingMsg[0]
                roomName = incommingMsg[1]
                self.sendMessage(msg, roomName)
                return 10
                
                


            


    def sendMessage(self, msg):#, room):
        global connections
        for connection in self.connections:
                try:
                    connection.send(bytes(msg))
                except(ConnectionResetError):
                    #   Checks if connection was closed by peer
                    pass
    
    def recvMsg(self, c, a):
            close = False
            data = c.recv(1024)
            #   c is connection
            #   recv  = receiving data from the connection
            #   arg is number of bytes
            if not data:
                self.disconnect(c, a)
                close = True
            return (close, data)

    def disconnect(self, c, a):
        print(str(a[0]) + ": " + str(a[1]) + " disconnected")
        self.connections.remove(c)
        c.close()

    #def populateLoginsDict():
        #    global user_logins = {}
        #
        #    with open('user_pass.txt') as aFile:
        #        for line in aFile:
        #            (key, val) = line.split()
        #            user_logins[key] = val
        #
        #    return user_logins
        #
    #def showConnections(self):



    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #   init conection: AF_INET -> IPv4
        #                   SOCK_STREAM -> TCP connection
    def __init__(self):
    
        self.sock.bind((self.ADDRESS, self.PORT))
        self.sock.listen(1)
        print("Server running ....")

    def handler(self, c, a):
        global connections
        close = False
        data = ""
        while True:
            (close, data) = self.recvMsg(c, a)
            if (close):
                break
            else:
                self.sendMessage(data)
            

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



if __name__ == "__main__":
    print("Trying to connect ...")
    try:
        server = Server()
        server.run()
    except KeyboardInterrupt:
        stdout.flush()
        open("user_pass.txt", 'w').close()
        sys.exit(0);
    except:
        print("Couldn't start the server ...")
        pass


