from email import message
import socket
import threading
from crypter import AESCrypter

# Username for current client
username = input("Choose live chat username: ")

# Setup client socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to host server
clientsocket.connect(("127.0.0.1", 1338)) #Host/port

thread_stopped = False

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
def chat():
    while True:
        if thread_stopped:
            break
        user_message = f'{username}: {input("")}'
        # Problem might be that it gets broadcasted everywhere including to client who sent message (broadcasr everyone except client who sent the message)
        #If username == admin we will do special cases for messages (i.e. kick or ban or promote etc)

        clientsocket.send(user_message.encode())


# recieve()
# chat()


thread_recieve = threading.Thread(target=recieve)
thread_recieve.start()
thread_chat = threading.Thread(target=chat)
thread_chat.start()