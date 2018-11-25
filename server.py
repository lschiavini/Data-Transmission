import socket
import threading
import sys
from sys import argv, stdout, exit
import random                                                      
import os

from room import *

class Server:
    SIZEMESSAGE = 4096
    PORT = 10000
    ADDRESS = '0.0.0.0' 
        #   make server available to any IP address that is 
        #   configured on the server 
    connections = []
    rooms = []
    userVector = [] 
        #   format: user,pass,roomName,rPassW, data(either command or message)

    userMenuCommand = {64:"@"}

    
    
    def createUsr(self):
        while True:
            pass

    def confirmLogin(self):
        #User exists? if yes testUsrPass, else createUsr
        pass
    

    def testUsrPass(self, user, passW):
        pass
    
    def testRoomPass(self, roomName, rPassW):
        pass

    def writeUsr2File(self, user, passW, roomName, rPassW):
        pass
    
    def createRoom(self, roomName, rPassW):
        rooms.append(Room(roomName, rPassW))
    
    def checkDuplicateRoom(self,  roomName, rPassW):
        pass

    
    def enterRoom(self, roomName, rPassW):
        pass

    def deleteRoom(self, roomName, rPassW):
        for n in range(len(rooms)):
            condName = rooms[n].getName() == roomName
            condPassW = rooms[n].getPassW() == rPassW
            
            if condName:
                if condPassW:
                    rooms.remove(rooms[n])
                    break
                else:
                    #ask password to client
                    pass

    def showAllRooms(self):
        message = "Rooms Available: \n"
        self.sendMessage(message)
        for n in range(len(rooms)):
            message = rooms[n].getName()
            if(rooms[n].getIsVip()):
                message = message + " LOCKED"  
            self.sendMessage(message)
            

    def usrListener(self, c, a):
        #gets user command, check if it is some of the menu comands or if he is just talking
        while True:
            try:
                (close, data) = self.recvMsg(c, a)
                comData = data[0]
        
                condMenu = (comData == ord(self.userMenuCommand.get(64)))
                #print(self.userMenuCommand.get(64))
                
                #print(type(comData))
                #print(self.userMenuCommand.get(comData))
                #print(condMenu)

                
                if (condMenu):
                    print("COND MENU")
                    while True:
                        self.sendMessage("Please choose a Number from 0 to 10: ")
                        (close, data) = self.recvMsg(c, a)
                        comData = int(data[0]) 
                        condDataNum = (comData >= ord("0")) and (comData <= ord("8"))
                        if condDataNum:
                            break
                        else:
                            self.sendMessage("Type a number between 0  and 8 ...\n")
                    return (close, data)
                else:#user just wants to talk
                    #data = "lalalallalalalalaladasdsadsa_RoomName"
                    print("COND TALK")
                    comData = str(data)
                    incommingMsg = comData.split('_')
                    msg = incommingMsg[0]
                    #roomName = incommingMsg[1]
                    self.sendMessage(msg)#, roomName)
                    return (close, "10")
            except:
                break
                

    

    def printMenu(self):
            printMenu = """//////WELCOME TO CHATROOM APP
                                        MENU \n  
                                0 : CREATE USER \n
                                1 : LOGIN \n
                                2 : CREATE ROOM \n
                                3 : DELETE ROOM \n
                                4 : SHOW ALL ROOMS \n
                                5 : ENTER ROOM \n
                                6 : TALK \n
                                7 : MENU \n
                                8 : EXIT :( 
                                
                                >> Press any number you want\n"""
            self.sendMessage(printMenu)

    def clearScreen(self):
        clearScreen = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        self.sendMessage(clearScreen)
        
    def helpMessage(self):
        message = "Press @ any time for the menu to appear"


    def userFlow(self, c, a):#inside handler
        close = False
        command = "10"

        (close, command) = self.usrListener(c, a)
        
        if not(command == "6") and not (command == "10"):
            self.clearScreen()
        if command == "0":
            self.createUsr()
        elif command == "1":
            self.confirmLogin(),      #LOGIN
        elif command == "2":
            self.createRoom(roomName, rPassW)
        elif command == "3":
            self.deleteRoom(roomName, rPassW)
        elif command == "4":
            self.showAllRooms()
        elif command == "5":
            self.enterRoom(roomName, rPassW)
        elif command == "6":
            self.sendMessage(msg, room)
        elif command == "7":
            self.printMenu()
        elif command == "8":
            self.disconnect(c, a)
        elif command == "10":
            print("SEU PEBA")
        else:
            pass
    
        return close




    def handler(self, c, a):
        global connections
        close = False
        data = ""
        while True:
            close = self.userFlow(c , a)
            print("SEU PEBA")
            
            
            #(close, data) = self.usrListener(c, a)
            if (close):
                break
            else:
                pass

    def sendMessage(self, msg):#, room):
        global connections
        for connection in self.connections:
                try:
                    connection.send(bytes(msg, 'utf-8'))
                except(ConnectionResetError):
                    #   Checks if connection was closed by peer
                    pass
    
    def recvMsg(self, c, a):
            close = False
            data = c.recv(self.SIZEMESSAGE)

            #   c is connection
            #   recv  = receiving data from the connection
            #   arg is number of bytes
            if not data:
                self.disconnect(c, a)
                close = True
            else:
                data = str(data, "utf-8")
                data = bytes(data, 'utf-8')
            return (close, data)

    
    def disconnect(self, c, a):
        print(str(a[0]) + ": " + str(a[1]) + " disconnected")
        self.connections.remove(c)
        c.close()




    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #   init conection: AF_INET -> IPv4
        #                   SOCK_STREAM -> TCP connection
    def __init__(self):
    
        self.sock.bind((self.ADDRESS, self.PORT))
        self.sock.listen(1)
        print("Server running ....")

    
            

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
            
            self.printMenu()



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


