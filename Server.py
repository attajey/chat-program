#============================
# IMPORTS
#============================
#GUI imports
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import messagebox as mBox
from tkinter import filedialog as fd
from tkinter import *
from PIL import ImageTk, Image

from os import path
from threading import Thread
from time import sleep
from queue import Queue
import signal
import socket
import sys
import threading
from threading import Lock
import datetime
import time

__author__ = 'Atta Jirofty - Summer 1398'

__doc__ = " This module is written for Broadcasting messages (admin usage)"


clients = [] #list of clients
lock = Lock() #for threading
date = datetime.datetime.now().strftime('%Y-%m-%d') #for naming history files



#==============================================================================
class Client(threading.Thread):
    def __init__(self, ip, _port, connection):
        threading.Thread.__init__(self)
        self.connection = connection
        self.ip = ip
        self.port = _port

    def run(self):
        pass

    def send_msg(self, msg):
        try:
            self.connection.sendall(msg.encode())
        except:
            clients.pop(0)
            print("♦♦♦♦♦♦♦♦♦♦♦♦♦♦\n••A Client left.\nYour previous message was not recieved by users!\n•○○•Sry 4 this bug•○○•\nTry Again\n♦♦♦♦♦♦♦♦♦♦♦♦♦♦\n ")



class Server:
    def __init__(self, ip, _port):
        self.ip = ip
        self.port = _port
        self.address = (self.ip, self.port)
        self.server = None

    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(self.address)
        except socket.error:
            if self.server:
                self.server.close()
            sys.exit(1)

    def run(self, *args, **kwargs):
        self.open_socket()
        self.server.listen(5)
        while True:
            lock.acquire()
            connection, (ip, _port) = self.server.accept()

            print(f'\n♠♠♠\nClient with IP: {ip} , Port: {_port} joined...\n♠♠♠\n\n#################\nAdmin >')

            c = Client(ip, _port, connection)
            c.start()
            c.join()

            clients.append(c)
            lock.release()
    @staticmethod
    def remove():
        clients.remove(c)
        print(f'\n Client with IP: {ip} disconnected\n\n############\n')



class Admin():
    def run(self, *args, **kwargs):
        while True:
            msg = input("Admin > ")

            for client in clients:
                client.send_msg(msg)
                f = open(str(date+'.txt'), "a+", encoding='utf-8')
                f.write( time.ctime() + " --> " + msg + "\n")

#===============================================================================
class GUI():
    def __init__(self):
        self.win = tk.Tk() #initializing the main frame
        self.win.geometry("250x250") #window size
        self.win.title("Hardware R&D Broadcasting System") #title of the window
        self.createWidgets() #calling widgets
        self.win.iconbitmap('icon2.ico') #icon path
        #self.win.resizable(0, 0) #unable to resize the window

        self.scr = scrolledtext.ScrolledText()
        #Add Image
        load = Image.open("img2.png")
        render = ImageTk.PhotoImage(load)
        img = Label(self.win, image=render)
        img.image = render
        img.place(x=12,y=100)


    def runServer(self):
        #creating container
        self.win.withdraw() #hiding the main window
        self.chatPage = Toplevel() #making another window for sending messages
        self.chatPage.title(" Chat Page ") #title of the chat page
        self.chatPage.geometry("520x290")
        self.chatPage.resizable(0, 0)
        self.chatContainer = ttk.LabelFrame(self.chatPage, text=' Chat Page ') #making a container for chat page
        self.chatContainer.grid(column=0, row=0, padx=10, pady=10) #modifying chat page container
        # adding scroll box for chat dialogs
        scrolW = 40
        scrolH = 10
        self.scr = scrolledtext.ScrolledText(self.chatContainer, width=scrolW, height=scrolH, wrap=tk.WORD)
        self.scr.grid(column=0, columnspan=3)
        self.scr.insert(tk.INSERT, 'There is no GUI for admin. Im so sorry for this deficiency.\nIn the next version, this feature will be added.\nUse cmd for sending messages.\nIf you wish to exit, press the Exit button or select the Exit option in menu on the top left side of the window.\n\nبرای ادمین رابط گرافیکی نوشته نشده است. برای این کمبود در برنامه عذرخواهم.\nدر ورژن بعدی این ویژگی به برنامه اضافه خواهد شد.\n' )
        # adding back & send button
        self.action = ttk.Button(self.chatContainer, text='Back', command=self.backClick)
        self.action.grid(column=3, row=1)
        self.exitButton = ttk.Button(self.chatPage, text='Exit', command=self._quit)
        self.exitButton.grid(column=3, row=2)
        #menuBar
        menuBar = Menu(self.chatPage)
        self.chatPage.config(menu=menuBar)
        #file menu
        fileMenu = Menu(menuBar, tearoff=0)
        fileMenu.add_command(label='Exit', command=self._quit)
        menuBar.add_cascade(label='Files', menu=fileMenu)

        port = 12345
        server = Server(self.hostIp.get(), int(port))
        admin=Admin()
        #server = Thread(target=server.run, daemon=True)
        #admin = Thread(target=admin.run, daemon=True)
        #admin.start()
        #server.start()
        server_thread = threading.Thread(target=server.run)
        admin_thread = threading.Thread(target=admin.run)
        server_thread.start()
        admin_thread.start()
        server_thread.join()
        admin_thread.join()


    def sendMsg(self):
        self.action.configure(text='Send')
        guiMsg = self.chitChat.get()
        return guiMsg


    def backClick(self):
        self.action.configure(text='Back')
        self.win.deiconify()
        self.chatPage.withdraw()


    def enterClick(self):
        self.action.configure(text='Enter')
        test = Thread(target=self.runServer, daemon=True)
        test.start()


    def _quit(self):
        answer = mBox.askyesno("Exit", "Are You Sure?")
        if (answer == True):
            self.win.quit()
            self.win.destroy()
            exit()


    def _msgBox(self):
        mBox.showinfo("About The Program", "A local network broadcasting system for ZharfPouyan company, Hardware section\n\nFor more information on how to use this program read the 'Instruction' text file\n\n--created by Atta Jirofty\n\n Summer 1398/2019")

    def createWidgets(self):
        self.container = ttk.LabelFrame(self.win, text=" Admin ")
        self.container.grid(column=0, row=0, padx=10, pady=10)

        version = tk.Text(self.container, height=1, width=13)
        version.grid(column=0, row=2, pady=5, sticky=tk.W)
        version.insert(tk.END, "Version 1.0.0")

        #entry
        ttk.Label(self.container, text='Enter IP :').grid(column=0, row=0, sticky=tk.W)
        self.hostIp = tk.StringVar()
        self.IpEntered = ttk.Entry(self.container, width=24, textvariable=self.hostIp)
        self.IpEntered.grid(column=0, row=1, sticky='W')
        self.IpEntered.focus()
        #button
        self.action = ttk.Button(self.container, text='Enter', command=self.enterClick)
        self.action.grid(column=3, row=1)
        #menuBar
        menuBar = Menu(self.win)
        self.win.config(menu=menuBar)
        #file menu
        fileMenu = Menu(menuBar, tearoff=0)
        fileMenu.add_command(label='Exit', command=self._quit)
        menuBar.add_cascade(label='Files', menu=fileMenu)
        #help menu
        helpMenu = Menu(menuBar, tearoff=0)
        helpMenu.add_command(label='About', command=self._msgBox)
        menuBar.add_cascade(label='Help', menu=helpMenu)
        #image



#==============================================================================

gui = GUI()
gui.win.mainloop()
f.close()
