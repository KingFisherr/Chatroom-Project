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

# Need function to send message to all clients

# Need function to handle messages from clients

# Need function to receieve connection from client
while True:
    clientconn, address = s.accept()
    print (f"Connection to {address} established...")
    with clientconn:
        clientconn.send(b"You have been connected to server!")

        
# Need additional non core administrative functions or similiar

#print ("Server open for connection...")
# ready to receieve connection 