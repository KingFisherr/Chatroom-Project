from asyncio.windows_events import NULL
import socket
import threading
import json
from crypter import AESCrypter
from dbmodels import database
import re

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

#list of admins 
admins = []

# List of usernames of connected clients
username_list = []

# Need function to receieve connection from client
def receive():
    while True:
        clientconn, address = server.accept()
        print (f"Connection to {address} established...")

        #Ask client for username
        clientconn.send("Username".encode())

        # Username var stores the username received from client
        user_pass_json = clientconn.recv(1024).decode()
        user_pass_json = json.loads(user_pass_json)

        username = user_pass_json[0]
        password = user_pass_json[1]

        # Check for ban database
        db.checkfordb('ban_database.sqlite')
        # Check if client is banned
        if db.checkban(username, password):
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


        # # Check for user database
        # db.checkfordb('user_database.sqlite')    
        # # Check if username exists
        # if db.checkusername(username): 
        #     # If username exists then verify login
        #     if db.checklogin(username, password):
        #         # This is an existing user
        #         continue
        #     else: 
        #         print ("Wrong password, reeenter")
        #         # We want to disconnect client so they retry password
        #         clientconn.send("WRONGPASS")
        #         clientconn.close()
        #         continue
        # else:
        #     db.storeuserinfo(username, password)

        

        # Update client list and username list with new client
        clients.append (clientconn)
        username_list.append(username)

        print(f"{username} is joining the server")
        
        # Call broadcast func to send a message to all clients
        broadcast(f"{username} has joined the server".encode(), clientconn)

        # Let client know they are now connected to the chat server
        clientconn.send("You are now connected to the live chat server".encode())

        # Handle multiple clients

        thread = threading.Thread(target=handler, args=(clientconn,))
        thread.start()

# Function sends message to all connected clients
def broadcast(messsage, client):
    for x in clients:
        if x == client:
            continue
        #time.sleep(0.5)
        x.send(messsage)

# to access the username list and search for name for ip
def transverse(names):
    for a in range(len(username_list)):
        if str(username_list[a]) == names:
            return clients[a]
    return -1

# use user ip address to find the username
def namelookup(ip_address):
    for g in range(len(clients)):
        if clients[g] == ip_address:
            return username_list[g]
    return -1

#check if user is admin 
def admincheck(usernamee):
    for good in admins:
        if good == usernamee:
            return True
    return False

#add user into admins
def adminadd(usernamess):
    admins.append(usernamess)



        


#we add commands here
def commands(message1, client):
    name_of_client = namelookup(client)

    if "/chatmember" in str(message1):
        final = str(username_list)
        client.send(final.encode())
    elif "/disconnect" in str(message1):
        client.close()
    elif "/help" in str(message1):
        if admincheck(name_of_client):
            client.send("Those are available commands: \n/chatmember\n/help\n/kick\n/ban\n/disconnect\n".encode())
        else:
            client.send("Those are available commands: \n/chatmember\n/help\n/disconnect\n".encode())
    elif "/kick" in str(message1) and admincheck(name_of_client):
        if re.search (r"kick\s.+",str(message1)):
            target = re.findall(r"kick\s.+",str(message1))
            target[0] = target[0].replace("kick ","")
            target[0] = target[0].replace("'","")
            if transverse(target[0]) != "-1":
                found = transverse(target[0])
                found.close()
            else:
                client.send("User doesn't exist please double check".encode())
        else:
            client.send("Please check if you have the right format for the command".encode())
    elif "/ban" in str(message1) and admincheck(name_of_client):
        if re.search (r"ban\s.+",str(message1)):
            target = re.findall(r"ban\s.+",str(message1))
            target[0] = target[0].replace("ban ","")
            target[0] = target[0].replace("'","")
            if transverse(target[0]) != "-1":
                found = transverse(target[0])
                db.storebaninfo(target[0],found)
                found.close()
            elif db.checkban(target[0],found):
                client.send("User is already Banned".encode())
            else:
                client.send("User doesn't exist please double check".encode())
        else:
            client.send("Please check if you have the right format for the command".encode())
    elif "/admin" in str(message1):
        client.send("Please enter the code you get from the Staff".encode())
        codes = client.recv(1024).decode()
        print(codes)
        txts = re.findall(r"\s.+",str(codes))
        print(txts[0])
        txts[0] = txts[0].replace(" ","")
        txts[0] = txts[0].replace("'","")
        print(txts[0])
        if txts[0] == "Passcodes": #you can change the password here
            adminadd(name_of_client)
            client.send("You are now an admin".encode())
        else:
            client.send("Wrong passcode, try again".encode())


        
    else:
        client.send("Command Not Found, Use /help to Check for Command".encode())

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
            broadcast(f'{username} has left the chat'.encode(), client)

            # Disconnect client from server and remove from list
            clients.remove(client)
            client.close()
            username_list.remove(username)
            break

# Need additional non core administrative functions or similiar

# Ready to receieve connection 
print ("Server open for connection")
receive()

db.storebaninfo()