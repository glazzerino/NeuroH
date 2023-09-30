import sys
import os
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as MessageBox
from datetime import datetime
import threading
import argparse
import math

from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

IP = "10.22.16.247"  # Escribe el IP aquí
PORT1 = 5005  # Escribe el primer puerto aquí

# First Client - 5005
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default=IP, help="The ip of the OSC server")
parser.add_argument("--port", type=float, default=PORT1, help="The port the OSC server is listening on (1)")
args = parser.parse_args()

client = udp_client.SimpleUDPClient(args.ip, args.port)



os.chdir(r"./")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.now = datetime.now()
        #For buttons
        self.btn = tk.Button(self, text="Start", command = self.start_clicked)
        self.btn.place(x=40,y=200)
        self.exit = tk.Button(self, text="Exit", command= lambda: app.destroy())
        self.exit.place(x=100,y=200)
        
        #For labels
        self.label1 = tk.Label(self,text='Select the subject:')
        self.label1.place(x=5, y=20)
        self.label2 = tk.Label(self, text='Select the Scene:')
        self.label2.place(x=5, y=70)
        self.label3 = tk.Label(self, text='Selected Emotion:')
        self.label3.place(x=5, y=130)
        self.label4 = Label(self, text=self.now)
        self.label4.place(x=50,y=350)
        
        #For comboboxes
        self.SelectSubject = tk.StringVar()
        self.SelectScenes = tk.StringVar()
        self.SelectEmotions = tk.StringVar()
        Subjects = ttk.Combobox(self, textvariable=self.SelectSubject)
        Subjects['values'] = ["Subject_" + str(m) for m in range (1,13)]
        Subjects['state'] = 'readonly' #prevent a typing value
        Subjects.place(x=5,y=40)
        Scenes = ttk.Combobox(self, textvariable=self.SelectScenes)
        Scenes['values'] = ["Scene_" + str(m) for m in range (1,5)]
        Scenes['state'] = 'readonly' #prevent a typing value
        Scenes.place(x=5,y=100)
        Emotions = ttk.Combobox(self, textvariable=self.SelectEmotions)
        Emotions['values'] = ['anger','disgust','fear','happiness','sadness','surprise','neutral']
        Emotions['state'] = 'readonly' #prevent a typing value
        Emotions.place(x=5,y=160)
        #For checkbuttons
        self.savedata_value = tk.BooleanVar()
        savedata = tk.Checkbutton(self, text="Save data", variable=self.savedata_value, command=self.savedata_clicked)
        savedata.place(x=50,y=250)
    


    def start_clicked(self):
        scene = self.SelectScenes.get()
        now = datetime.now()
        self.label4.config(text=now)
        print(now)
        client.send_message("/Interfaz/save", self.savedata_value.get())
        client.send_message("/Interfaz/subject", self.SelectSubject.get())
        client.send_message("/Interfaz/scene", self.SelectScenes.get())
        client.send_message("/Interfaz/date", now.strftime("%d/%m/%Y"))
        client.send_message("/Interfaz/hour", now.strftime("%H:%M:%S"))
        
        if scene == 'Scene_1':
            os.system('python scene02.py')
                  
        else:
            MessageBox.showerror("ERROR!", "No scene was selected.")
        
        return self.now
    
    def savedata_clicked(self):
        self.savedata_value.get()

if __name__ == "__main__":
    app = App()
    app.title("Neurohumanities Lab")
    app.geometry("800x400+10+10")
    app.resizable(False,False)
    app.mainloop()