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
#from PyQt5 import Qt
#import notify2
import sys
from os import path
from tkinter import *
from PIL import ImageTk, Image
from threading import Thread
import socket

__author__ = 'Atta Jirofty'
__doc__ = " This module is written for Broadcasting messages (client usage)"


class GUI():
    def __init__(self):
        self.win = tk.Tk() #initializing the main frame
        self.win.geometry("250x230") #window size
        self.win.title("Hardware R&D Broadcasting System") #title of the window
        self.createWidgets() #calling widgets
        self.win.iconbitmap('icon2.ico') #icon path
        self.win.resizable(0, 0) #unable to resize the window
        #Add Image
        load = Image.open("img2.png")
        render = ImageTk.PhotoImage(load)
        img = Label(self.win, image=render)
        img.image = render
        img.place(x=12,y=80)


    def runServer(self):
        #creating container
        self.win.withdraw() #hiding the main window
        self.chatPage = Toplevel() #making another window for sending messages
        self.chatPage.title(" Chat Page ") #title of the chat page
        self.chatContainer = ttk.LabelFrame(self.chatPage, text=' Chat Page ') #making a container for chat page
        self.chatContainer.grid(column=0, row=0, padx=10, pady=10) #modifying chat page container
        # adding scroll box for chat dialogs
        scrolW = 40
        scrolH = 10
        self.scr = scrolledtext.ScrolledText(self.chatContainer, width=scrolW, height=scrolH, wrap=tk.WORD)
        self.scr.grid(column=0, columnspan=3)
        self.scr.configure(state='disabled')
        # adding back button
        self.action = ttk.Button(self.chatContainer, text='Back', command=self.backClick)
        self.action.grid(column=3, row=1)
        #Back-end procceses
        port = 12345
        self.client(self.hostIp.get(), int(port))


    def client(self, _host, _port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f'Trying to connect to : {_host}, ({_port})')
            s.connect((_host, _port))
            print("Connected ...")
            while True:
                resp = s.recv(4096).decode()

                print(f'Admin > {resp}')
                self.scr.configure(state='normal')
                self.scr.insert(tk.INSERT, 'Admin -> ' + resp + '\n')
                self.scr.configure(state='disabled')

                if (self.chatPage.winfo_viewable() == 0 and resp): #or (not self.chatPage.focus())): # for sending notifications
                    self.win.deiconify()
                    mBox.showinfo(" ! ", "Admin just send a message ! \n Check it out fast")
                    self.win.withdraw()


    def backClick(self):
        self.action.configure(text='Back')
        self.chatPage.withdraw()
        self.win.deiconify()


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
        self.container = ttk.LabelFrame(self.win, text=" Client ")
        self.container.grid(column=0, row=0, padx=10, pady=10)
        #entry
        ttk.Label(self.container, text='Enter Admin IP :').grid(column=0, row=0, sticky=tk.W)
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
