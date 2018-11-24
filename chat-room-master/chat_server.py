#CHAT SERVER_SAVITHRU M LOKANATH

import socket
import re
import logging
from sys import argv                                #IMPORT LIBRARIES
from sys import stdout
from threading import Thread, Timer
import datetime 
import os
import os.path
import logging

logging.basicConfig(level=logging.INFO, filename='chatserver.log', format='[%(levelname)s] %(asctime)s %(threadName)s %(message)s', ) 

#INITIALIZATION

buffer_size = 8192
host = '127.0.0.1'
backlog = 10                                #Connections in queue
block_time = 60                             #Blocking time if login fails for 3 consecutive times
time_expire = 30 * 60                       #Expiry time if user fails to logout

#COMMANDS 

WHO_ELSE_CONNECTED = 'whoelse'
BROADCAST = 'broadcast' 
MESSAGE = 'message'
LOGOUT = 'logout' 
SENDFILE = 'sendfile'

#DICTIONARY

commands_dict = {
    WHO_ELSE_CONNECTED : 'Display all chat memebers online ',
    BROADCAST : 'Send a message to the entire chat room. Type \'3 <content>\'',
    MESSAGE : 'Send a private message to someone. Type \'1 <destination clientname> <content>\' ',             
    LOGOUT : 'Disconnect this session.',
    SENDFILE : 'Send a file to another chat member. Type 2 <destination username> <filepath>'
}

logged_in_users = []                    #Stores the logged in users
past_connections = {}                   #Stores who else is there
blocked_connections = {}                #Stores the blocked users due to blocking function

#FUNCTION TO FIND WHO IS THERE ONLINE 

def who_else(client, sender_username):
    other_users = 'Users currently logged in: ' 
    
    for user in logged_in_users:
        if (user[0] != sender_username):
            other_users += user[0] + ' '
    
    if (len(logged_in_users) < 2):     #If no client is online 
        other_users += '[none] '
    
    client.sendall(other_users)

#BROADCAST FUNCTION

def broadcast(user, command):
    message = 'Braodcast message from ' + user + ': '
    
    for word in command[1:]:
        message += word + ' '        #Broadcasts to all Users

    for user_tuple in logged_in_users:
        user_tuple[1].sendall(message)

#PRIVATE MESSAGE TO USER FUNCTION

def private_message(sender_username, client, command):
    message = 'Private message from ' + sender_username + ': '
    
    receiver = command[1]
    
    for word in command[2:]:
        message += word + ' '
    
    receiver_is_logged_in = False
    for user_tuple in logged_in_users:
        if user_tuple[0] == receiver:
            user_tuple[1].sendall(message)         #Send Message to a private user
            receiver_is_logged_in = True
    
    if (not receiver_is_logged_in):
        client.sendall(receiver + ' is not logged in. ')   #If user is not online

#SENDFILE FUNCTION

def sendfile(sender_username, client, command):
    message = 'File from ' + sender_username + ': '   

    receiver = command[1]                           #Destination clientname
    path = command[2]                               #File path
    receiver_is_logged_in = False
    
    if os.path.isfile(path):
        #print "file exists"                        #Check if file exists 
        a = path.rsplit('/')
        b = a[4]
        #print b
        logging.info("File {} Sent".format(b))


        rd = open(path, "rb")
        data = rd.read()
        #print data
        
        for user_tuple in logged_in_users:
            if user_tuple[0] == receiver:
                #user_tuple[1].send(message)           #Send to user
                user_tuple[1].sendall(data)
                receiver_is_logged_in = True

    else:
        client.sendall('File does not exists.\n')       #Send this if file does not exist

#LOGOUT FUNCTION

def logout(client):
    client.sendall('Good bye!')
    client.close() 

#EXIT FUNCTION

def client_exit(client, client_ip, client_port):
    for user in logged_in_users:
        if user[1] == client:
            logged_in_users.remove(user)
    print 'Client on %s : %s disconnected' %(client_ip, client_port)
    logging.info("Client on IP {} & Port {} Disconnected".format(client_ip, client_port))
    open("/Users/savithru/Desktop/user_pass.txt", 'w').close()              #Clear user list & password in saved file
    stdout.flush()     
    client.close()

#TIMEOUT FUNCTION

def client_timeout(client, client_identifier):
    client.sendall('Your session has been ended due to inactivity. ')    #If not active for 30 minutes, end session
    client.close()


#PROMPT COMMANDS 

def prompt_commands(client, client_ip_and_port, username):    
    while 1:
        try:
            client.sendall('\nEnter the number command:\n 1. Message\n 2. Sendfile\n 3. Broadcast\n 4. Whoelse\n 5. Logout\n  ')
            
            timeout_countdown = Timer(time_expire, client_timeout, (client, client_ip_and_port))     #Start Timeout_timer
            timeout_countdown.start()
            
            command = client.recv(buffer_size).split()
            timeout_countdown.cancel() 
            past_connections[username] = datetime.datetime.now() 
        
        except:                                                     #Handle exception errors  
            logout(client)
            client.close()
        
        if (command[0] == "1"):
            private_message(username, client, command)

        elif (command[0] == "2"):
            sendfile(username, client,command)
              
        elif (command[0] == "3"):                                   #PROMPTS
            broadcast(username, command)

        elif (command[0] == "4"):
            who_else(client, username)
            
        elif (command[0] == "5"):
            logout(client)
            
        else:
            client.sendall('Command not found. ')

#WELCOME FUNCTION

def login(client, username):
    client.sendall('\nLogin successful. Welcome to ChatRoom_Savithru!')
    logged_in_users.append((username, client))                              #Add to list
    past_connections[username] = datetime.datetime.now() 

