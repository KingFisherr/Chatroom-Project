import json
import socket
import threading
from crypter import AESCrypter
from base64 import b64encode, b64decode
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

# Username for current client
username = input("Choose live chat username: ")

# Password for current clietn
password = input(f"Enter password for {username}: ")

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

            print("RAW DATA {}".format(data))
            if data == "Username":
                clientsocket.send(user_pass_json.encode())
            elif data == "Banned":
                print('You are banned from this server. Please contact Admin.')
                clientsocket.close()
                thread_stopped = True
            elif data == "Wrongpass":
                print("Wrong password, try again")
                clientsocket.close()
                thread_stopped = True
            elif data == "IV":
                send_iv = b64decode(clientsocket.recv(24).decode())
                recv_iv = b64decode(clientsocket.recv(24).decode())
                # print(send_iv)
                # print(recv_iv)
                crypter.init_cipher(send_iv, recv_iv)   
                print("iv has been initialized")
            elif data == "":
                raise Exception("received empty string, server probably disconnected")

            else:
                # if gui_running:
                #     self.text_area.config(state = 'normal') 
                #     self.text_area.insert('end', message)
                #     self.text_area.yview('end')
                #     self.text_area.config(state = 'disabled')
                #print("crypter initialized {}".format(crypter.initialized()))
                if(crypter.initialized()):
                    dmesg = crypter.decrypt_string(data)
                    print(dmesg)
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

        #user_message = f"{username}: {self.input_area.get('1.0', 'end')}"
        # If username == admin we will do special cases for messages (i.e. kick or ban or promote etc)

        # Implement function or add on to this function for file transfer functionality
        emsg = crypter.encrypt_string(user_message)

        #clientsocket.send(b64decode(dmsg).decode())
        clientsocket.send(emsg)

        #self.input_area.delete('1.0', 'end')

# def gui_loop():
#     win = tkinter.Tk()
#     win.configure(bg = "lightgray")

#     chat_label = tkinter.Label(win, text="Chat:", bg = "lightgray")
#     chat_label.config(font=("Calibri,12"))
#     chat_label.pack(padx=20, pady= 5)

#     text_area = tkinter.scrolledtext.ScrolledText(win)
#     text_area.config(state = 'disabled')
#     text_area.pack(padx=20, pady= 5)

#     message_label = tkinter.Label(win, text="Message:", bg = "lightgray")
#     message_label.config(font=("Calibri,12"))
#     message_label.pack(padx=20, pady= 5)

#     input_area = tkinter.Text(win, height= 3)
#     input_area.pack(padx=20, pady= 4)
    
#     send_button = tkinter.Button(win, text= "Send", command= chat)
#     send_button.config(font=("Calibri,12"))
#     send_button.pack(padx=20, pady= 5)

#     gui_done = True

#     win.protocol("WM_DELETE_WINDOW", stopp)

#     win.mainloop()
# def stopp(self):
#     self.gui_running = False
#     self.win.destroy()
#     self.clientsocket.close()
#     exit(0)

# box = tkinter.Tk()
# box.withdraw()
# box_nickname = simpledialog.askstring("Nickname","Please enter nickname: ", parent = box)

# # gui_done = False

# # gui_running = True

# gui_thread = threading.Thread(target = gui_loop)
# gui_thread.start()


# # Start thread recieve function and then chat function
# thread_recieve = threading.Thread(target=recieve)
# thread_recieve.start()
# thread_chat = threading.Thread(target=chat)
# thread_chat.start()

# gui_thread = threading.Thread(target = gui_loop)
# gui_thread.start()


# Start thread recieve function and then chat function
thread_recieve = threading.Thread(target=recieve)
thread_recieve.start()
thread_chat = threading.Thread(target=chat)
thread_chat.start()