#! /usr/bin/env python3
from tkinter import *
import threading
import time
import config

class HeartDetectorWindow:
   # use default value before setConfig has been called 
    conf = config.Config()
    
    def b1(self, event):
        self.conf.C_HB_DRAMATIC = self.varDramatic.get()
        self.conf.C_HB_NORMAL = self.varNormal.get()
        self.conf.prettyPrint()
        
    def hide(self):
        self.root.withdraw()

    def destroy(self):
        self.root.quit()
        self.root.update()
            
    def run(self):
        self.root = Tk()
        Label(self.root, 
            text="BioMIDI Heart Detector",
            font="Verdana 24").grid(row=0)

        Label(self.root, 
            text="Written by Andy Buru (andy@andyburu.se)\n",
            font="Verdana 12").grid(row=1)


        Label(self.root,
            text="\nConnection Status").grid(row=2)
        self.varConnected = StringVar()
        self.varConnected.set("Disconnected")
        Entry(self.root,
            state="readonly", 
            width=10, 
            bd=1, 
            textvariable=self.varConnected).grid(row=3)
    
        Label(self.root,
            text="\nDramatic Factor (1 = normal, 3 = super dramatic)").grid(row=4)
        self.varDramatic = IntVar(self.root, value=self.conf.C_HB_DRAMATIC)
        Entry(self.root,
            textvariable=self.varDramatic,
            width=5,
            bd=1).grid(row=5)
    
        Label(self.root,
            text="\nNormal BPM (Beat per Minute)").grid(row=6)
        self.varNormal = IntVar(self.root, value=self.conf.C_HB_NORMAL)
        Entry(self.root,
            textvariable=self.varNormal,
            width=5,
            bd=1).grid(row=7)
    
        # Apply button
        Button(
            self.root,
            text="Apply").grid(row=3, column=1)
        self.root.bind_class('Button', '<Button-1>', self.b1)
        
        print("Starting mainloop.")
        self.root.mainloop()
        print("Exiting mainloop!")        

    def setConnectionStatus(self,  status):
        self.varConnected.set(status)
        
    def show(self):
        self.root.update()
        self.root.deiconify()
        
    def setConfig(self,  conf):
        self.conf = conf
        self.varDramatic.set(conf.C_HB_DRAMATIC)
        self.varNormal.set(conf.C_HB_NORMAL)
        
    def __init__(self):
        global windowThread
        self.windowThread = threading.Thread(target=self.run)
        self.windowThread.start()
        time.sleep(1)
        return
