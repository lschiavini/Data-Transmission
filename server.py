import socket
import threading
import sys
from sys import argv, stdout, exit
import random                                                      
import os
from threading import Event


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
    roomVector = []
        #   format: object room
    userVector = [] 
        #   format: object user
        #   data(either command or message)

    userMenuCommand = {64:"@"}

    def printWelcome(self, c, a):
        self.clearScreen(c,a)
        self.sendToUser(c, " Welcome to the ChatRoom App...\nPress @ to see the Menu\n\n\n")
    
    def createUsr(self, c, a, newUser):

        while True:
            self.sendToUser(c," Please write your new Username: ")
            (close, data) = self.receiveStrMessage(c, a)
            
            (condTestPass, userObj) = self.testUsrPass(data, None)

            if (condTestPass):
                #if User doesnt exists returns True
                newUser.setName(data)#sets Name
                while True:
                    self.sendToUser(c," Please choose a new Password: ")
                    (close, data) = self.receiveStrMessage(c, a)
                    prevPass = data
                    self.sendToUser(c," Please REPEAT your Password: ")
                    (close, data) = self.receiveStrMessage(c, a)
                    nextPass = data
                    
                    (condTestPass, userObj) = self.testUsrPass(data, None)
           
                    #if not (condTestPass):
                    #    self.sendToUser(c," Somebody created the User before you did...\n")
                    #    break
                    #el
                    if(prevPass == nextPass):
                        newUser.setPass(data)#PassWord
                        self.userVector.append(newUser)
                        self.clearScreen(c,a)
                        self.sendToUser(c," New User Added...Going to Login\n\n\n\n\n")
                        userObj = self.confirmLogin(c,a, newUser)

                        return close
                    else:
                        pass
            else:
                #User already being used, go to Login
                self.sendToUser(c," User already exists... Do you want to go to Login? (Y/n)\n")
                (close, data) = self.receiveStrMessage(c, a)
                yesNo = data
                condNo = (yesNo == "N") or (yesNo == "n") 
                condYes = (yesNo == "Y") or (yesNo == "y")
                if (condYes):
                    #go to Login
                    userObj = self.confirmLogin(c,a, newUser)
                    return close
                elif(condNo):
                    #ask for another userName input
                    pass

    def confirmLogin(self,c,a, iUser):
        #User exists? if yes testUsrPass, else createUsr
        #   Assigns connection to User
        yesNo = ""


        while True:
            self.sendToUser(c," LOGIN\n Please write your Username: ")
            (close, userName) = self.receiveStrMessage(c, a)
            self.sendToUser(c," Please write your Password: ")
            (close, passW) = self.receiveStrMessage(c, a)

            (condTestPass, userObj) = self.testUsrPass(userName, passW)
            print(str(condTestPass) + " User found: " + userObj.getName() + "Pass: " + userObj.getPass())
            if(condTestPass):
                for u in self.userVector:
                    if (u.getName() == userObj.getName()):
                        u.setConnection(c)
                        self.sendToUser(c," Logged In, You Welcome ")  
                        Event().wait(1.5)           
                        return (True, u)
            else:
                self.sendToUser(c," LOGIN\n Wrong Password. Do you Want to Try again?(Y/n) ")
                (close, data) = self.receiveStrMessage(c, a)
                yesNo = data
                condNo = (yesNo == "N") or (yesNo == "n") 
                condYes = (yesNo == "Y") or (yesNo == "y")
                if (condYes):
                    #go to Login
                    pass
                elif(condNo):
                    #ask for another userName input
                    self.createUsr(c,a, iUser)

    def printAllUsr(self):
        print("User List ------- Pass List\n")
        for u in self.userVector:
            print(u.getName()+ "\t: " +u.getPass()+ "\n")

    def testUsrPass(self, userName, passW = None):
        #Tests User/password
        #If it passes the test returns True, else False
        newUser = User()
        if (len(self.userVector) > 0):
            print("There are Users")
            if (passW == None):
                #Tests if user isn't already being used
                for usr in self.userVector:
                    print("User: " + userName + "\tVectUser: " + usr.getName())
                    if (usr.getName() == userName):
                        return (False,newUser)
                return (True,usr)
            else:
                for usr in self.userVector:
                    if (usr.getName() == userName):
                        if(usr.getPass() == passW):
                            return (True, usr)        
                return (False,newUser)    #User doesnt match
        else:
            print(" There are no Users")
            return (True, newUser)

    def devMenu(self, c, a, iUser):

        self.clearScreen(c,a)
        self.printMenu(c,a)
        #Create a Room
        close = self.createRoom(c, a, iUser)
        self.confirmEnter(c, a, iUser)

        #Add user to Room
        pass

    def handler(self, c, a):
        global connections
        close = False
        data = ""

        self.printWelcome(c, a)

        
        #Create a user
        self.printAllUsr()
        iUser = User()
        close = self.createUsr(c, a, iUser)

        while True:
            #close = self.userFlow(c , a)            
            self.devMenu(c , a, iUser)
            #(close, data) = self.usrListener(c, a)
            if (close):
                break
            else:
                pass

    def testRoomPass(self, roomName, rPassW):
        pass

    def writeUsr2File(self, user, passW, roomName, rPassW):
        pass
    
    def createRoom(self, c, a, user):
        newRoom = Room()

        while True:
            self.sendToUser(c," Please write the name of the Room: ")
            (close, data) = self.receiveStrMessage(c, a)
            
            (condTestPass, roomObj) = self.testRoomPass(data, None)

            if (condTestPass):
                #if Room doesnt exists returns True
                newRoom.setName(data)#sets Name
                newRoom.setPass("None")#sets Name
                newRoom.isVip(False)#sets Name
                
                self.sendToUser(c,"Do you want a password? (Y/n)")
                (close, yesNo) = self.receiveStrMessage(c, a)
                condNo = (yesNo == "N") or (yesNo == "n") 
                condYes = (yesNo == "Y") or (yesNo == "y")

                if(condYes):
                    while True:
                        self.sendToUser(c," Please choose a new Password: ")
                        (close, data) = self.receiveStrMessage(c, a)
                        prevPass = data
                        self.sendToUser(c," Please REPEAT your Password: ")
                        (close, data) = self.receiveStrMessage(c, a)
                        nextPass = data
                        
                        (condTestPass, roomObj) = self.testRoomPass(data, None)
            
                        if not (condTestPass):
                            self.sendToUser(c," Somebody created the Room before you did...\n")
                            break
                        elif(prevPass == nextPass):
                            newRoom.setPass(data)#PassWord
                            newRoom.isVip(True)
                            self.roomVector.append(newRoom)
                            self.clearScreen(c,a)
                            self.sendToUser(c," New Room Added... Going back to Menu\n\n\n\n\n")
                            Event().wait(1.5)
                            return close
                        else:
                            pass
                elif(condNo):
                    newRoom.setPass("None")#PassWord
                    newRoom.isVip(False)
                    self.roomVector.append(newRoom)
                    self.clearScreen(c,a)
                    self.sendToUser(c," New Room Added... Going back to Menu\n\n\n\n\n")
                    Event().wait(1.5)
                    return close


            else:
                #Room already created, go to Login
                self.sendToUser(c," Room already created... Do you want to Enter? (Y/n)\n")
                (close, data) = self.receiveStrMessage(c, a)
                yesNo = data
                condNo = (yesNo == "N") or (yesNo == "n") 
                condYes = (yesNo == "Y") or (yesNo == "y")
                if (condYes):
                    #go to Login
                    self.confirmEnter(c,a, user)
                    print("Entered Room that was already created")
                    return close
                elif(condNo):
                    #ask for another roomName input
                    pass

    def testRoomPass(self, roomName, passW):
        noneRoom = Room()
        #Tests room/password
        #If it passes the test returns True, else False
        if (len(self.roomVector) > 0):
            print("There are rooms")
            if (passW == None):
                #Tests if room isn't already being used
                for rum in self.roomVector:
                    print("room: " + roomName + "\tVectroom: " + rum.getName()+ "\tPASSoom: " + rum.getPass())
                    if (rum.getName() == roomName):
                        return (False,noneRoom)
                return (True,rum)
            else:
                for rum in self.roomVector:
                    print("\tPass Provided: " + passW + "\tRoom Pass: " + rum.getPass()+"\n")
                    if (rum.getName() == roomName):
                        if(rum.getPass() == passW):
                            return (True, rum)
                print("Pass doesnt match")
                return (False, noneRoom) #Pass doesnt match
                
        else:
            print(" There are no rooms")
            return (True, noneRoom)

    def findRoom(self, roomName):
        findRoom = Room()
        for rum in self.roomVector:
            if (rum.getName() == roomName):
                return (True, rum)
        return(False, findRoom)
                
            

        

    def confirmEnter(self, c, a, user):
        #Room exists? if yes testRoomPass, else createRoom
        #   Assigns connection to User
        yesNo = ""
        condNo = (yesNo == "N") or (yesNo == "n") 
        condYes = (yesNo == "Y") or (yesNo == "y")

        self.showAllRooms(c,a)

        while True:
            self.sendToUser(c," Entering Room \n Please write the Room name: ")

            (close, data) = self.receiveStrMessage(c, a)
            roomName = data

            (condExists, roomObj) = self.findRoom( roomName)
            condHasPass = False
            
            if(condExists):
                condHasPass = roomObj.getIsVip()
            else:
                pass
            
            
            print(str(condHasPass) + "  "+roomObj.getName())
            
            self.findRoom(roomName)
            if condHasPass: 
                #The Room does have a password
                self.sendToUser(c," Please write the Room Password: ")
                (close, passW) = self.receiveStrMessage(c, a)

                (condTestPass, roomObj) = self.testRoomPass(roomName, passW)
                print(str(condTestPass) + " room found: " + roomObj.getName() + "Pass: " + roomObj.getPass())
                if(condTestPass):
                    for rum in self.roomVector:
                        if (rum.getName() == roomObj.getName()):
                            user.setRoom(rum)
                            rum.addUser(c, user)
                            self.sendToUser(c," Entered the Room, Have a nice chat :P ")  
                            Event().wait(1.5)
                            self.clearScreen(c,a)        
                            return True
                else:
                    self.sendToUser(c," LOGIN\n Wrong Password. Do you Want to Try again?(Y/n) ")
                    (close, data) = self.receiveStrMessage(c, a)
                    yesNo = data
                    if (condYes):
                        #try again
                        pass
                    elif(condNo):
                        #ask for another userName input
                        break
            else:
                #The room is non Vip
                for rum in self.roomVector:
                    print(str(" room found: " + rum.getName() + "Pass: " + rum.getPass()))
                    if (rum.getName() == roomObj.getName()):
                        user.setRoom(rum)
                        rum.addUser(c, user)
                        self.sendToUser(c," Entered the Room, Have a nice chat :P ")  
                        Event().wait(1.5)
                        self.clearScreen(c,a)        
                        return True
                #didnt find room
                print("No non vip room found")
                return False




    def deleteRoom(self, roomName, rPassW):
        for n in range(len(rooms)):
            condName = rooms[n].getName() == roomName
            condPassW = rooms[n].getPass() == rPassW
            
            if condName:
                if condPassW:
                    rooms.remove(rooms[n])
                    break
                else:
                    #ask password to client
                    pass

    def showAllRooms(self,c,a):
        message = " Rooms Available: \n"
        self.sendToUser(c, message)
        for n in range(len(self.roomVector)):
            print("\tVectroom: " + self.roomVector[n].getName()+ "\tPASSoom: " + self.roomVector[n].getPass())
            message = self.roomVector[n].getName()
            if(self.roomVector[n].getIsVip()):
                message = message + " LOCKED"  
            self.sendToUser(c," "+message + "\n\n")
            

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
                

    

    def printMenu(self,c,a):
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
            self.sendToUser(c, printMenu)

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
            self.createRoom(c,a)
        elif command == "2":
            self.deleteRoom(roomName, rPassW)
        elif command == "3":
            self.showAllRooms()
        elif command == "4":
            self.enterRoom(roomName, rPassW)
        elif command == "5":
            self.sendToAll(msg, room)
        elif command == "6":
            self.printMenu(c,a)
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


