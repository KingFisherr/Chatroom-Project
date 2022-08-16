import os
import json
import socket
import time
import threading
import settings
from gui import App
from crypter import AESCrypter
from PIL import Image
from base64 import b64encode, b64decode
from playsound import playsound #pip install playsound==1.2.2

HOST = "127.0.0.1"
PORT = 1400


settings.init()

# file_name = ""
# last_file = ""


class Client:
    def __init__(self, host, port):

        # Connect to server
        self.clientsocket = None
        self.crypter = AESCrypter()
        self.app = App(self)
        self.host = host
        self.port = port
        self.app.mainloop()

    def connect_to_server(self, username, password):
        while True:
            try:
                # print(host, " : ", port)
                self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.clientsocket.connect((self.host, self.port))  # Host/port
                break
            except Exception as e:
                print("failed to connect to server ec {}".format(e))
                time.sleep(1)
                print("trying again..")

        # Store username and password in json var
        self.user_pass_json = (username, password)
        self.user_pass_json = json.dumps(self.user_pass_json)

        thread_receive = threading.Thread(target=self.receive)
        thread_receive.start()
        # thread_recv_file = threading.Thread(target=self.recv_file)
        # thread_recv_file.start() 

    def send_message(self, message, encrypt=True):
        emsg = message
        if encrypt:
            emsg = self.crypter.encrypt_string(message)
        # data_dict = {"Message": emsg} # MAYBE WE MAKE DICT HERE (yes pls)
        self.clientsocket.send(emsg)

    def receive(self):
        while self.app.gui_running:
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
                    self.app.gui_done = True
                    self.end()
                    thread_stopped = True

                # If wrong pass let client know, disconnect and end gui window
                elif data == "Wrongpass":
                    print("Wrong password, try again")
                    self.clientsocket.close()
                    self.app.gui_done = True
                    self.end()
                    thread_stopped = True

                elif data == "Duplicate":
                    print("User is already logged in")
                    self.clientsocket.close()
                    self.app.gui_done = True
                    self.end()
                    thread_stopped = True

                # exit Gui if receive exit
                elif data == "Exit":
                    self.clientsocket.close()
                    self.app.gui_done = True
                    self.end()
                    thread_stopped = True

                elif data == "SendImage":
                    file = open(settings.file_name, 'rb')
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
                            print ("FILE COMPLETELY SENT")
                            break

                elif data == "RecvImage":
                    #Start getting file via on a thread
                    # thread_recv_file = threading.Thread(target=self.recv_file)
                    # thread_recv_file.start()                   

                    # WE tell server we are ready to get file
                    self.clientsocket.send("READYTORECV".encode())
                    remaining = self.clientsocket.recv(1024).decode()
                    print (f"REMAINING IS: {remaining}")
                    print (f"REMAINING IS: {self.crypter.decrypt_string(remaining)}")
                    if type(remaining) == int: 
                        print (f"REMAINING IS: {self.crypter.decrypt_string(remaining)}")
                        remaining = int(remaining)
                        #remaining = 206993
                        #print (remaining) REMAINING IS: LPwrNp0I3GwJWRtxYesCqZ+qrh0vgFGieEpZ
                        with open('endloc.jpg','wb') as file:
                            while remaining:
                                image_data = self.clientsocket.recv(min(4096,remaining))
                                remaining -= len(image_data)
                                file.write(image_data)                    
                            file.close()
                        print (f"{file.name} ALL RECV")
                        # Display image in new tkinter window
                        path = os.path.abspath(file.name)
                        print (path)
                        im = Image.open(path)

                        im.show()                    

                    # window = GUI()
                    # image_gui_thread = threading.Thread(target = window.createImageWindow, args= (file.name,))
                    # image_gui_thread.start()
                    #window.createImageWindow(file.name)

                elif data == "IV":
                    send_iv = b64decode(self.clientsocket.recv(24).decode())
                    recv_iv = b64decode(self.clientsocket.recv(24).decode())
                    # print(send_iv)
                    # print(recv_iv)
                    self.crypter.init_cipher(send_iv, recv_iv)
                    # print("iv has been initialized")

                # if pinged, then the computer will play sound and notify the client
                elif data == "Pinged":
                    sound = "ping.mp3"
                    playsound(sound)

                elif data == "":
                    raise Exception("received empty string, server probably disconnected")

                else:
                    if self.app.gui_running:
                        if self.crypter.initialized():
                            data = self.crypter.decrypt_string(data)
                        self.app.chat_frame.recv_message(data)

            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
                print("Error connecting to server")
                self.clientsocket.close()
                break

    # Stop GUI and close client socket
    def end(self):
        self.clientsocket.close()
        self.app.gui_running = False
        self.app.destroy()
        exit(0)

    # def recv_file(self):
    #     data = self.clientsocket.recv(2048).decode()
    #     if data == "RECVXX":
    #         self.clientsocket.send("READYTORECV".encode())
    #         remaining = self.clientsocket.recv(1024).decode()
    #         print (f"REMAINING IS: {self.crypter.decrypt_string(remaining)}")
    #         if type(remaining) == int: 
    #             remaining = int(remaining)
    #             #remaining = 206993
    #             #print (remaining) REMAINING IS: LPwrNp0I3GwJWRtxYesCqZ+qrh0vgFGieEpZ
    #             with open('endloc.jpg','wb') as file:
    #                 while remaining:
    #                     image_data = self.clientsocket.recv(min(4096,remaining))
    #                     remaining -= len(image_data)
    #                     file.write(image_data)                    
    #                 file.close()
    #             print (f"{file.name} ALL RECV")
    #             # Display image in new tkinter window
    #             path = os.path.abspath(file.name)
    #             print (path)
    #             im = Image.open(path)

    #         im.show()   

# Initialize client object
client = Client(HOST, PORT)
