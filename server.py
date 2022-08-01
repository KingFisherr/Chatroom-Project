import json
import time
import socket
import bcrypt
import threading
from crypter import AESCrypter
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
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

# List of crypters
crypters = []

# Need function to receieve connection from client
def receive():
    while True:
        clientconn, address = server.accept()
        print (f"Connection to {address} established...")

        #Ask client for username
        clientconn.send("Username".encode())

        # user_pass_json var stores the username and password received from client as json
        user_pass_json = clientconn.recv(1024).decode()
        user_pass_json = json.loads(user_pass_json)

        username = user_pass_json[0]
        password = user_pass_json[1]
        
        #cheking if DB exists before trying to store
        db.checkfordb('ban_database.sqlite')
        

        # Check for ban database
        db.checkfordb('ban_database.sqlite')
        # Check if client is banned
        if db.checkban(username):
            # If client is on ban list send them ban message
            clientconn.send("Banned".encode())
            # Disconnect client from server
            clientconn.close()
            continue
                   
        #init crypter
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
  
        # Check if username exists
        db.checkfordb('user_database.sqlite')
        if db.checkUsername(username): 
            print ("Username exists")
            # If username exists then verify login
            if not db.checkloginHash(username, password):
                print("Password does not match")
                # We want to disconnect client so they retry password
                clientconn.send("Wrongpass".encode())
                clientconn.close()
                continue
        else:
            print ("stored user info")
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(13))
            #cheking if DB exists before trying to store
            db.checkfordb('user_database.sqlite')
            db.storeuserinfo(username, hashed.decode())
            

        # Update client list and username list with new client
        crypters.append(crypter)
        clients.append(clientconn)
        username_list.append(username)

        print(f"{username} is joining the server")
        
        # Call broadcast func to send a message to all clients
        broadcast(f"{username} has joined the server", clientconn)
        
        # Let client know they are now connected to the chat server
        # broadcast(f"You are now connected to the live chat server", clientconn)
        # clientconn.send("You are now connected to the live chat server".encode())
        cstr = crypter.encrypt_string("You are now connected to the live chat server")
        clientconn.send(cstr)
        
        # Handle multiple clients
        thread = threading.Thread(target=handler, args=(clientconn,))
        thread.start()

def client_to_crypter(client):
    # get the index of the target client
    index = clients.index(client)
    # get the crypter of the target client
    return crypters[index]

# Function sends message to all connected clients
def broadcast(message, client):
    print(f"broadcasting {message}")
    for x in clients:
        # skip the sender
        if x == client:
            continue
            
        try:
            crypter = client_to_crypter(x)
            # encrypt the message to send
            emsg = crypter.encrypt_string(message)
            # ( ( ( hacky sleep cuz no size header ) ) )
            time.sleep(0.5)
            # send the message to the target clientss
            x.send(emsg)
        except Exception as ex:
            print(ex)

# Functions handles messages sent to server by clients
def handler(client):
    
    crypter = client_to_crypter(client)
    
    while True:
        try:
            # Get message from client
            message = client.recv(1024)
            
            if(message == b""):
                raise Exception("exception: received empty string") 
            
            # print("RECEIVED RAW {}".format(message))
            dmsg = crypter.decrypt_string(message)
            
            print("received {}".format(dmsg.decode()))
            
            # Broadcast message to all clients
            broadcast(dmsg.decode(), client)
            
            # Implement function or add on to this function for file transfer functionality
            
        except Exception as ex:
            print(ex)
            # Broadcast the user has disconnected
            index = clients.index(client)
            username = username_list[index]
            broadcast(f'{username} has left the chat', client)
            
            # not thread safe, data race
            # Disconnect client from server and remove from list
            crypters.remove(crypter)
            username_list.remove(username)
            clients.remove(client)
            client.close()
            break

# Need additional non core administrative functions or similiar

# Ready to receieve connection 
print ("Server open for connection")
receive()
