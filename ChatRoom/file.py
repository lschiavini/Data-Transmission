from server import *
from room import *
from client import *

class File:

    
    def __init__(self, filename):
        self.fileName = filename
        self.serverDir = os.path.join("", 'ServerFiles/')
        self.localDir = os.path.join("", 'LocalFiles/')
    

    def setName(self, name):
        self.fileName = name
    
    def getName(self):
        return self.fileName

    def getServerDir(self):
        return self.serverDir

    def getLocalDir(self):
        return self.localDir
    
    def setServerDir(self, dir):
        aux = os.path.join("", dir)
        if not os.path.exists(aux):
            return False
        else:
            self.serverDir = os.path.join("", dir)
            return True

    def setLocalDir(self, dir):
            aux = os.path.join("", dir)
            if not os.path.exists(aux):
                return False
            else:
                self.localDir = os.path.join("", dir)
                return True

    
    
    
    
    

    