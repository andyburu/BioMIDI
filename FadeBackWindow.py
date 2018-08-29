#! /usr/bin/env python3
from tkinter import *
import threading
import time
import config

class FadeBackWindow:
    # use default value before setConfig has been called 
    conf = config.Config()
    
    def b1(self, event):
        self.conf.C_FB_STYLE = self.varStyle.get()
        self.conf.C_FB_FACTOR = self.varFactor.get()
        self.conf.prettyPrint()
        
    def hide(self):
        self.root.withdraw()

    def destroy(self):
        self.root.quit()
        self.root.update()
            
    def run(self):
        self.root = Tk()
        Label(self.root, 
            text="BioMIDI Fade Back",
            font="Verdana 24").grid(row=0)

        Label(self.root, 
            text="Written by Andy Buru (andy@andyburu.se)\n",
            font="Verdana 12").grid(row=1)


        Label(self.root,
            text="\nTime Out").grid(row=2)
        self.varTimeOut = StringVar()
        self.varTimeOut.set("Open")
        Entry(self.root,
            state="readonly", 
            width=10, 
            bd=1, 
            textvariable=self.varTimeOut).grid(row=3)
    
        Label(self.root,
            text="\nTime out percent modifier").grid(row=4)
        self.varFactor = IntVar(self.root, value=self.conf.C_FB_FACTOR)
        Entry(self.root,
            textvariable=self.varFactor,
            width=5,
            bd=1).grid(row=5)
    
        Label(self.root,
            text="\nReturn Style").grid(row=6)
        self.varStyle = IntVar(self.root, value=self.conf.C_FB_STYLE)
        Radiobutton(self.root,
            variable=self.varStyle,
            width=20,
            text="Gradual",
            value=1).grid(row=7)
        Radiobutton(self.root,
            variable=self.varStyle,
            width=20,
            text="Sudden",
            value=0).grid(row=8)
    
        # Apply button
        Button(
            self.root,
            text="Apply").grid(row=3, column=1)
        self.root.bind_class('Button', '<Button-1>', self.b1)
        
        print("Starting mainloop.")
        self.root.mainloop()
        print("Exiting mainloop!")        

    def setTimeOut(self, time):
        self.varTimeOut.set(time)
        
    def show(self):
        self.root.update()
        self.root.deiconify()
        
    def setConfig(self,  conf):
        self.conf = conf
        self.varStyle.set(conf.C_FB_STYLE)
        self.varFactor.set(conf.C_FB_FACTOR)
        
    def __init__(self):
        global windowThread
        self.windowThread = threading.Thread(target=self.run)
        self.windowThread.start()
        time.sleep(1)
        return
