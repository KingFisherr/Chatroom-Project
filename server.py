import socket
import threading
from crypter import AESCrypter

host = "127.0.0.1"
port = 1338


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))

# Start listening
server.listen()

clients = [] # or sockets
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

        print(f"Client's username is {username}")
        
        # Call broadcast func to send a message to all clients
        # message will notify all clients of a newly joined client
        broadcast(f'{username} has joined the server'.encode())
        clientconn.send("You are now connected to the live chat server".encode())

        #Multiple client

        thread = threading.Thread(target=handler, args=(clientconn,))
        thread.start()

# Need function to send message to all clients
def broadcast(messsage):
    for x in clients:
        x.send(messsage)

# Need function to handle messages from clients

def handler(client):

    while True:
        try:
            message = client.recv(1024)

            broadcast(message)
        except:
            # Broadcast the user has disconnected
            index = clients.index(client)
            username = username_list[index]
            broadcast(f'{username} has left the chat'.encode())

            # Disconnect client from server and remove from list
            clients.remove(client)
            client.close()
            username_list.remove(username)
            break

# Need additional non core administrative functions or similiar

print ("Server open for connection")
receive()
# ready to receieve connection 