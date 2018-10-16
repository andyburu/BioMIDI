#! /usr/bin/env python3
from tkinter import *
import threading
import time
import config

class MIDItoDMXWindow:
    # use default value before setConfig has been called 
    conf = config.Config()
    
    def b1(self, event):
        self.conf.C_MD_WAIT = self.varWait.get()
        self.conf.C_MD_CHANNEL = self.varChan.get()
        self.conf.C_MD_MOD = self.varMod.get()
        self.conf.prettyPrint()
        
    def hide(self):
        self.root.withdraw()

    def destroy(self):
        self.root.quit()
        self.root.update()
            
    def run(self):
        self.root = Tk()
        Label(self.root, 
            text="BioMIDI MIDItoDMX",
            font="Verdana 24").grid(row=0)

        Label(self.root, 
            text="Written by Andy Buru (andy@andyburu.se)\n",
            font="Verdana 12").grid(row=1)

        Label(self.root,
            text="\nWait time between DMX messages").grid(row=2)
        self.varWait = IntVar(self.root, value=self.conf.C_MD_WAIT)
        Entry(self.root,
            textvariable=self.varWait,
            width=5,
            bd=1).grid(row=3)
    
        Label(self.root,
            text="\nDMX Channel").grid(row=4)
        self.varChan = IntVar(self.root, value=self.conf.C_MD_CHANNEL)
        Entry(self.root,
            textvariable=self.varChan,
            width=5,
            bd=1).grid(row=5)
   
        Label(self.root,
            text="\nPercent modifier").grid(row=6)
        self.varMod = IntVar(self.root, value=self.conf.C_MD_MOD)
        Entry(self.root,
            textvariable=self.varMod,
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

    def show(self):
        self.root.update()
        self.root.deiconify()
        
    def setConfig(self,  conf):
        self.conf = conf
        self.varWait.set(conf.C_MD_WAIT)
        self.varChan.set(conf.C_MD_CHANNEL)
        self.varMod.set(conf.C_MD_MOD)
        
    def __init__(self):
        global windowThread
        self.windowThread = threading.Thread(target=self.run)
        self.windowThread.start()
        time.sleep(1)
        return
