from server import *
from room import *

class User:
    username = ""
    passWord = ""
    actualConnection = []
    hasConn = False

    def __init__(self, user, passW, c, room = None):
        self.username = user
        self.passWord = passW
        self.actualConnection = c
        
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
        self.hasConn = True
        self.actualConnection = c    
    def hasConnection(self):
        return self.hasConn
    def getConnection(self):
        return self.actualConnection
    

    