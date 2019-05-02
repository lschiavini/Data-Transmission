from server import *
from user import *

class Room:
    

    # if no passWord, not VIP check

    def __init__(self):#, namey = None, passey = None):
        
        self.users = []#Object Users
        self.numberUser = 0
        self.name = ""
        self.passW = "None"
        self.isVipVar = False   

    def setName(self, name):
        self.name = name
    
    def setPass(self, passW):
        self.passW = passW

    def getName(self):
        return self.name
    
    def getPass(self):
        return self.passW
    
    def getIsVip(self):
        return self.isVipVar

    def isVip(self, vipStatus):
        self.isVipVar = vipStatus
    
    def getNumberUsers(self):
        return self.numberUser

    def addUser(self, user):
        self.numberUser = self.numberUser + 1
        self.users.append(user)
    
    def removeUser(self, user):
        while user in self.users:
            if user in self.users:
                self.numberUser = self.numberUser - 1
            self.users.remove(user)
    
    
    def getUsers(self):
        return self.users
    
    def hasUser(self, iUser):
        for u in self.users:
            if(u.getName() == iUser.getName()):
                return True
        return False

    def __del__(self):
        #print("Room " + self.name + " deleted...")
        pass
