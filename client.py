import socket
import threading
from crypter import AESCrypter

# Username for current client
username = input("Choose live chat username: ")

# Setup client socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to host server
clientsocket.connect(("127.0.0.1", 1338)) #Host/port

# Function to recieve data from server
def recieve():
    while True:    
        try:
            data = clientsocket.recv(1024).decode()
            if data == "Username":
                clientsocket.send(username.encode())
                second_data = clientsocket.recv(1024).decode()
                print(second_data)
            else:
                print(data)
        except:
            print ("Encountered some error")
            clientsocket.close()
            break

# Function to send messages to server
#def chat():
    #d

recieve()
#thread_recieve = threading.Thread(target=recieve)
#thread_recieve.start()
# thread_chat = threading.Thread(target=chat)
# thread_chat.start()