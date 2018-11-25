from server import *

class User:
    username = ""
    passWord = ""
    actualConnection = []
    actualRoom = []

    def __init__(self, user, passW, c, room = None):
        self.username = user
        self.passWord = passW
        self.actualConnection = c
        if (room != None):
            self.actualRoom = room

    def __init__(self):
        pass

    def setName(self, name):
        self.username = name
    def setPass(self, passW):
        self.passWord = passW

    def getName(self):
        return self.username
    def getPass(self):
        return self.passWord
    
    def setConnection(self, c):
        self.actualConnection = c
        
    def setRoom(self, room):
        self.actualRoom = room
    
    def getConnection(self):
        return self.actualConnection
    def getRoom(self):
        return self.actualRoom
    
    