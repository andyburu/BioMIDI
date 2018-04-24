#! /usr/bin/env python3
from tkinter import *
import threading
import time
import config

class MotionDetectorWindow:
   # use default value before setConfig has been called 
    conf = config.Config()
    
    def b1(self, event):
        self.conf.C_DISPLAY_VIDEO = self.varDisplay.get()
        self.conf.C_TRIGGER_BY_HEARTBEAT = self.varTriggerByHeartBeat.get()
        self.conf.C_TRIGGER_BY_TIMING = self.varTriggerByTiming.get()
        self.conf.C_VIDEO_FPS = self.varVideoFPS.get()
        self.conf.C_MIDI_MPS = self.varMidiMPS.get()
        self.conf.C_AMPLIFIER = self.varAmplifier.get()
        self.conf.prettyPrint()
        
    def hide(self):
        self.root.withdraw()

    def destroy(self):
        self.root.quit()
        self.root.update()
            
    def run(self):
        self.root = Tk()
        Label(self.root, 
            text="BioMIDI Motion Detector",
            font="Verdana 24").grid(row=0)

        Label(self.root, 
            text="Written by Andy Buru (andy@andyburu.se)\n",
            font="Verdana 12").grid(row=1)

        # Display on or off
        self.varDisplay=IntVar(self.root, value=self.conf.C_DISPLAY_VIDEO)
        Checkbutton(self.root,
            text="Display Video Window",
            variable=self.varDisplay, 
            onvalue=1,
            offvalue=0).grid(row=2)
        
        # Trigger mode
        self.varTriggerByHeartBeat=IntVar(self.root, value=self.conf.C_TRIGGER_BY_HEARTBEAT)
        Checkbutton(self.root, 
            text="Trigger by MIDI Heart Beat",      
            variable=self.varTriggerByHeartBeat,
            onvalue=1,
            offvalue=0).grid(row=3)

        self.varTriggerByTiming=IntVar(self.root, value=self.conf.C_TRIGGER_BY_TIMING)
        Checkbutton(self.root,
            text="Trigger by Timing",
            variable=self.varTriggerByTiming,
            onvalue=1,
            offvalue=0).grid(row=4)

        # Timing configuration
        Label(self.root, 
            text="\nVideo FPS (Frames per Second) to update.").grid(row=6)

        self.varVideoFPS = IntVar(self.root, value=self.conf.C_VIDEO_FPS)
        Entry(self.root,
            textvariable=self.varVideoFPS,
            width=5,
            bd=1).grid(row=7)

        Label(self.root,
            text="\nMidi MPS (Messages per Second) to send.").grid(row=8)
        self.varMidiMPS = IntVar(self.root, value=self.conf.C_MIDI_MPS)

        Entry(self.root,
            textvariable=self.varMidiMPS,
            width=5,
            bd=1).grid(row=9)

        # Readjust configuration
        Label(self.root, 
            text="\nAmplify the motion 1=none, 3=some, 5=lot.").grid(row=10)
        self.varAmplifier = IntVar(self.root, value=self.conf.C_AMPLIFIER)

        Entry(self.root,
            textvariable=self.varAmplifier,
            width=5,
            bd=1).grid(row=11)
    
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
        self.varDisplay.set(conf.C_DISPLAY_VIDEO)
        self.varTriggerByHeartBeat.set(conf.C_TRIGGER_BY_HEARTBEAT)
        self.varTriggerByTiming.set(conf.C_TRIGGER_BY_TIMING)
        self.varVideoFPS.set(conf.C_VIDEO_FPS)
        self.varMidiMPS.set(conf.C_MIDI_MPS)
        self.varAmplifier.set(conf.C_AMPLIFIER)
        
    def __init__(self):
        global windowThread
        self.windowThread = threading.Thread(target=self.run)
        self.windowThread.start()
        time.sleep(1)
        return
