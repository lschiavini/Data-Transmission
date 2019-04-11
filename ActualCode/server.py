import socket
import threading
import sys
from sys import argv, stdout, exit
import random                                                      
import os
from threading import Event


from room import *
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

    userMenuCommand = {64:"@",
                        37:"%"}
    
    charStartFileTrans = "!"

####GUI FUNCT

    def printWelcome(self, c, a):
        self.clearScreen(c,a)
        self.sendToUser(c, " Welcome to the ChatRoom App...\n\n\n")
    
    def clearScreen(self, c, a):
        clearScreen = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        self.sendToUser(c, clearScreen)
        
    def helpMessage(self, c, a):
        message = "Press @ any time for the menu to appear"
        self.sendToUser(c, message)

    def printMenu(self,c,a):
            printMenu = """//////WELCOME TO CHATROOM APP
                        MENU \n  
                1 : CREATE ROOM \n
                2 : DELETE ROOM \n
                3 : SHOW ALL ROOMS \n
                4 : ENTER ROOM \n
                5 : MENU \n
                6 : EXIT :( 
                
        >> Press any number you want to enter Menu Options\n"""
            self.sendToUser(c, printMenu)

    def roomGUI(self,c,a, room):
        RoomGUI = """//////WELCOME TO """+room.getName() +""" ROOM
            @ : MENU \n  
            >> Press @ to go back to Menu
            >> Press % to see Users in this Room
            >> Press ! to send Files\n"""
        self.sendToUser(c, RoomGUI)

####STATE MACHINE

    def handler(self, c, a):
        iUser = User()
        self.initState(c,a, iUser)
        
        close = False
        isMenuFirst = True
        try:
            print(" New User added: " + iUser.getName() + "\n")
        except(Exception):
            pass
        self.menu(c, a, iUser, isMenuFirst)
        self.disconnect( c, a,iUser)


    def initState(self, c, a, iUser):
        global connections
        close = False
        data = ""
        self.printWelcome(c,a)        
        #Create a user
        self.printAllUsr()
        close = self.createUsr(c,a, iUser)
        #Prints menu
        self.clearScreen(c,a)
        self.printMenu(c,a)
        

    def menu(self, c, a, iUser, isMenuFirst):
        #while not Exit
         #looking at the menu
        userExit = False
        while not userExit:
            notNumber = False
            chatRoomEnable = False
            command = bytes("10",'utf-8')
            while not notNumber:
                notNumber =  (command >= bytes("1",'utf-8')) and (command <= bytes("6",'utf-8'))
                try:
                    self.clearScreen(c,a)
                    self.printMenu(c,a)
                    self.sendToUser( c,"\tWrite a number from 1 to 6")
                    (close, command) = self.userListener(c, a, iUser, isMenuFirst)
                    
                    command = str(command, "utf-8")
                    print("COMMAND: " + command + "\n")
                except:
                    pass   
            if command == "1":
                print("CREATE\n")
                (close, chatRoomEnable) = self.createRoom( c, a, iUser)
            elif command == "2":
                print("DELETE\n")
                self.deleteRoom( c, a)
            elif command == "3":
                print("SHOW ALL ROOMS\n")
                self.showRoomsMenu( c, a)
            elif command == "4":
                print("ENTER\n")
                chatRoomEnable = self.confirmEnter( c, a, iUser) #TODOIST: needs to enter chatRoom
            elif command == "5":
                print("MENU\n")
                self.printMenu( c, a)
            elif command == "6":
                print("EXIT\n")
                userExit = True
            elif command == "10":
                print("SEU PEBA")
            else:
                pass
                
            if chatRoomEnable:
                #chatRoom
                self.chatRoom(c, a, iUser, isMenuFirst)
                chatRoomEnable = False
            else:
                pass

            isMenuFirst = False

    def chatRoom(self,c,a, iUser, isMenuFirst):
        close = False
        data = []
        isMenuFirst = False
        goMenu = False
        seeUsers = False

        for rum in self.roomVector:
            if rum.hasUser(iUser):
                self.roomGUI(c,a,rum)
        while not goMenu:
            (close, bytedata) = self.userListener(c, a, iUser, isMenuFirst)
            
            if bytedata is not None:
                goMenu = self.callMenu(c,a,bytedata)
                seeUsers = self.callSeeUsers(c,a,bytedata)
                sendFiles = self.callSendFiles(c,a,bytedata)

                if seeUsers:
                    rum = self.findRoomFromUser(iUser)
                    self.whoAmItalkingTo(c, rum)
                if goMenu:
                    self.exitRoom( c, a, iUser)
                    break
                if sendFiles:
                    rum = self.findRoomFromUser(iUser)
                    self.sendFilesToRoom(rum, iUser)
                    

                data = str(bytedata, "utf-8")

                condiUserInRoom = self.updateRooms(iUser, data) 

                if (condiUserInRoom):
                    self.sendToUser(c, " \n")
                else:
                    #needs to enter a Room to Talk
                    self.sendToUser(c, " You need to be connected to a Room to talk.")
                    break

        return (close, data, isMenuFirst, goMenu) #isMenu
    
    def userListener(self, c, a, iUser, isMenuFirst):
            data = None
            if (isMenuFirst is None):
                isMenuFirst = False
            
            if (isMenuFirst):
                (close, data) = self.recvMsg(c, a)
                data = str(data,'utf-8')
                return (close, data)
            else:    
                try:
                    stringUser =">> "
                    self.sendToUser(c, stringUser)
                    (close, bytedata) = self.recvMsg(c, a)
                    return (close, bytedata)
                except:
                    pass

    def callMenu(self, c, a, data):
        try:
            comData = data[0]
            condMenu = (comData == ord(self.userMenuCommand.get(64)))       
            if (condMenu):
                print("COND MENU")
                return True
        except (Exception):
            pass    
        return False

    def callSeeUsers(self, c, a, data):
        try:
            comData = data[0]
            condSeeWho = (comData == ord(self.userMenuCommand.get(37)))       
            if (condSeeWho):
                print("COND SEE USERS")
                return True
        except (Exception):
            pass    
        return False
    
    def callSendFiles(self,c,a,data):
        try:
            comData = data[0]
            condSendFiles = (comData == ord(self.charStartFileTrans))      
            if (condSendFiles):
                print("COND SEND FILES")
                return True
        except (Exception):
            pass    
        return False

