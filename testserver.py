import os
import re
import json
import time
import socket
import bcrypt
import threading
from dbmodels import database
from crypter import AESCrypter
from base64 import b64encode, b64decode
from Crypto.Random import get_random_bytes

# Create database object from dbmodels
db = database()
# Create encryption/decryption object from cypter 

# Establish server host and port via socket object
host = "127.0.0.1"
port = 1400

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

# List of crypters
crypters = []


# Need function to receieve connection from client
def receive():
    while True:
        clientconn, address = server.accept()
        print(f"Connection to {address} established...")

        # Ask client for username
        clientconn.send("Username".encode())

        # user_pass_json var stores the username and password received from client as json
        user_pass_json = clientconn.recv(1024).decode()
        # print (user_pass_json)
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

        # init crypter
        crypter = AESCrypter()
        send_iv = get_random_bytes(16)
        recv_iv = get_random_bytes(16)
        crypter.init_cipher(send_iv, recv_iv)

        clientconn.send("IV".encode())
        time.sleep(1)
        clientconn.send(b64encode(recv_iv))
        clientconn.send(b64encode(send_iv))

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
        print("enters check")
        if db.checkUsername(username):
            print("Username exists")
            # If username exists then verify login
            if not db.checkloginHash(username, password):
            #if not db.checklogin(username, password):
                print("Password does not match")
                # We want to disconnect client so they retry password
                clientconn.send("Wrongpass".encode())
                clientconn.close()
                continue
        else:
            # user cannot enter hashed password so it will not match database
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(13))
            # print (f'before stored {hashed}')
            # checking if DB exists before trying to store
            db.checkfordb('user_database.sqlite')
            db.storeuserinfo(username, hashed.decode())
           

        # Update client list and username list with new client
        crypters.append(crypter)
        clients.append(clientconn)
        username_list.append(username)

        print(f"{username} is joining the server")

        # Call broadcast func to send a message to all clients
        broadcast(f"{username} has joined the server\n", clientconn)

        # Let client know they are now connected to the chat server
        # clientconn.send("You are now connected to the live chat server".encode())

        cstr = crypter.encrypt_string("You are now connected to the live chat server\n")
        clientconn.send(cstr)

        # Handle multiple clients
        handlerthread = threading.Thread(target=handler, args=(clientconn,))
        handlerthread.start()


def client_to_crypter(client):
    # get the index of the target client
    index = clients.index(client)
    # get the crypter of the target client
    return crypters[index]


# Functions handles messages sent to server by clients
def handler(client):
    crypter = client_to_crypter(client)

    while True:
        try:
            # Get message from client
            message = client.recv(1024)
             # data = {"type":"File", "body":"chatroom or client"}

            if message == b"":
                raise Exception("exception: received empty string")

            #print("Cypher text = {}".format(message.decode()))
            # broadcast(f"Cypher text = {message}\n", client)
            dmsg = crypter.decrypt_string(message)

            temp = dmsg.decode()

            if temp == "SENDXX":
                #if filePermission(client) == "SERVER":
                sendfile(client)
            # WE can use {"type":"Text", "body":"the message"} to decipher for command, reg message, or a file
            # data = {"type":"File", "body":"path"}
            
            if temp == "RECVXX":
                send_to_client(client)
            #data = json.loads(dict from client)
            # If type = message
            # Elif type = file
                # Sendfile func
            # Elif type = command


            #search for command
            # print (f"THIS IS DSMG {dmsg.decode()}")
            if re.search (r":\s/.",str(dmsg)):
                broadcast_single(dmsg, client)
                commands(dmsg, client)

            # Broadcast message to all clients
            elif re.search (r"@.",str(dmsg)):
                ping(dmsg, client)
                broadcast(dmsg.decode(), client)


            # print("received {}".format(dmsg.decode()))

            else:
                # Broadcast message to all clients
                print("received {}".format(dmsg.decode()))
                broadcast(dmsg.decode(), client)

            # Implement function or add on to this function for file transfer functionality

        except Exception as ex:
            print(ex)
            # Broadcast the user has disconnected
            index = clients.index(client)
            username = username_list[index]
            broadcast(f'{username} has left the chat\n', client)

            # not thread safe, data race
            # Disconnect client from server and remove from list
            crypters.remove(crypter)
            username_list.remove(username)
            clients.remove(client)
            client.close()
            break


# Function sends message to all clients
def broadcast(message, client):
    #print(f"broadcasting {message}")
    print(message)
    for x in clients:
        # skip the sender
        # if x == client:
        #     continue

        try:
            crypter = client_to_crypter(x)
            # encrypt the message to send
            emsg = crypter.encrypt_string(message)
            # ( ( ( hacky sleep cuz no size header ) ) )
            #time.sleep(0.5)
            # send the message to the target clientss
            x.send(emsg)
        except Exception as ex:
            print(ex)


