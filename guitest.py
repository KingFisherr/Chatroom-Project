import json
import socket
import threading
#from crypter import AESCrypter
#from base64 import b64encode, b64decode
from tkinter import *
import tkinter.scrolledtext
from tkinter import simpledialog


HOST = "127.0.0.1"
PORT = 1338

class Client:
    def __init__(self, host, port):

        # Connect to server
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clientsocket.connect((host, port)) #Host/port

        # Create window for login
        msgbox = tkinter.Tk()
        msgbox.withdraw()

        # Create login elements
        self.username = simpledialog.askstring("Username","Please enter nickname: ", parent = msgbox)
        self.password = simpledialog.askstring("Password", "Enter password", parent = msgbox)

        # Store username and password in json var
        self.user_pass_json = (self.username,self.password)
        self.user_pass_json = json.dumps(self.user_pass_json)

        # Set GUI_DONE to false and GUI_RUNNING to true
        self.gui_done = False
        self.gui_running = True

        gui_thread = threading.Thread(target = self.gui_loop)
        thread_recieve = threading.Thread(target= self.receive)
        #thread_chat = threading.Thread(target= self.chat)


        gui_thread.start()
        thread_recieve.start()
        #thread_chat.start()

    # Create chat GUI window for client 
        # Needs to look nicer
        # Button for sending file
    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg = "lightgray")

        self.chat_label = tkinter.Label(self.win, text="Chat:", bg = "lightgray")
        self.chat_label.config(font=("Calibri,12"))
        self.chat_label.pack(padx=20, pady= 5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.config(state = 'disabled')
        self.text_area.pack(padx=20, pady= 5)

        self.message_label = tkinter.Label(self.win, text="Message:", bg = "lightgray")
        self.message_label.config(font=("Calibri,12"))
        self.message_label.pack(padx=20, pady= 5)

        self.message_box = tkinter.Text(self.win, height= 3)
        self.message_box.pack(padx=20, pady= 5)
        
        self.send_button = tkinter.Button(self.win, text= "Send", command = self.chat)
        self.send_button.config(font=("Calibri,12"))
        self.send_button.pack(padx=20, pady= 5)

        self.gui_done = True


        # When window is closed we call end function
        self.win.protocol("WM_DELETE_WINDOW", self.end)

        # Binds return button to func
        #self.win.bind('<Return>', self.chat)

        self.win.mainloop()
    
    def receive(self):
        while self.gui_running:
            try:
                # Get data from server
                data = self.clientsocket.recv(1024).decode()

                print("RAW DATA {}".format(data))
                if data == "Username":
                    self.clientsocket.send(self.user_pass_json.encode())

                # If banned let client know, disconnect and end gui window
                elif data == "Banned":
                    print('You are banned from this server. Please contact Admin.')
                    self.clientsocket.close()
                    self.gui_done = True
                    self.end()
                    thread_stopped = True

                # If wrong pass let client know, disconnect and end gui window
                elif data == "Wrongpass":
                    print("Wrong password, try again")
                    self.clientsocket.close()
                    self.gui_done = True
                    self.end()
                    thread_stopped = True
                    
                elif data == "Duplicate":
                    print("User is already logged in")
                    self.clientsocket.close()
                    self.gui_done = True
                    self.end()
                    thread_stopped = True

                # elif data == "IV":
                #     send_iv = b64decode(clientsocket.recv(24).decode())
                #     recv_iv = b64decode(clientsocket.recv(24).decode())
                #     # print(send_iv)
                #     # print(recv_iv)
                #     crypter.init_cipher(send_iv, recv_iv)   
                #     print("iv has been initialized")
                # elif data == "":
                #     raise Exception("received empty string, server probably disconnected")

                else:
                    if self.gui_running:
                        self.text_area.config(state = 'normal') 
                        self.text_area.insert('end', data)
                        self.text_area.yview('end')
                        self.text_area.config(state = 'disabled')
                    #print("crypter initialized {}".format(crypter.initialized()))
                    # if(crypter.initialized()):
                    #     dmesg = crypter.decrypt_string(data)
                    #     print(dmesg)
                    # else:
                    #     print("received message before crpter initialization : {}".format(data))
            
            except:
                print ("Error connecting to server")
                self.clientsocket.close()
                break
    
    def chat(self, _event=None):     
        message = f"{self.username}: {self.message_box.get('1.0', 'end')}"
        self.clientsocket.send(message.encode())
        self.message_box.delete('1.0', 'end')          


    # Stop GUI and close client socket
    def end(self):
        self.clientsocket.close()
        self.gui_running = False
        self.win.destroy()
        #self.clientsocket.close()
        exit(0)

    
# Initialize client object
client = Client(HOST, PORT)