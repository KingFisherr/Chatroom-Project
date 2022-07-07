import socket
import threading
import json
from crypter import AESCrypter

# Username for current client
username = input("Choose live chat username: ")

# Password for current clietn
password = input(f"Enter password for {username}: ")

# Create tuple to store user and password in one struct
user_pass_json = (username, password)
user_pass_json = json.dumps(user_pass_json)

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
                clientsocket.send(user_pass_json.encode())
                second_data = clientsocket.recv(1024).decode()
                if second_data == "Banned":
                    print('You are banned from this server. Please contact Admin.')
                    clientsocket.close()
                    thread_stopped = True   
                elif second_data == "Wrongpass":
                    print("Wrong password, try again")
                    clientsocket.close()
                    thread_stopped = True                  
            else:
                print(data)
            
        except:
            print ("Error connecting to server")
            clientsocket.close()
            break

# Function to send messages to server
def chat():
    while True:
        if thread_stopped:
            break
        user_message = f'{username}: {input("")}'

        # If username == admin we will do special cases for messages (i.e. kick or ban or promote etc)

        # Implement function or add on to this function for file transfer functionality

        clientsocket.send(user_message.encode())


# recieve()
# chat()


thread_recieve = threading.Thread(target=recieve)
thread_recieve.start()
thread_chat = threading.Thread(target=chat)
thread_chat.start()