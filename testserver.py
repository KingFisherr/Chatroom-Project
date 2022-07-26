import socket
import threading
import json
import re
from crypter import AESCrypter
from dbmodels import database

# Create database object from dbmodels
db = database()
# Create encryption/decryption object from cypter 

# Establish server host and port via socket object
host = "127.0.0.1"
port = 1338

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))

# Start listening
server.listen()

# List of connected clients
clients = [] 

# List of usernames of connected clients
username_list = []

# List of admins
admins = []

# Functions handles messages sent to server by clients
def handler(client):

    while True:
        try:
            # Get message from client
            message = client.recv(1024)

            #search for command
            if re.search (r":\s/.*",str(message)):
                commands(message, client)

            # Broadcast message to all clients
            else:
                broadcast(message, client)

            # Implement function or add on to this function for file transfer functionality
            
        except:
            # Broadcast the user has disconnected
            index = clients.index(client)
            username = username_list[index]
            client.close()
            broadcast_disconnected(f"{username} has left the chat\n".encode(), client)

            # Disconnect client from server and remove from list
            clients.remove(client)
            #client.close()
            username_list.remove(username)
            break

# Need function to receieve connection from client
def receive():
    while True:
        clientconn, address = server.accept()
        print (f"Connection to {address} established...")

        #Ask client for username
        clientconn.send("Username".encode())

        # user_pass_json var stores the username and password received from client as json
        user_pass_json = clientconn.recv(1024).decode()
        #print (user_pass_json)
        user_pass_json = json.loads(user_pass_json)

        username = user_pass_json[0]
        password = user_pass_json[1]

        # username = clientconn.recv(1024).decode()
        # password = "banana"

        # Check if user is already in server, by checking username/client ip list
        if (ifuserexists(username)):
            clientconn.send("Duplicate".encode())
            clientconn.close()
            continue
        # Notes argument taken in to IP

        # Check for ban database
        db.checkfordb('ban_database.sqlite')
        # Check if client is banned
        if db.checkban(username):
            # If client is on ban list send them ban message
            clientconn.send("Banned".encode())
            # Disconnect client from server
            clientconn.close()
            continue
        
        # NOTES
        # Currently we can kick banned user when they connect to server via username and password, should just be socket (ip address)
        # Need to fix login checker

        # We have a username and password
        # First check user_info database to see if given username exists
            # If it exists we can verify both username and password
            # Else we will store the new username and password


        # Check for user database
        db.checkfordb('user_database.sqlite')    
        # Check if username exists
        if db.checkUsername(username): 
            print ("Username exists")
            # If username exists then verify login
            if not db.checklogin(username, password):
                print("Password does not match")
                # We want to disconnect client so they retry password
                clientconn.send("Wrongpass".encode())
                clientconn.close()
                continue
        else:
            print ("Stored new user info")
            db.storeuserinfo(username, password)

        
        # Update client list and username list with new client
        clients.append (clientconn)
        username_list.append(username)

        print(f"{username} is joining the server")
        
        # Call broadcast func to send a message to all clients
        broadcast_disconnected(f"{username} has joined the server\n".encode(), clientconn)

        # Let client know they are now connected to the chat server
        clientconn.send("You are now connected to the live chat server\n".encode())

        # Handle multiple clients
        handlerthread = threading.Thread(target=handler, args=(clientconn,))
        handlerthread.start()

# Function sends message to all clients
def broadcast(messsage, client):
    for x in clients:
        x.send(messsage)

# Function sends message only to all connected clients
def broadcast_disconnected(messsage, client):
    for x in clients:
        if x == client:
            continue
        x.send(messsage)

# Need additional non core administrative functions or similiar
def ifuserexists(username):
    if username in username_list:
        return True
    else:
        False

# to access the username list and search for name for ip
def transverse(names):
    # transverse the user list one by one
    for num in range(len(username_list)):
        #if they found the user. then return the ip address according to the client list.
        if str(username_list[num]) == names:
            return clients[num]
    #if we can't find anything we return -1
    return -1

# use user ip address to find the username
# this is similar function to the transverse function. We use ip address to find the username this time
def namelookup(ip_address):
    for g in range(len(clients)):
        if clients[g] == ip_address:
            return username_list[g]
    #if we can't find anything we return -1
    return -1

#check if user is admin 
def admincheck(usernamee):
    #check through the admin list to see if a user is inside the admin list
    for good in admins:
        # if we found the user then return true
        if good == usernamee:
            return True
    #if not return false
    return False

