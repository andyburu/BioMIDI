#! /usr/bin/env python3
from tkinter import *
import threading
import time

class MotionDetectorWindow: 
    def b1(self, event):
        print("Apply")
        
    def hide(self):
        self.root.withdraw()

    def destroy(self):
        self.root.quit()
        self.root.update()
            
    def run(self):
        self.root = Tk()
        self.labTitle = Label(
            self.root, 
            text="BioMIDI Motion Detector",
            font="Verdana 24").grid(row=0)

        self.labAuthor = Label(
            self.root, 
            text="Written by Andy Buru (andy@andyburu.se)\n",
                    font="Verdana 12").grid(row=1)

        # Display on or off
        self.varDisplay=IntVar(self.root, value=0)
        self.cheDisplay = Checkbutton(
            self.root,
            text="Display Video Window",
            onvalue=1,
            offvalue=0).grid(row=2)
        
        # Trigger mode
        self.varTriggerByMidi=IntVar(self.root, value=1)
        self.cheTriggerByMidi = Checkbutton(
            self.root, 
            text="Trigger by MIDI Heart Beat",      
            variable=self.varTriggerByMidi,
            onvalue=1,
            offvalue=0).grid(row=3)

        self.varTriggerByTiming=IntVar(self.root, value=0)
        self.cheTriggerByTiming = Checkbutton(
            self.root,
            text="Trigger by Timing",
            variable=self.varTriggerByTiming,
            onvalue=1,
            offvalue=0).grid(row=4)

        # Timing configuration
        self.lVideoFPS = Label(
            self.root, 
            text="\nVideo FPS (Frames per Second) to update.").grid(row=6)

        self.varVideoFPS = IntVar(self.root, value=30)
        self.eVideoFPS = Entry(
            self.root,
            textvariable=self.varVideoFPS,
            width=5,
            bd=1).grid(row=7)

        self.lMidiMPS = Label(
            self.root,
            text="\nMidi MPS (Messages per Second) to send.").grid(row=8)
        self.varMidiMPS = IntVar(self.root, value=5)

        self.eMidiMPS = Entry(
                self.root,
                textvariable=self.varMidiMPS,
                width=5,
                bd=1).grid(row=9)

        # Readjust configuration
        self.lReadjust = Label(
            self.root, 
            text="\nAmount of continously readjustment of what is much motion.").grid(row=10)
        self.varReadjust = IntVar(self.root, value=200)

        self.eMidiMPS = Entry(
                self.root,
                textvariable=self.varReadjust,
                width=5,
                bd=1).grid(row=11)
    
        # Apply button
        self.bApply = Button(
            self.root,
            text="Apply").grid(row=3, column=1)
        self.root.bind_class('Button', '<Button-1>', self.b1)
        
        print("Starting mainloop.")
        self.root.mainloop()
        print("Exiting mainloop!")        

    def show(self):
        self.root.update()
        self.root.deiconify()
        
    def __init__(self):
        global windowThread
        self.windowThread = threading.Thread(target=self.run)
        self.windowThread.start()
        time.sleep(1)
        return
