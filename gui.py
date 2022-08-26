import json
import settings
from pathlib import Path
from tkinter import filedialog, Tk, Canvas, Entry, messagebox, Button, PhotoImage, Frame, Label
from tkinter import scrolledtext
from crypter import AESCrypter
import tkinter

settings.init()

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    print(ASSETS_PATH / Path(path))
    return ASSETS_PATH / Path(path)

class App(Tk):
    def __init__(self, client):
        Tk.__init__(self)
        self.title("Chatroom App")
        self.geometry("1012x506") 
        self.client = client;
        self.gui_done = False
        self.gui_running = True
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.login_frame = Login(parent=self.container, controller=self)
        self.chat_frame = ChatBox(self.container, self)
        self.login_frame.tkraise()
        #self.chat_frame.tkraise()

class Login(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.connecting = False
        self.configure(bg="#5E95FF")
        self.grid(row=0, column=0, sticky="nsew")

        self.canvas = Canvas(
            self,
            bg="#5E95FF",
            height=506,
            width=1012,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(
            469.0, 0.0, 1012.0, 506.0, fill="#FFFFFF", outline=""
        )

        self.entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        entry_bg_1 = self.canvas.create_image(736.0, 331.0, image=self.entry_image_1)
        entry_1 = Entry(self.canvas, bd=0, bg="#EFEFEF", highlightthickness=0)
        entry_1.place(x=568.0, y=294.0, width=336.0, height=0)

        self.entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        entry_bg_2 = self.canvas.create_image(736.0, 229.0, image=self.entry_image_2)
        entry_2 = Entry(self.canvas, bd=0, bg="#EFEFEF", highlightthickness=0)
        entry_2.place(x=568.0, y=192.0, width=336.0, height=0)

        self.canvas.create_text(
            573.0,
            306.0,
            anchor="nw",
            text="Password",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.canvas.create_text(
            573.0,
            204.0,
            anchor="nw",
            text="Username",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.canvas.create_text(
            553.0,
            66.0,
            anchor="nw",
            text="Enter your login details",
            fill="#5E95FF",
            font=("Montserrat Bold", 26 * -1),
        )

        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.validateLogin,
            relief="flat",
        )
        button_1.place(x=641.0, y=412.0, width=190.0, height=48.0)

        self.canvas.create_text(
            85.0,
            66.0,
            anchor="nw",
            text="LiveChat",
            fill="#FFFFFF",
            font=("Montserrat Bold", 50 * -1),
        )

        self.canvas.create_text(
            553.0,
            109.0,
            anchor="nw",
            text="Enter the credentials that the admin gave",
            fill="#CCCCCC",
            font=("Montserrat Bold", 16 * -1),
        )

        self.canvas.create_text(
            553.0,
            130.0,
            anchor="nw",
            text="you while signing up for the program",
            fill="#CCCCCC",
            font=("Montserrat Bold", 16 * -1),
        )

        self.entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
        entry_bg_3 = self.canvas.create_image(736.0, 241.0, image=self.entry_image_3)
        self.username = Entry(
            self.canvas,
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
            font=("Montserrat Bold", 16 * -1),
            foreground="#777777",
        )
        self.username.place(x=573.0, y=229.0, width=326.0, height=22.0)

        self.entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
        entry_bg_4 = self.canvas.create_image(736.0, 342.0, image=self.entry_image_4)
        self.password = Entry(
            self.canvas,
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
            font=("Montserrat Bold", 16 * -1),
            foreground="#777777",
            show="•",
        )
        self.password.place(x=573.0, y=330.0, width=326.0, height=22.0)

        self.canvas.create_text(
            90.0,
            431.0,
            anchor="nw",
            text="© 2022",
            fill="#FFFFFF",
            font=("Montserrat Bold", 18 * -1),
        )

        self.image_image_1 = PhotoImage(file=relative_to_assets("image_3.png"))
        self.image_image_1 = self.image_image_1.subsample(2)
        self.image_1 = self.canvas.create_image(440.0, 230.0, image=self.image_image_1)

        self.canvas.create_text(
            90.0,
            150.0,
            anchor="nw",
            text="Is an instant messaging",
            fill="#FFFFFF",
            font=("Montserrat Regular", 18 * -1),
        )

        self.canvas.create_text(
            90.0,
            179.0,
            anchor="nw",
            text="application supported by",
            fill="#FFFFFF",
            font=("Montserrat Regular", 18 * -1),
        )

        self.canvas.create_text(
            90.0,
            208.0,
            anchor="nw",
            text="custom end-to-end encryption.",
            fill="#FFFFFF",
            font=("Montserrat Regular", 18 * -1),
        )

        self.canvas.create_text(
            90.0,
            237.0,
            anchor="nw",
            text="With LiveChat you can talk to",
            fill="#FFFFFF",
            font=("Montserrat Regular", 18 * -1),
        )

        self.canvas.create_text(
            90.0,
            266.0,
            anchor="nw",
            text="your friends near and far",
            fill="#FFFFFF",
            font=("Montserrat Regular", 18 * -1),
        )

        self.canvas.create_text(
            90.0,
            295.0,
            anchor="nw",
            text="without worrying about security.",
            fill="#FFFFFF",
            font=("Montserrat Regular", 18 * -1),
        )

        self.canvas.create_text(
            90.0,
            324.0,
            anchor="nw",
            text="Login or",
            fill="#FFFFFF",
            font=("Montserrat Regular", 18 * -1),
        )
        
        self.canvas.create_text(
            90.0,
            353.0,
            anchor="nw",
            text="Sign Up now",
            fill="#FFFFFF",
            font=("Montserrat Regular", 18 * -1),
        )

    def validateLogin(self):
        if self.username.get() == "" or self.password.get() == "":
            return

        if not self.connecting:
            self.controller.username = self.username.get()
            self.controller.client.connect_to_server(self.username.get(), self.password.get())
            self.connecting = True

        self.controller.chat_frame.tkraise()

class ChatBox(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#4682B4")
        self.grid(row=0, column=0, sticky="nsew")

        self.chat_label = tkinter.Label(self, text="Chat:", fg="white", bg="#4682B4")
        self.chat_label.config(font=("Calibri,14"))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self, width=200, height=20) 
        self.text_area.config(state='disabled')
        self.text_area.pack(padx=20, pady=5)

        self.message_label = tkinter.Label(self, text="Message:", fg="white", bg="#4682B4")
        self.message_label.config(font=("Calibri,14"))
        self.message_label.pack(padx=20, pady=5)

        self.message_box = tkinter.Text(self, width=200, height=3)
        self.message_box.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self, text="Send", bg="#4682B4", borderwidth=3,
                                          activebackground="#4682B4", activeforeground="Orange", command=self.chat)
        self.send_button.config(font=("Calibri,12"))
        self.send_button.place(x=110.0, y=500, width=190.0, height=48.0)
        

        self.select_file_button = tkinter.Button(self, text="Upload File", bg="#4682B4", borderwidth=3,
                                                activebackground="#4682B4", activeforeground="Orange",
                                                 command=self.get_file_path)
        self.select_file_button.config(font=("Calibri,12"))
        self.select_file_button.place(x=409.0, y=500, width=190.0, height=48.0)

        self.send_file_button = tkinter.Button(self, text="Download File", bg="#4682B4", borderwidth=3,
                                                activebackground="#4682B4", activeforeground="Orange",
                                               command=self.fileDownloadHandler)
        self.send_file_button.config(font=("Calibri,12"))
        self.send_file_button.place(x=700.0, y=500, width=190.0, height=48.0)
        self.gui_done = True

        # When window is closed we call end function
        #self.protocol("WM_DELETE_WINDOW", self.end)

        # Binds return button to func
        # self.bind('<Return>', lambda event: self.chat())

    def recv_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert('end', message)
        self.text_area.yview('end')
        self.text_area.config(state='disabled')

    def get_file_path(self):
        settings.file_name = filedialog.askopenfilename()
        print (f"Settings is saved as {settings.file_name}")
        if settings.file_name is settings.last_file:
            print("NO FILE")
            messagebox.showerror("Please select a file first")
        else:
            settings.last_file = settings.file_name
            self.file_handler()

    # def on_file_confirmed(self):
#         global file_name
#         global last_file
#         if file_name is last_file:
#             print("NO FILE")
#             messagebox.showerror("Please select a folder first")
#             # Who to send to
#         else:
#             last_file = file_name
#             self.fileHandler()
            # DO something with file name

    def file_handler(self):
        message = "SENDXX"
        self.controller.client.send_message(message)

        
    def fileDownloadHandler(self):

        check_for_file = "CXFXL"
        self.controller.client.send_message(check_for_file)    

        # if not settings.file_name:
        #     print (settings.file_name)
        #     print("No file available to download")
        #     # We need to break or continue or something
        #     # This checks locally, so no point... we need a flag from server letting us know there exists a file in the server ready to be downloaded.

    def no_file(self):
        print("No file available to download")
    
    def xqc(self):
        message = "RECVXX"
        self.controller.client.send_message(message)    

    def chat(self, _event=None):
        #print("do something please")
        message = f"{self.controller.username}: {self.message_box.get('1.0', 'end')}"
        self.controller.client.send_message(message)
        self.message_box.delete('1.0', 'end')
        # {"type":"Text", "body":"the message"}
        # If we detect user is sending a file we can update a global var with file name

if __name__ == '__main__':
    app = App(None)
    app.mainloop()