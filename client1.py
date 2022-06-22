import socket
import threading 

# Username for current client
username = input("Choose live chat username: ")

# Setup client socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to host server
clientsocket.connect(("127.0.0.1", 1338)) #Host/port

#client chatroom status
connect_status = False

# Function to recieve data from server
def recieve():
    while True:    
        try:
            data = clientsocket.recv(1024).decode()
            if data == "Username":
                clientsocket.send(username.encode())
                second_data = clientsocket.recv(1024).decode()
                print(second_data)
            elif data == "Connected": #check if the chatroom is connected, if connected, then enter chat function.
                connect_status = True
            elif data == "Disconnected":
                connect_status = False
            elif data == "Message":
                mess = clientsocket.recv(1024).decode()
                print(mess)
            else:
                print(data)
        except:
            print ("Encountered some error")
            clientsocket.close()
            break

# Function to send messages to server
def chat():
        clientsocket.send("Message".encode())
        text = f'{username}: {input("")}'
        clientsocket.send(text.encode())
        
                        
            

recieve()

# Message for current client after connected into chatroom
while connect_status == True:
    txtdata = input("Your Message: ")
    chat()

#thread_recieve = threading.Thread(target=recieve)
#thread_recieve.start()
# thread_chat = threading.Thread(target=chat)
# thread_chat.start()
