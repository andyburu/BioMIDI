#! /usr/bin/env python3
from tkinter import *
import threading
import time
import config
import scales

class NoteOnScaleWindow:
   # use default value before setConfig has been called 
    conf = config.Config()
    
    def setConfig(self,  conf):
        self.conf = conf
        self.varScale.set(self.conf.C_CURRENT_SCALE)
        self.varOctaveOffset.set(self.conf.C_OCTAVE_OFFSET)
    
    def b1(self, event):
        self.conf.C_CURRENT_SCALE = self.varScale.get()
        self.conf.C_OCTAVE_OFFSET = self.varOctaveOffset.get()
        self.conf.prettyPrint()
    
    def hide(self):
        self.root.withdraw()

    def destroy(self):
        self.root.quit()
        self.root.update()
        
    def show(self):
        self.root.update()
        self.root.deiconify()
        
    def __init__(self):
        global windowThread
        self.windowThread = threading.Thread(target=self.run)
        self.windowThread.start()
        time.sleep(1)
        return
        
    def run(self):
        i=0
        self.root = Tk()
        
        Label(
            self.root, 
            text="BioMIDI Note On Scale",
            font="Verdana 24").grid(row=i)
        i+=1

        Label(
            self.root, 
            text="Written by Andy Buru (andy@andyburu.se)\n",
                    font="Verdana 12").grid(row=i)
        i+=1
                    
        
        # Scale configuration
        Label(
            self.root, 
            text="\nSelect scale to pick notes from.").grid(row=i)
        i+=1
        
        self.varScale = IntVar(self.root,  value=self.conf.C_CURRENT_SCALE)
        no = 0
        for n,  s in scales.Scales.SCALES:
            Radiobutton(
                self.root, 
                text=n, 
                variable=self.varScale, 
                value=no,
            ).grid(row=i)
            i+=1
            no+=1
                
        # Timing configuration
        Label(
            self.root, 
            text="\nOctave Off-set.").grid(row=i)
        i+=1
        
        self.varOctaveOffset = IntVar(self.root, value=self.conf.C_OCTAVE_OFFSET)
        Entry(
            self.root,
            textvariable=self.varOctaveOffset,
            width=5,
            bd=1).grid(row=i)
        i+=1
        
        # Apply button
        self.bApply = Button(
            self.root,
            text="Apply").grid(row=3, column=1)
        self.root.bind_class('Button', '<Button-1>', self.b1)
        
        print("Starting mainloop.")
        self.root.mainloop()
        print("Exiting mainloop!")       
