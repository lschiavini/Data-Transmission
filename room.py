from server import *

class Room:
    name = ""
    passW = "None"
    isVip = False
    numberUser = 0
    
    users = []#Object Users

    # if no passWord, not VIP check

    def __init__(self, namey = None, passey = None):
        yesNo = ""
        condNo = (yesNo != "N") or (yesNo != "n") 
        condYes = (yesNo != "Y") or (yesNo != "y")
        
        #easy debug code for name pass room
        condNameNone = namey == None
        condPassNone = passey == None
        self.name = namey
        self.passW = "None"
        if not (condNameNone and condPassNone):
            pass
        #finish easy debug for name pass room
        else:
            self.name = input("Set up the name of the Room: ") 
            while (condYes or condNo):
                yesNo = input("Do you want a password? (Y/n)")
                if condYes:
                    self.isVip = True
                    self.passW = input("Set up the password of the Room: ")
                    break
                else:
                    self.passW = "None"
                    break
    def getName(self):
        return self.name
    
    def getPassW(self):
        return self.passW
    
    def isVip(self):
        return self.isVip
    
    def getNumberUsers(self):
        return self.numberUser

    def addUser(self, usrName, c):
        self.numberUser = self.numberUser + 1
        self.users.extend[user]
    
    def getUsers(self):
        return self.users

    def __del__(self):
        print("Room " + self.name + " deleted...")