#BLOCK FUNCTION

def block(ip_addr, client_sock, username):    
    list_of_blocked_usernames = blocked_connections[ip_addr]
    list_of_blocked_usernames.append(username)                              #Add to list
    blocked_connections[ip_addr] = list_of_blocked_usernames
    client_sock.close()

#UNBLOCK FUNCTION

def unblock(ip_addr, username):
    list_of_blocked_usernames = blocked_connections[ip_addr]
    list_of_blocked_usernames.remove(username)                              #Add to list
    blocked_connections[ip_addr] = list_of_blocked_usernames


def is_blocked(ip_addr, username):
    list_of_blocked_usernames = blocked_connections[ip_addr]
    if (username in list_of_blocked_usernames):
        return True
    return False

#IF ALREADY USER IS LOGGED IN FUNCTION

def is_already_logged_in(username):
    for user in logged_in_users:
        if user[0] == username:
            return True
    return False

#LOGIN FUNCTION

def prompt_login(client_sock, client_ip, client_port):
    username = 'default'
    
    while (not username in logins):
        client_sock.sendall('\nPlease enter a valid username. ')
        username = client_sock.recv(buffer_size) 
    
        if (is_blocked(client_ip, username)):                               #Check if Blocked
            client_sock.sendall('Your access is temporarily blocked.')
            username = 'default'
        
        if (is_already_logged_in(username)):
            client_sock.sendall('This user has already logged in.')         #Check is user is logged in
            username = 'default'
    
    login_attempt_count = 0

    while login_attempt_count < 3:                                          #If login < 3 continue
        client_sock.sendall('Please enter your password. ')
        password = client_sock.recv(buffer_size) 
        
        if (logins[username] != password):
            login_attempt_count += 1
            client_sock.sendall('Wrong Username or Password. Please try again. ')
        
        elif (logins[username]) and (logins[username] == password):
            login(client_sock, username)
            return (True, username)
    
    return (False, username)

#NEW USER ACCOUNT CREATION FUNCTION

def prompt_create_username(client_sock):
    client_sock.sendall('Welcome to ChatRoom_Savithru! Would you like to create a new user? [yes/no]')
    response = client_sock.recv(buffer_size)
    
    if (response == "yes"):
        created_username = False
        new_user = ""
        while (not created_username):
            client_sock.sendall('Please choose a username. ')
            new_user = client_sock.recv(buffer_size)
            
            if (len(new_user) < 3 or len(new_user) > 8):
                client_sock.sendall('Usernames must be between 3 and 8 characters long. ')    
            
            elif (new_user in logins):
                client_sock.sendall('This username already exists! Please choose another!')
            else:
                created_username = True
        
        new_pass = ""
        created_password = False
        while (not created_password):
            client_sock.sendall('Please type in a secure password. ')
            new_pass = client_sock.recv(buffer_size)
            
            if (len(new_pass) < 4 or len(new_pass) > 8):
                client_sock.sendall('Passwords must be between 4 and 8 characters long.')  #PASSWORD ENTER
            else:
                created_password = True
        
        with open('/Users/savithru/Desktop/user_pass.txt', 'a') as aFile:
            aFile.write('\n' + new_user + ' ' + new_pass)                                   #STORE PASSWORD
        
        logins[new_user] = new_pass
        
        client_sock.sendall('New user created.\n')

#CLIENT HANDLE FUNCTION

def handle_client(client_sock, client_ip_and_port):
    client_ip = client_ip_and_port[0]                           #CLIENT IP
    client_port = client_ip_and_port[1]                         #CLIENT PORT
    
    if (not blocked_connections.has_key(client_ip)):
        blocked_connections[client_ip] = []
    
    prompt_create_username(client_sock)
    
    try:
        while 1:
            user_login = prompt_login(client_sock, client_ip, client_port)
            #print "xxxxxx"
            #print user_login
            logging.info("User Login Info = {}".format(user_login))

            if (user_login[0]):                                                         #If login succeeds
                prompt_commands(client_sock, client_ip_and_port, user_login[1])
                
            else: 
                  
                client_sock.sendall('Login failed too many times. Please try after 60 seconds') #If login fails
                block(client_ip, client_sock, user_login[1])
                Timer(block_time, unblock, (client_ip, user_login[1])).start()
    except:
        client_exit(client_sock, client_ip, client_port)

#POPULATE DICTIONARIES WITH DATA

def populate_logins_dictionaries():
    user_logins = {}

    with open('/Users/savithru/Desktop/user_pass.txt') as aFile:
        for line in aFile:
            (key, val) = line.split()
            user_logins[key] = val

    return user_logins

#MAIN THREADING FUNCTION

def main(argv):
    server_port = 9528                                            #Server Port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host,server_port))                                   #Bind the socket
    sock.listen(backlog)
    print 'Server on port ' + str(server_port)
    logging.info("The chat server is running on IP address 127.0.0.1 & on PORT number {}".format(server_port))
    stdout.flush()
    
    try:
        while 1:
            client_connection, addr = sock.accept()                                 
            print 'Client connected on '  + str(addr[0]) + ':' + str(addr[1])
            logging.info("Chat Client Connected on IP {} & Port {}".format(host, server_port)) 
            stdout.flush()
            thread = Thread(target=handle_client, args=(client_connection, addr))   #Start a thread & connect
            thread.start()
    except (KeyboardInterrupt, SystemExit):
        stdout.flush()
        open("/Users/savithru/Desktop/user_pass.txt", 'w').close()                  #On keyboard interrupt EXIT
        print '\nServer shut down.'
        
logins = populate_logins_dictionaries()
main(argv)