# Function sends message only to all connected clients
def broadcast_disconnected(message, client):
    for x in clients:
        if x == client:
            continue
        else:     
            crypter = client_to_crypter(x)
            emsg = crypter.encrypt_string(message)
            x.send(emsg)

def broadcast_single(message, client):
    for x in clients:
        if x == client:
            try:
                crypter = client_to_crypter(x)
                # encrypt the message to send
                emsg = crypter.encrypt_string(message)
                # ( ( ( hacky sleep cuz no size header ) ) )
                #time.sleep(0.5)
                # send the message to the target clientss
                x.send(emsg)
            except Exception as ex:
                print(ex)


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
        # if they found the user. then return the ip address according to the client list.
        if str(username_list[num]) == names:
            return clients[num]
    # if we can't find anything we return -1
    return -1


# use user ip address to find the username
# this is similar function to the transverse function. We use ip address to find the username this time
def namelookup(ip_address):
    for g in range(len(clients)):
        if clients[g] == ip_address:
            return username_list[g]
    # if we can't find anything we return -1
    return -1


# check if user is admin
def admincheck(usernamee):
    # check through the admin list to see if a user is inside the admin list
    for good in admins:
        # if we found the user then return true
        if good == usernamee:
            return True
    # if not return false
    return False


# add user into admins
def adminadd(usernamess):
    admins.append(usernamess)

#ping function
def ping(message1,client1):
    crypter = client_to_crypter(client1)
    if re.search (r"@.+",str(message1)):
        #extract the message from the text
        target = re.findall(r"@.+",str(message1))
        target[0] = target[0].replace("'","")
        target[0] = target[0].replace("\\n","")
        # split them withg space
        lists = target[0].split(' ')
        print("message before ",message1)
        print("extracted ",target[0])
        print("this is list ",lists)
        # for each word between space
        for i in lists:
            #if there's @ inside the word
            if "@" in i:
                #extract name
                i = i.replace("@","")
                #see if the name is exist in chatroom
                if str(transverse(i)) != "-1":
                    found = transverse(i)
                    # ping it 
                    found.send("Pinged".encode())
                    client1.send(crypter.encrypt_string("Pinged!\n"))
                else:
                    client1.send(crypter.encrypt_string("user"))
    #if we didnt have a "@user" in the format then we will return the message.
    else:
        client1.send(crypter.encrypt_string("Please check if you have the right format for the command\n"))

# kick function
def kick(mess, client1):
    crypter = client_to_crypter(client1)
    # if they found kick inside the message
    print("this is mess :",mess)
    if re.search(r"kick\s.+", str(mess)):
        # extract the message from the text
        target = re.findall(r"kick\s.+", str(mess))
        target[0] = target[0].replace("kick ", "")
        target[0] = target[0].replace("'", "")
        #target[0] = target[0].replace("n", "")
        target[0] = target[0].replace("\\n", "")
        print(mess)
        print(target[0])
        print(transverse(target[0]))
        # if they found a client ip address with transverse function
        if str(transverse(target[0])) != "-1":
            found = transverse(target[0])
            # close the GUI
            found.send("Exit".encode())
            # then we disconnect them
            #found.close()
        # if the function can't find a user, then there exist no user in the database
        else:
            client1.send(crypter.encrypt_string("User doesn't exist please double check\n"))
            #client1.send("User doesn't exist please double check\n".encode())
    # if we didnt have a "/kick user" in the format then we will return the message.
    else:
        client1.send(crypter.encrypt_string("Please check if you have the right format for the command\n"))
        #client1.send("Please check if you have the right format for the command\n".encode())



# current number of people inside the chat room
def chat_member(client1):
    crypter = client_to_crypter(client1)
    #send the list of username to the user
    final = str(username_list)+"\n"
    client1.send(crypter.encrypt_string(final))


# help function, to send out the commands
def helps(client1, client_name):
    # if they found client name under the admin list
    if admincheck(client_name):
        crypter = client_to_crypter(client1)
        help_message = "Those are available commands: \n/chatmember\n/help\n/kick\n/ban\n/disconnect\n"
        help_message = crypter.encrypt_string(help_message)
        client1.send(help_message)        
        #client1.send("Those are available commands: \n/chatmember\n/help\n/kick\n/ban\n/disconnect\n".encode())
    # if not then return regular user list
    else:
        crypter = client_to_crypter(client1)
        help_message = "Those are available commands: \n/chatmember\n/help\n/disconnect\n"
        help_message = crypter.encrypt_string(help_message)
        client1.send(help_message)        
        #client1.send("Those are available commands: \n/chatmember\n/help\n/disconnect\n".encode())


