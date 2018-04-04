#! /usr/bin/env python3
import nsmclient 
import config
import pickle
import os
import time
import mido
import threading
import logging
import NoteOnScaleWindow
import scales
from mido import Message

OCTAVE = 12 

window = NoteOnScaleWindow.NoteOnScaleWindow()
conf = config.Config()
dataFile = False
prettyName = "NoteOnScale"
INI_FILE = prettyName + ".obj"
gRun = True

def mainthread():
    lastMidi = 0
    global out_port
    
    #use JACK
    mido.set_backend('mido.backends.rtmidi/UNIX_JACK')

    # open midi port
    out_port = mido.open_output('Output', client_name='Note On Scale (OUT)')
    logging.info("Outgoing port: {}".format(out_port))

    in_port = mido.open_input('Input', client_name='Note On Scale (IN)')
    logging.info("Incoming port: {}".format(in_port))
    
    while gRun:
        for msg in in_port.iter_pending():
            midi = msg.value
            if midi == lastMidi or midi == 0:
                continue

            # send_midi_message(midi)
            threading.Thread(target=send_midi_message, args=(midi,  out_port)).start()
            lastMidi = midi
        time.sleep(0.1)
        
# pick a note from a scale
def midi_to_note_on_scale(midi):
    # find scale and octave from config
    s = scales.Scales.SCALES[conf.C_CURRENT_SCALE][1]
    o = OCTAVE * conf.C_OCTAVE_OFFSET
    
    scale_pos = midi / (127 / len(s))
    if len(s) == scale_pos: scale_pos = scale_pos-1
    return s[int(scale_pos)] + o

def send_midi_message(midi,  out_port):
    # select note
    note = midi_to_note_on_scale(midi)

    # turn on note
    on = Message('note_on', channel=13, note=note, velocity=int(midi))
    out_port.send(on)

    ms = 10000 / midi;

    # log and sleep
    logging.debug("lenght:" + str(ms) + "ms velocity:" + str(midi) + " note:" + str(note) + " thread:" + str(threading.currentThread().getName()))
    time.sleep(ms / 1000.0)

    # turn off note
    off = Message('note_off', channel=13, note=note, velocity=int(midi))
    out_port.send(off)

capabilities = {
    "switch" : False,       #client is capable of responding to multiple `open` messages without restarting
    "dirty" : False,        #client knows when it has unsaved changes
    "progress" : False,     #client can send progress updates during time-consuming operations
    "message" : True,       #client can send textual status updates
    "optional-gui" : True,  #client has an optional GUI 
    }

#requiredFunctions
def myLoadFunction(path,  name):
    global conf,  dataFile
    dataFile = path + "/" + INI_FILE
    if not os.path.exists(dataFile):
        return True,  "Found no file to be loaded."

    filehandler = open(dataFile, 'rb')
    conf = pickle.load(filehandler)
    
    window.setConfig(conf)
    
    conf.prettyPrint()
    threading.Thread(target=mainthread).start()
    
    return True, dataFile + " loaded!"
    
def mySaveFunction(path):
    global conf,  dataFile
    if dataFile == False:
            return True,  "Don't know where to save."
    
    if not os.path.exists(dataFile):
        os.makedirs(os.path.dirname(dataFile))
    
    conf.prettyPrint()
    
    filehandler = open(dataFile, 'wb')
    pickle.dump(conf, filehandler)
    return True, dataFile + " saved!"
    
requiredFunctions = {
    "function_open" : myLoadFunction, #Accept two parameters. Return two values. A bool and a status string. Otherwise you'll get a message that does not help at all: "Exception TypeError: "'NoneType' object is not iterable" in 'liblo._callback' ignored"
    "function_save" : mySaveFunction, #Accept one parameter. Return two values. A bool and a status string. Otherwise you'll get a message that does not help at all: "Exception TypeError: "'NoneType' object is not iterable" in 'liblo._callback' ignored"                   
    }

def myShowGui():
    window.show()
    return True
    
def myHideGui():
    window.hide()
    return True

def myQuit():
    global gRun
    gRun = False
    window.destroy()
    return True

#Optional functions
optionalFunctions = {
        "function_quit" : myQuit,  #Accept zero parameters. Return True or False
        "function_showGui" : myShowGui, #Accept zero parameters. Return True or False
        "function_hideGui" : myHideGui, #Accept zero parameters. Return True or False
        "function_sessionIsLoaded" : None, #No return value needed.
        } 

ourNsmClient, process = nsmclient.init(prettyName = prettyName, capabilities = capabilities, requiredFunctions = requiredFunctions, optionalFunctions = optionalFunctions,  sleepValueMs = 100) 

#Direct send only functions for your program.
#ourNsmClient.updateProgress(value from 0.1 to 1.0) #give percentage during load, save and other heavy operations
#ourNsmClient.setDirty(True or False) #Inform NSM of the save status. Are there unsaved changes?
#ourNsmClient.sendError(errorCode or String, message string) #for a list of error codes: http://non.tuxfamily.org/nsm/API.html#n:1.2.5.

while True:
    process()
