import socket
import threading
import time
host = "127.0.0.1"
port = 1338


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))

# Start listening
server.listen()

clients = [] # or sockets
username_list = []



# function to send message to all clients   # moved this to front to aviod design error
def broadcast(temps):
    for x in clients:
        x.send(temps.encode())
        time.sleep(0.5)


# Need function to receieve connection from client
def receive():
    while True:
        clientconn, address = server.accept()
        print (f"Connection to {address} established...")

        #Ask client for username
        clientconn.send("Username".encode())

        # Username var stores the username received from client
        print("receiving1")
        username = clientconn.recv(1024).decode()

        # Maybe check ban database here 

        # Maybe also check username/password database and implement a login system (admin will have different login)

        # Update client list and username list with new client
        clients.append (clientconn)
        username_list.append(username)

        print(f"Client's username is {username}")
         
        # Call broadcast func to send a message to all clients
        # message will notify all clients of a newly joined client

        clientconn.send("You are now connected to the live chat server".encode())
        while True:
            clientconn.send("Start".encode())#ask for message
            print("receiving2")
            another = clientconn.recv(1024).decode()
            if another == "Message":
                print("receiving3")
                fulltxt = clientconn.recv(1024).decode()
                broadcast(fulltxt)
        
        #Multiple client

        #thread = threading.Thread(target= )





# Need function to handle messages from clients
#def handler():
    
# Need additional non core administrative functions or similiar

print ("Server open for connection")
receive()
print ("it is me mario")
#messagehandler()
# ready to receieve connection 
