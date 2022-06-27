import socket
import threading
from crypter import AESCrypter
from dbmodels import database

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

# Need function to receieve connection from client
def receive():
    while True:
        clientconn, address = server.accept()
        print (f"Connection to {address} established...")

        #Ask client for username
        clientconn.send("Username".encode())

        # Username var stores the username received from client
        username = clientconn.recv(1024).decode()

        # Maybe check ban database here 

        # Maybe also check username/password database and implement a login system (admin will have different login)

        # Update client list and username list with new client
        clients.append (clientconn)
        username_list.append(username)

        print(f"{username} is joining the server")
        
        # Call broadcast func to send a message to all clients
        broadcast(f'{username} has joined the server'.encode(), clientconn)

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

# Functions handles messages sent to server by clients
def handler(client):

    while True:
        try:
            # Get message from client
            message = client.recv(1024)

            # Broadcast message to all clients
            broadcast(message, client)
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
