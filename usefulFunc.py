###UsefulFunctions
from server import *

class Routing():
    serverObj = []

    def __init__(self, server):
        self.serverObj = server

    def clearScreen(self):
        clearScreen = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        self.serverObj.sendMessage(clearScreen)
            
    def helpMessage(self):
        helpMessage = "<<<<<<Press @ any time for the menu to appear>>>>>>"
        self.serverObj.sendMessage(helpMessage)




#def showAllRooms(self,c,a):
#        message = " Rooms Available: \n"
#        self.sendToUsr(c, message)
#        for n in range(len(rooms)):
#            message = rooms[n].getName()
#            if(rooms[n].getIsVip()):
#                message = message + " LOCKED"  
#            self.sendToUsr(c,message)