#add user into admins
def adminadd(usernamess):
    admins.append(usernamess)

#kick function
def kick(mess,client1):
    # if they found kick inside the message
    if re.search (r"kick\s.+",str(mess)):
        #extract the message from the text
        target = re.findall(r"kick\s.+",str(mess))
        target[0] = target[0].replace("kick ","")
        target[0] = target[0].replace("'","")
        target[0] = target[0].replace("n","")
        target[0] = target[0].replace("\\","")
        print(mess)
        print(target[0])
        print(transverse(target[0]))
        #if they found a client ip address with transverse function
        if str(transverse(target[0])) != "-1":
            found = transverse(target[0])
            #close the GUI
            found.send("Exit".encode())
            # then we disconnect them
            found.close()
        #if the function can't find a user, then there exist no user in the database
        else:
            client1.send("User doesn't exist please double check\n".encode())
    #if we didnt have a "/kick user" in the format then we will return the message.
    else:
        client1.send("Please check if you have the right format for the command\n".encode())

# current number of people inside the chat room
def chat_member(client1):
    #send the list of username to the user
    final = str(username_list)
    client1.send(final.encode())

# help function, to send out the commands
def helps(client1,client_name):
    #if they found client name under the admin list
    if admincheck(client_name):
        client1.send("Those are available commands: \n/chatmember\n/help\n/kick\n/ban\n/disconnect\n".encode())
    # if not then return regular user list
    else:
        client1.send("Those are available commands: \n/chatmember\n/help\n/disconnect\n".encode())


#ban function, to ban a user from branch
def bans(mess,client1):
    #if it picks up subject
    if re.search (r"ban\s.+",str(mess)):
        #extract the subject from the message
        target = re.findall(r"ban\s.+",str(mess))
        target[0] = target[0].replace("ban ","")
        target[0] = target[0].replace("'","")
        target[0] = target[0].replace("n","")
        target[0] = target[0].replace("\\","")
        # if subject is found in the user list
        print(mess)
        print(target[0])
        print(transverse(target[0]))
        if str(transverse(target[0])) != "-1":
            found = transverse(target[0])
            #ban it and disconnect it
            db.storebaninfo(target[0],found)
            #close the GUI
            found.send("Exit".encode())
            # close client
            found.close()
        # else return a message if didnt find the subject in the database
        else:
            client1.send("User doesn't exist please double check\n".encode())
    # if didnt find the subjest in the text
    else:
        client1.send("Please check if you have the right format for the command\n".encode())


#admin function,make a user to become admin
def New_admin(client1,name_client):
    client1.send("Please enter the code you get from the Staff\n".encode())
    #receive code from the user
    codes = client1.recv(1024).decode()
    #extract the code from the message
    txts = re.findall(r"\s.+",str(codes))
    txts[0] = txts[0].replace(" ","")
    txts[0] = txts[0].replace("'","")
    #if password matches, then add user into admin list
    if txts[0] == "Passcodes": #you can change the password here
        adminadd(name_client)
        client1.send("You are now an admin\n".encode())
    # send a message if the passcode is wrong
    else:
        client1.send("Wrong passcode, try again\n".encode())

# We need function that starts image sending process
# We have client 1, name of file, buffer of file, and client 2
# We send "sendimage" signal to client 1
    # Client 1 sends file data
    # We save it to a var in server
# We send recvimage signal to clien 2
    # Server sends file data to client
    # Client 2 saves in file
    # client1.send("SendImage".encode())
    # file = open('gotit.jpg', 'wb')
    # image_data = client1.recv(2048)
    # while image_data:
    #     file.write(image_data)
    #     image_data = client1.recv(2048)
    #     # if "Done" in image_data:
    #     #     break
    # print ("We got the whole image")
    # file.close()     

    # We have issue where after sending image to server, we cannot send messages     
    #### Currently we get stuck receivbeing the image even after client is done sending
    
#we add commands here
def commands(message1, client):
    name_of_client = namelookup(client)

    if "/chatmember" in str(message1):
        chat_member(client)
    elif "/disconnect" in str(message1):
        client.close()
    elif "/help" in str(message1):
        helps(client,name_of_client)
    elif "/kick" in str(message1) and admincheck(name_of_client):
        kick(message1,client)
    elif "/ban" in str(message1) and admincheck(name_of_client):
        bans(message1,client)
    elif "/admin" in str(message1):
        New_admin(client,name_of_client)



        
    else:
        client.send("Command Not Found, Use /help to Check for Command\n".encode())

# Ready to receieve connection 
print ("Server open for connection")
receive()
