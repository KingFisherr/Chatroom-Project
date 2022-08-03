import os
import json
import socket
import time
import getpass
import threading
import tkinter
from playsound import playsound #pip install playsound==1.2.2
#from Tkinter import 
import tkinter as tk
from tkinter import scrolledtext
from tkinter import simpledialog
from crypter import AESCrypter
from base64 import b64encode, b64decode
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox


HOST = "127.0.0.1"
PORT = 1400

class Client:
    def __init__(self, host, port):

        # Connect to server
        self.clientsocket = None

        while True:
            try:
                # print(host, " : ", port)
                self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.clientsocket.connect((host, port))  # Host/port
                break
            except Exception as e:
                print("failed to connect to server ec {}".format(e))
                time.sleep(1)
                print("trying again..")

        # Create window for login
        msgbox = tkinter.Tk()
        msgbox.withdraw()

        #Create login elements
        self.username = simpledialog.askstring("Username", "Please enter nickname: ", parent=msgbox)
        self.password = simpledialog.askstring("Password", "Enter password",show="*", parent=msgbox)

        # Store username and password in json var
        self.user_pass_json = (self.username, self.password)
        self.user_pass_json = json.dumps(self.user_pass_json)

        self.crypter = AESCrypter()

        # Set GUI_DONE to false and GUI_RUNNING to true
        self.gui_done = False
        self.gui_running = True

        #gui_thread = threading.Thread(target=self.gui_loop)
        thread_receive = threading.Thread(target=self.receive)
        # thread_chat = threading.Thread(target= self.chat)

        #gui_thread.start()
        #time.sleep(1)
        thread_receive.start()
        # thread_chat.start()
        # when gui loop runs on its own thread SIGSEGV signals are emitted...
        self.gui_loop()

    # Create chat GUI window for client 
    # Needs to look nicer
    # Button for sending file
    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="#4682B4")

        self.chat_label = tkinter.Label(self.win, text="Chat:", fg="white", bg="#4682B4")
        self.chat_label.config(font=("Calibri,12"))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.config(state='disabled')
        self.text_area.pack(padx=20, pady=5)

        self.message_label = tkinter.Label(self.win, text="Message:", fg="white", bg="#4682B4")
        self.message_label.config(font=("Calibri,12"))
        self.message_label.pack(padx=20, pady=5)

        self.message_box = tkinter.Text(self.win, height=3)
        self.message_box.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", bg="#4682B4", borderwidth=3, relief="sunken", activebackground="#4682B4", activeforeground="Orange", command=self.chat)
        self.send_button.config(font=("Calibri,12"))
        #self.send_button.pack(padx=20, pady=5)
        self.send_button.pack()

        self.gui_done = True

        # When window is closed we call end function
        self.win.protocol("WM_DELETE_WINDOW", self.end)

        # Binds return button to func
        self.win.bind('<Return>',lambda event:self.chat())
        self.win.mainloop()

    def receive(self):
        while self.gui_running:
            try:
                # Get data from server
                data = self.clientsocket.recv(2048).decode()

                #print("RAW DATA {}".format(data))
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

                # exit Gui if receive exit
                elif data == "Exit":
                    self.clientsocket.close()
                    self.gui_done = True
                    self.end()
                    thread_stopped = True

                elif data == "SendImage":
                    # open image (somehow need to get file name)
                    file = open('animage.jpg', 'rb')
                    file.seek(0, os.SEEK_END)
                    file_size = file.tell()
                    self.clientsocket.send(str(file_size).encode())
                    print("Size of file is :", file.tell(),"bytes")
                    file.seek(0,0)
                    while True:
                        image_data = file.read(4096)
                        while (image_data):
                            self.clientsocket.send(image_data)
                            image_data = file.read(4096)
                        if not image_data:
                            file.close()
                            break

                elif data == "RecvImage":
                    # open file to read image into
                    file = open('gotit.jpg', 'wb')
                    image_data = self.clientsocket.recv(2048)
                    while image_data:
                        file.write(image_data)
                        image_data = self.clientsocket.recv(2048)
                    file.close()
                
                # if pinged, then the computer will play sound and notify the client
                elif data == "Pinged":
                    sound = "ping.mp3"
                    playsound(sound)

                elif data == "IV":
                    send_iv = b64decode(self.clientsocket.recv(24).decode())
                    recv_iv = b64decode(self.clientsocket.recv(24).decode())
                    # print(send_iv)
                    # print(recv_iv)
                    self.crypter.init_cipher(send_iv, recv_iv)
                    # print("iv has been initialized")

                elif data == "":
                    raise Exception("received empty string, server probably disconnected")

                else:
                    if self.gui_running:
                        if self.crypter.initialized():
                            data = self.crypter.decrypt_string(data)
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', data)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')

            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
                print("Error connecting to server")
                self.clientsocket.close()
                break


    def chat(self, _event=None):
        message = f"{self.username}: {self.message_box.get('1.0', 'end')}"
        emsg = self.crypter.encrypt_string(message)
        self.clientsocket.send(emsg)
        self.message_box.delete('1.0', 'end')
        # If we detect user is sending a file we can update a global var with file name


    # Stop GUI and close client socket
    def end(self):
        self.clientsocket.close()
        self.gui_running = False
        self.win.destroy()
        # self.clientsocket.close()
        exit(0)


# Initialize client object
client = Client(HOST, PORT)