# ban function, to ban a user from branch
def bans(mess, client1):
    crypter = client_to_crypter(client1)
    # if it picks up subject
    if re.search(r"ban\s.+", str(mess)):
        # extract the subject from the message
        target = re.findall(r"ban\s.+", str(mess))
        target[0] = target[0].replace("ban ", "")
        target[0] = target[0].replace("'", "")
        target[0] = target[0].replace("n", "")
        target[0] = target[0].replace("\\", "")
        # if subject is found in the user list
        print(mess)
        print(target[0])
        print(transverse(target[0]))
        if str(transverse(target[0])) != "-1":
            found = transverse(target[0])
            # ban it and disconnect it
            db.storebaninfo(target[0], found)
            # close the GUI
            found.send("Exit".encode())
            # close client
            #found.close()
        # else return a message if didnt find the subject in the database
        else:
            client1.send(crypter.encrypt_string("User doesn't exist please double check\n"))
    # if didnt find the subjest in the text
    else:
        client1.send(crypter.encrypt_string("Please check if you have the right format for the command\n"))


# admin function,make a user to become admin
def New_admin(client1, name_client):
    crypter = client_to_crypter(client1)
    client1.send(crypter.encrypt_string("Please enter the code you get from the Staff\n"))
    # receive code from the user
    codes = client1.recv(1024).decode()
    dcode = crypter.decrypt_string(codes)
    # extract the code from the message
    txts = re.findall(r"\s.+", str(dcode))
    #print("codes: ",txts)
    txts[0] = txts[0].replace(" ", "")
    txts[0] = txts[0].replace("'", "")
    txts[0] = txts[0].replace("\\n", "")
    # print("Acodes: ",txts)
    # if password matches, then add user into admin list
    if txts[0] == "Passcodes":  # you can change the password here
        adminadd(name_client)
        client1.send(crypter.encrypt_string("You are now an admin\n"))
    # send a message if the passcode is wrong
    else:
        client1.send(crypter.encrypt_string("Wrong passcode, try again\n"))

def filePermission(client1):
    crypter = client_to_crypter(client1)
    client1.send(crypter.encrypt_string("Do you want send file to chatroom or a client?\n"))
    answer = client1.recv(1024).decode()
    answer_decoded = crypter.decrypt_string(answer)
    regexp = re.compile(r'SERVER')
    if regexp.search(answer_decoded):
        return "SERVER"
    else:
        return "CLIENT"

# Function to send files to server
# After update handler will call sendfile when it receives type file
def sendfile(client1):
    # We need to tell client we are ready to recieve a file 
    client1.send("SendImage".encode())
    crypter = client_to_crypter(client1)
    # We need to send name of file to client client1.send("Imagename.encode")
    remaining = client1.recv(1024).decode()
    temp_rem = remaining
    remaining = int(remaining)
    client1.send(crypter.encrypt_string(f"You are sending file of size: {remaining}\n"))
    with open('gotit.jpg','wb') as file:
        while remaining:
            image_data = client1.recv(min(4096,remaining))
            remaining -= len(image_data)
            file.write(image_data)
        file.close()
        help_message = "Server has received the entire file\n"       
        help_message = crypter.encrypt_string(help_message)
        client1.send(help_message)  

def send_to_client(client1):
    client1.send("RecvImage".encode())
    fileToSend = open('gotit.jpg', 'rb')
    fileToSend.seek(0, os.SEEK_END)
    file_size = fileToSend.tell()
    data_message = client1.recv(1024).decode()
    if data_message == "READYTORECV":
        print("Size of file is :", file_size,"bytes")
        client1.send(str(file_size).encode())
        fileToSend.seek(0,0)
        print ("Sending file...")
        while True:
            image_data = fileToSend.read(4096)
            while (image_data):
                client1.send(image_data)
                image_data = fileToSend.read(4096)
            if not image_data:
                fileToSend.close() 
                break
        
#we add commands here
def commands(message1, client):
    name_of_client = namelookup(client)
    crypterX = client_to_crypter(client)
    print("message1:",message1)
    if "/chatmember" in str(message1):
        chat_member(client)
    elif "/disconnect" in str(message1):
        client.send("Exit".encode())
        #client.close()
        # We need to make sure client is deleted off our lists
    elif "/help" in str(message1):
        helps(client, name_of_client)
    elif "/kick" in str(message1) and admincheck(name_of_client):
        kick(message1, client)
    elif "/ban" in str(message1) and admincheck(name_of_client):
        bans(message1, client)
    elif "/admin" in str(message1):
        New_admin(client, name_of_client)
    elif "/sendfile" in str(message1):
        sendfile(client)
    else:
        client.send(crypterX.encrypt_string("Command Not Found, Use /help to Check for Command\n"))
        #client.send("Command Not Found, Use /help to Check for Command\n".encode())

# Ready to receieve connection
print("Server open for connection")
receive()