from server import *
from room import *

class User:

    
    hasConn = False
    def __init__(self):
        self.username = ""
        self.passWord = ""
        self.actualConnection = []
        self.actualPort = []
        self.hasConn = False


    def setName(self, name):
        self.username = name
    def setPass(self, passW):
        self.passWord = passW

    def getName(self):
        return self.username
    def getPass(self):
        return self.passWord
    
    def setConnection(self, c, a):
        self.hasConn = True
        self.actualConnection = c
        self.actualPort = a

    def hasConnection(self):
        return self.hasConn

    def getConnection(self):
        return self.actualConnection
    
    def getPort(self):
        return self.actualPort
    
    def remConnection(self):
        self.hasConn = False
        self.actualConnection = None
        self.actualPort = None

    

    