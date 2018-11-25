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