import socket
import threading
import sys
from sys import argv, stdout, exit
import random                                                      
import os

from room import *
from usefulFunc import *

from user import *

class Server:
    SIZEMESSAGE = 4096
    PORT = 10000
    ADDRESS = '0.0.0.0' 
        #   make server available to any IP address that is 
        #   configured on the server 
    connections = []
    rooms = []
        #   format: object room
    userVector = [] 
        #   format: object user
        #   data(either command or message)

    userMenuCommand = {64:"@"}

    def printWelcome(self, c, a):
        self.clearScreen(c,a)
        self.sendToUser(c, " Welcome to the ChatRoom App...\nPress @ to see the Menu\n\n\n")
    
    def createUsr(self, c, a):
            
        yesNo = ""
        condNo = (yesNo == "N") or (yesNo == "n") 
        condYes = (yesNo == "Y") or (yesNo == "y")

        newUser = User()

        while True:
            self.sendToUser(c," Please write your new Username: ")
            (close, data) = self.receiveStrMessage(c, a)
            
            print(data)
            if (self.testUsrPass(data, None)):
                #if User doesnt exists returns True
                newUser.setName(data)#sets Name
                while True:
                    self.sendToUser(c," Please choose a new Password: ")
                    (close, data) = self.receiveStrMessage(c, a)
                    prevPass = data
                    self.sendToUser(c," Please write AGAIN your Password: ")
                    (close, data) = self.receiveStrMessage(c, a)
                    nextPass = data
                    
                    print("DEBUG LAZYYYY")
                    print(newUser.getName())
                    if not (self.testUsrPass(newUser.getName(), None)):
                        self.sendToUser(c," Somebody created the User before you did...\n")
                        break
                    elif(prevPass == nextPass):
                        newUser.setPass(data)#PassWord
                        self.userVector.append(newUser)
                        self.sendToUser(c," New User Added\n\n\n\n\n")
                        return close
                    else:
                        pass
            else:
                #User already being used, go to Login
                self.sendToUser(c," User already exists... Do you want to go to Login? (Y/n)\n")
                (close, data) = self.receiveStrMessage(c, a)
                yesNo = data
                if (condYes):
                    #go to Login
                    self.confirmLogin(c)
                    return close
                elif(condNo):
                    #ask for another userName input
                    pass



    def confirmLogin(self):
        #User exists? if yes testUsrPass, else createUsr
        pass
    

    def printAllUsr(self):
        print("User List ------- Pass List\n")
        for u in self.userVector:
            print(u.getName()+ "\t: " +u.getPass()+ "\n")

    def testUsrPass(self, userName, passW = None):
        #Tests User/password
        #If it passes the test returns True, else False
        if (len(self.userVector) > 0):
            print("There are Users")
            if (passW == None):
                #Tests if user isn't already being used
                for usr in self.userVector:
                    print("User: " + userName + "\tVectUser: " + usr.getName())
                    if (usr.getName() == userName):
                        return False
                    else:
                        return True
            else:
                for usr in self.userVector:
                    if (usr.getName() == userName):
                        if(usr.getPassW() == passW):
                            return True
                        else:
                            return False #Pass doesnt match
                    else:
                        return False    #User doesnt match
        else:
            print(" There are no Users")
            return True

    def devMenu(self, c, a):
        #Create a user
        self.printAllUsr()
        close = self.createUsr(c, a)
        #Create a Room
        #close = self.createRoom(c, a)
        #Add user to Room
        pass

    def handler(self, c, a):
        global connections
        close = False
        data = ""
        
        self.printWelcome(c, a)
        while True:
            #close = self.userFlow(c , a)            
            self.devMenu(c , a)
            #(close, data) = self.usrListener(c, a)
            if (close):
                break
            else:
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
        message = " Rooms Available: \n"
        self.sendToAll(message)
        for n in range(len(rooms)):
            message = rooms[n].getName()
            if(rooms[n].getIsVip()):
                message = message + " LOCKED"  
            self.sendToAll(message)
            

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
                        self.sendToUser(c, " Please choose a Number from 1 to 7: ")
                        (close, data) = self.recvMsg(c, a)
                        comData = int(data[0]) 
                        condDataNum = (comData >= ord("1")) and (comData <= ord("7"))
                        if condDataNum:
                            break
                        else:
                            self.sendToUser(c, " Type a number between 1  and 7 ...\n")
                    return (close, data)
                else:#user just wants to talk
                    #data = "lalalallalalalalaladasdsadsa_RoomName"
                    print("COND TALK")
                    comData = str(data)
                    incommingMsg = comData.split('_')
                    msg = incommingMsg[0]
                    #roomName = incommingMsg[1]
                    self.sendToAll(msg)#, roomName)
                    return (close, "10")
            except:
                break
                

    

    def printMenu(self):
            printMenu = """//////WELCOME TO CHATROOM APP
                                        MENU \n  
                                1 : CREATE ROOM \n
                                2 : DELETE ROOM \n
                                3 : SHOW ALL ROOMS \n
                                4 : ENTER ROOM \n
                                5 : TALK \n
                                6 : MENU \n
                                7 : EXIT :( 
                                
                                >> Press any number you want\n"""
            self.sendToAll(printMenu)

    def clearScreen(self, c, a):
        clearScreen = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        self.sendToUser(c, clearScreen)
        
    def helpMessage(self, c, a):
        message = "Press @ any time for the menu to appear"
        self.sendToUser(c, clearScreen)

    def userFlow(self, c, a):#inside handler
        close = False
        command = "10"

        (close, command) = self.usrListener(c, a)
        
        if not(command == "6") and not (command == "10"):
            self.clearScreen(c,a)
        if command == "8":
            self.createUsr()
        elif command == "9":
            self.confirmLogin(),      #LOGIN
        elif command == "1":
            self.createRoom(roomName, rPassW)
        elif command == "2":
            self.deleteRoom(roomName, rPassW)
        elif command == "3":
            self.showAllRooms()
        elif command == "4":
            self.enterRoom(roomName, rPassW)
        elif command == "5":
            self.sendToAll(msg, room)
        elif command == "6":
            self.printMenu()
        elif command == "7":
            self.disconnect(c, a)
        elif command == "10":
            print("SEU PEBA")
        else:
            pass
    
        return close


    

    

    def sendRoomMsg(self, msg, room):
        global connections
        for connection in room.getUsers().getConnection():
            try:
                connection.send(bytes(msg, 'utf-8'))
            except(ConnectionResetError):
                #   Checks if connection was closed by peer
                pass
        
    def sendToUser(self, c,msg):
        connection = c
        try:
            connection.send(bytes(msg, 'utf-8'))
        except(ConnectionResetError):
            #   Checks if connection was closed by peer
            pass

    def sendToAll(self, msg):
        global connections
        for connection in self.connections:
                try:
                    connection.send(bytes(msg, 'utf-8'))
                except(ConnectionResetError):
                    #   Checks if connection was closed by peer
                    pass
    
    def receiveStrMessage(self, c, a):
        close = False
        data = []
        try:
            (close, data) = self.recvMsg(c, a)
            data = str(data, "utf-8")
            return (close, data)
        except:
            return (close, data)

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


