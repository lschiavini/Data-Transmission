
from room import *
from user import *


roomVector = []

user1 = User()
user1.setName("Lucas1")


user2 = User()
user2.setName("Lucas2")

rum1 = Room()
rum1.setName("FirstRoom")
roomVector.append(rum1)

rum2 = Room()
rum2.setName("SecondRoom")
roomVector.append(rum2)

rum3 = Room()
rum3.setName("3Room")
roomVector.append(rum3)

rum4 = Room()
rum4.setName("4Room")
roomVector.append(rum4)

roomObj = Room()
roomObj.setName("FirstRoom")




#roomVector[2].addUser(user)
rum = rum1
rum.addUser(user1)

for r in roomVector:
        if r.getName() == rum.getName():
                roomVector.remove(r)
                roomVector.append(rum)

#roomVector[0].addUser(user1)
#
#roomVector[1].addUser(user2)


#n=0
#if (roomVector[n].getName() == roomObj.getName()):
#        rum = rum1
#        rum1.addUser(user1)
#        roomVector.remove(roomVector[n])
#        roomVector.append(rum1)


#for n in range(len(roomVector)):
#        print("ROOM:" + roomVector[n].getName() + "COMPARE2:" + roomObj.getName())
#        if (roomVector[n].getName() == roomObj.getName()):
#                roomVector[n].addUser(user) 
#                print("Added " + user.getName() +"\n")



print("LIST OF ROOMS" + "\n")
for rum in roomVector:
        print("ROOM NAME: " + rum.getName()+"\n")
        users = rum.getUsers()
        if (users is not None):
                for u in users:
                        print("User: " + u.getName() +"\n")