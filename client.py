import socket
import threading 

# Username for current client
username = input("Choose live chat username: ")

# Setup client socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to host server
clientsocket.connect((socket.gethostname(), 1337)) #Host/port

# Function to recieve data from server
def recieve():
    data = clientsocket.recv(1338)
    print (data)

# Function to send messages to server
def chat():
    d

thread_recieve = threading.Thread(target=recieve)
thread_recieve.start()
thread_chat = threading.Thread(target=chat)
thread_chat.start()