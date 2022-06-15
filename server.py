import socket
import threading

host = socket.gethostbyname()
port = 1338


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket.bind((host, port))

# Start listening
socket.listen()

clients = [] # or sockets
nicknames_list = []

# Need function to receieve connection from client
def receive():
    while True:
        clientconn, address = server.accept()
        print (f"Connection to {address} established...")


# Need function to send message to all clients
def broadcast(messsage):
    for x in clients:
        x.send(messsage)

# Need function to handle messages from clients
def handler():
    
# Need additional non core administrative functions or similiar

# print ("Server open for connection...")
# ready to receieve connection 