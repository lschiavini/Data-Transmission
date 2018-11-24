class chatRoomApp:
    #__ means private
    __users = []
    __vipRooms = []
    __Rooms = []



class Room:
    name = ""
    passW = ""
    isVip = False
    # if no passWord, not VIP check

    def __init__(self):
        yesNo = ""
        condNo = (yesNo != "N") || (yesNo != "n") 
        condYes = (yesNo != "Y") || (yesNo != "y")

        self.name = input("Set up the name of the Room: ") 
        while (condYes||condNo):
            yesNo = input("Do you want a password? (Y/n)")
        if condYes:
            self.isVip = True
        
    def __del__(self):
        pass

        
    


class Users(Client):
    name = ""
    passW = ""
    pairNamePass = []
    
    def __init__(self):
        self.name = input("Tell us your name: ")
        self.passW = input("Choose a Password")
        self.pairNamePass = append(self.name)
        self.pairNamePass = append(self.passW)
        
    def checkUsr(self):
        oldName = self.name
        oldpassW = self.passW

        condName = (oldName == self.pairNamePass[0])
        condpassW = (oldpassW == self.pairNamePass[1])

        if (condName && condpassW):
            return True
        else:
            return False  

    


