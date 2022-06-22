import socket
import threading
import time

# Username for current client
username = input("Choose live chat username: ")

# Setup client socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to host server
clientsocket.connect(("127.0.0.1", 1338)) #Host/port






# Message for current client after connected into chatroom
def messhandler():
        txtdata = input("Your Message: ")
        text = f'{username}: {txtdata}'
        clientsocket.send("Message".encode())
        time.sleep(0.5)
        clientsocket.send(text.encode())
        
# Function to recieve data from server
def recieve():
    while True:    
        try:
            data = clientsocket.recv(1024).decode()
            if data == "Username":
                clientsocket.send(username.encode())
                #second_data = clientsocket.recv(1024).decode()
                #print(second_data)

                ##after account username and password are done
            elif data == "Start":
                messhandler()
            else:
                print(data)
        except:
            print ("Encountered some error")
            clientsocket.close()
            break



        
                        
            

recieve()
print("what up")


#thread_recieve = threading.Thread(target=recieve)
#thread_recieve.start()
# thread_chat = threading.Thread(target=chat)
# thread_chat.start()