####USER FUNCT

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
                        (success,userObj) = self.confirmLogin(c,a, newUser)
                        if success:
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
                    (success,userObj) = self.confirmLogin(c,a, newUser)
                    if success:
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
            if(condTestPass):
                for u in self.userVector:
                    if (u.getName() == userObj.getName()):
                        try:
                            print("LAZYDEBUG")
                            print(str(u.hasConnection()))
                            if u.hasConnection():
                                print("GOT HERE - IF")    
                                self.sendToUser(c," User Already signed in...")
                                #self.createUsr(c, a, iUser) 
                                return (False, None)
                            else:
                                print("GOT HERE - ELSE")
                                u.setConnection(c)
                                self.sendToUser(c," Logged In, You Welcome ")  
                                Event().wait(1.5)           
                                return (True, u)
                        except (Exception):
                            pass  
                        
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
                    #print("User: " + userName + "\tVectUser: " + usr.getName())
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

####ROOM FUNCT

    def createRoom(self, c, a, user):
        newRoom = Room()
        isInRoom = False
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
                            isInRoom = self.confirmEnter(c,a, user)
                            return (close, isInRoom)
                        else:
                            pass
                elif(condNo):
                    newRoom.setPass("None")#PassWord
                    newRoom.isVip(False)
                    self.roomVector.append(newRoom)
                    self.clearScreen(c,a)
                    self.sendToUser(c," New Room Added... Entering\n\n\n\n\n")
                    isInRoom = self.confirmEnter(c,a, user)
                    return (close, isInRoom)


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
                    if (rum.getName() == roomName):
                        return (False,noneRoom)
                return (True,rum)
            else:
                for rum in self.roomVector:
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
       
    def findRoomFromUser(self, iUser):
        for rum in self.roomVector:
            users = rum.getUsers()
            if (users is not None):
                for u in users:
                    if str(u.getName()) == str(iUser.getName()):
                        return rum
        return False

    def confirmEnter(self, c, a, user):
        #Room exists? if yes testRoomPass, else createRoom
        #   Assigns connection to User
        yesNo = ""
        condNo = (yesNo == "N") or (yesNo == "n") 
        condYes = (yesNo == "Y") or (yesNo == "y")

        self.showAllRooms(c,a)
        isInRoom = False

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
            
            print(str(condHasPass) + "  " + roomObj.getName())
            
            if condHasPass: 
                #The Room does have a password
                self.sendToUser(c," Please write the Room Password: ")
                (close, passW) = self.receiveStrMessage(c, a)

                (condTestPass, roomObj) = self.testRoomPass(roomName, passW)
               
                if(condTestPass):
                    for n in range(len(self.roomVector)):
                        if (self.roomVector[n].getName() == roomObj.getName()):
                            self.roomVector[n].addUser( user)

                            print("LIST OF ROOMS" + "\n")
                            for rum in self.roomVector:
                                self.showUsrInRoom(rum)

                            self.sendToUser(c," Entered the Room, Have a nice chat :P ")  
                            self.sendToRoom("::: "+ user.getName() + " Entered the Room", self.roomVector[n], user)  
                            
                            Event().wait(1.5)
                            self.clearScreen(c,a)        
                            isInRoom = True
                            return isInRoom
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
                for n in range(len(self.roomVector)):
                    #print(str(" room found: " + rum.getName() + "Pass: " + rum.getPass()))
                    if (self.roomVector[n].getName() == roomObj.getName()):
                        #user.setRoom(rum)

                        self.roomVector[n].addUser( user)
                                                
                        print("LIST OF ROOMS" + "\n")
                        for rum in self.roomVector:
                            self.showUsrInRoom(rum)
                        
                        self.sendToUser(c," Entered the Room, Have a nice chat :P ")  
                        self.sendToRoom("::: "+ user.getName() + " Entered the Room", self.roomVector[n], user)  
                        
                        Event().wait(1.5)
                        self.clearScreen(c,a)         
                        isInRoom = True
                        
                        return isInRoom
                        break
                #didnt find room
                isInRoom = False
                return isInRoom
                break
        return isInRoom

    def exitRoom(self, c, a, iUser):
        room = self.findRoomFromUser(iUser)
        room.removeUser(iUser)
        print("USER REMOVED FROM ROOM")
                
    def deleteRoom(self,c,a):
        self.clearScreen(c,a)
        self.showAllRooms(c,a )
        self.sendToUser(c," \n\n Which Room do You want to delete? ")  
        (close, data) = self.receiveStrMessage(c, a)
        (exists, roomObj) = self.findRoom(data)
        
        if exists:
            while True:
                if roomObj.getIsVip():
                    self.sendToUser(c," \n\n Write the Room PassWord: ")
                else:
                    for n in range(len(self.roomVector)):
                        condName = self.roomVector[n].getName() == roomObj.getName()
                        condPassW = self.roomVector[n].getPass() == roomObj.getPass()
                        if condName:
                            if condPassW:
                                self.roomVector.remove(self.roomVector[n])
                                return True
                            else:
                                #ask password to client
                                while True:
                                    self.sendToUser(c," \n\n Wrong PassWord, Try again?(Y/n) ") 
                                    (close, yesNo) = self.receiveStrMessage(c, a)
                                
                                    condNo = (yesNo == "N") or (yesNo == "n") 
                                    condYes = (yesNo == "Y") or (yesNo == "y")
                                    if condYes:
                                        break
                                    elif condNo:
                                        return False
        else:
            self.sendToUser(c," \n\n Room doesn't exist ")  
            return False

    def whoAmItalkingTo(self, c, room):
        message = "LIST OF USERS: \n"
        self.sendToUser(c, " " + message + "\n\n")
        for rum in self.roomVector:
            if rum.getName() == room.getName():
                users = rum.getUsers()
                for u in users:
                    self.sendToUser(c,"\tUser: " + u.getName() +"\n")

    def showUsrInRoom(self, room):
        print("ROOM NAME: " + room.getName()+"\n")
        for rum in self.roomVector:
            if rum.getName() == room.getName():
                users = rum.getUsers()
                if (users is not None):
                    for u in users:
                        print("\tUser: " + u.getName() +"\n")
                        
    def showAllRooms(self,c,a):
        message = " Rooms Available: \n"
        self.sendToUser(c, message)
        for n in range(len(self.roomVector)):
            #print("\tVectroom: " + self.roomVector[n].getName()+ "\tPASSoom: " + self.roomVector[n].getPass())
            message = " " + self.roomVector[n].getName()
            if(self.roomVector[n].getIsVip()):
                message = message + " LOCKED" 
            message = message + " Users: " + str(self.roomVector[n].getNumberUsers()) 
            self.sendToUser(c, " " + message + "\n\n")

    def showRoomsMenu(self,c,a):
        self.showAllRooms(c,a)
        self.sendToUser(c," Press @ to go back")
        while True:
            (close, data) = self.recvMsg(c, a)
            isMenu = self.callMenu(c, a, data)
            if isMenu:
                break

    def updateRooms(self,iUser, msg):  
        try:
            msg = " " + str(iUser.getName()) + ": " + msg
        except(Exception):
            pass
        for rum in self.roomVector:
            users = rum.getUsers()
            if (users is not None):
                for u in users:
                    if str(u.getName()) == str(iUser.getName()):
                        self.sendToRoom(msg, rum, iUser)
                        return True
            else:
                print(str(rum.getName())+" Room Empty\n\n")
        return False


