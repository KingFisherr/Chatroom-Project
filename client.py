import json
import socket
import stdiomask
import getpass
import threading
from crypter import AESCrypter
from base64 import b64encode, b64decode

# Username for current client
username = input("Choose live chat username: ")

# Password for current client
#password = getpass.getpass(f"Enter password for {username}: ")
password = stdiomask.getpass(f"Enter password for {username}: ")
#password = input(f"Enter password for {username}: ")

# Create tuple to store user and password in one struct
user_pass_json = (username, password)
user_pass_json = json.dumps(user_pass_json)

# Create a global crypter object
crypter = AESCrypter()

# Setup client socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to host server
clientsocket.connect(("127.0.0.1", 1338)) #Host/port

thread_stopped = False

# Function to recieve data from server
def recieve():
    while True:    
        try:
            # Get data from server
            data = clientsocket.recv(1024).decode()
            # print("RAW DATA {}".format(data))
            # Send username and password to server
            if data == "Username":
                # Get response from server
                clientsocket.send(user_pass_json.encode())
            # If Banned message received we will close client connection to server
            elif data == "Banned":
                print('You are banned from this server. Please contact Admin.')
                clientsocket.close()
                thread_stopped = True
            # If wrongpass message received we will close client connnection to server
            elif data == "Wrongpass":
                print("Wrong password, try again")
                clientsocket.close()
                thread_stopped = True
            elif data == "IV":
                send_iv = b64decode(clientsocket.recv(24).decode())
                recv_iv = b64decode(clientsocket.recv(24).decode())
                crypter.init_cipher(send_iv, recv_iv)   
                # print("iv has been initialized")
            elif data == "":
                raise Exception("received empty string, server probably disconnected")
            else:
                if(crypter.initialized()):
                    dmesg = crypter.decrypt_string(data)
                    print(dmesg.decode())
                else:
                    print("received message before crpter initialization : {}".format(data))
            
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
        emsg = crypter.encrypt_string(user_message)

        #clientsocket.send(b64decode(dmsg).decode())
        clientsocket.send(emsg)


# recieve()
# chat()


thread_recieve = threading.Thread(target=recieve)
thread_recieve.start()
thread_chat = threading.Thread(target=chat)
thread_chat.start()