####MSG FUNCT

    def sendToRoom(self, msg, room, iUser):
        #for rum in self.roomVector:
        #    self.showUsrInRoom(rum)
        if room is not None:
            users = room.getUsers()  
            for u in users:
                #if str(u.getName()) != str(iUser.getName()):
                connection = u.getConnection()
                if connection is not None:
                    try:
                        #if msg is not None:
                        connection.send(bytes(msg, 'utf-8'))
                    except(ConnectionResetError):
                        #   Checks if connection was closed by peer
                        pass
                    except(Exception):
                        pass
        else:
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
        data = ''
        try:
            (close, data) = self.recvMsg(c, a)
            data = str(data, "utf-8")
            return (close, data)
        except:
            data = str(data, "utf-8")
            return (close, data)

    def recvMsg(self, c, a):
            close = False
            data = c.recv(self.SIZEMESSAGE)

            #   c is connection
            #   recv  = receiving data from the connection
            #   arg is number of bytes
            if not data:
                #self.disconnect(c, a)
                close = True
            else:
                data = str(data, "utf-8")
                data = bytes(data, 'utf-8')
            return (close, data)

    def sendFilesToRoom(self,room,iUser):
        if room is not None:
            users = room.getUsers()
            for u in users:
                if str(u.getName()) != str(iUser.getName()):
                    connection = u.getConnection()
                    if connection is not None:
                        try:
                            print("GOT HERE")
                            self.sendFiles2Client(connection)
                        except(ConnectionResetError):
                            #   Checks if connection was closed by peer
                            pass
                        except(Exception):
                            pass
        else:
            pass



    def sendFiles2Client(self,c):
        
        fileName='TD_work.pdf' #In the same folder or path is this file running must the file you want to tranfser to be
        path = self.createServerDir()
        filePath = path + "/" + fileName

        startFileTrans = bytes(self.charStartFileTrans,'utf-8')
        c.send(startFileTrans)
        print("Sending Files")

        with open(filePath, 'rb') as f:
            print("GOT HERE LAZY ASS")
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

####SERVER FUNCT

    def createServerDir(self):
        dir = ""
        dir = os.path.join(dir, 'ServerFiles')
        if not os.path.exists(dir):
            os.makedirs(dir)
        return dir

    def disconnect(self, c, a,  iUser):
        print(str(a[0]) + ": " + str(a[1]) + " disconnected")
        iUser.remConnection()
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


