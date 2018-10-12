#! /usr/bin/env python3
import nsmclient 
import config
import pickle
import os
import threading
import time
import mido
import logging
import FadeBackWindow
from mido import Message


conf = config.Config()
dataFile = False
running = True
in_port = False
out_port = False
stepping = 0
prettyName = "FadeBack"
INI_FILE = prettyName + ".obj"
window = FadeBackWindow.FadeBackWindow()

def outLoop(out_port):
    global running, stepping

    while running:
        time.sleep(1 * 100 / conf.C_FB_FACTOR)
        if stepping == 0:
            window.setTimeOut("Open")
        else:
            stepping -= 1
            window.setTimeOut(stepping)

            if(conf.C_FB_STYLE == 0 and stepping < 10):
                cc = Message('control_change', channel=0, control=1, value=int(stepping*12.7))
                out_port.send(cc)

            if(conf.C_FB_STYLE == 1):
                cc = Message('control_change', channel=0, control=1, value=int(stepping))
                out_port.send(cc)

def inLoop(in_port, out_port):
    global running, stepping

    while running:
        for msg in in_port.iter_pending():
            midi = msg.value
            channel = msg.channel
            if midi > stepping and midi > conf.C_FB_FILTER:
                stepping = midi + conf.C_FB_MIN
                if(conf.C_FB_STYLE == 0):
                    cc = Message('control_change', channel=0, control=1, value=127)
                    out_port.send(cc)

        time.sleep(0.1)


capabilities = {
    "switch" : False,       #client is capable of responding to multiple `open` messages without restarting
    "dirty" : False,        #client knows when it has unsaved changes
    "progress" : False,     #client can send progress updates during time-consuming operations
    "message" : True,       #client can send textual status updates
    "optional-gui" : True,  #client has an optional GUI 
}

#requiredFunctions
def myLoadFunction(path,  name):
    global conf, dataFile, out_port, in_port
    dataFile = path + "/" + INI_FILE
    if not os.path.exists(dataFile):
        return True,  "Found no file to be loaded."
        
        return True,  "Found no file to load."

    filehandler = open(dataFile, 'rb')
    conf = pickle.load(filehandler)
    window.setConfig(conf)
    conf.prettyPrint()

    #use JACK
    mido.set_backend('mido.backends.rtmidi/UNIX_JACK')

    # open midi port
    out_port = mido.open_output('Output', client_name='Fade Back (OUT)')
    logging.info("Outgoing port: {}".format(out_port))
 
    in_port = mido.open_input('Input', client_name='Fade Back (IN)')
    logging.info("Incoming port: {}".format(in_port))
    
    threading.Thread(target=inLoop, args=(in_port, out_port)).start()
    threading.Thread(target=outLoop, args=(out_port,)).start()
    
    return True, dataFile + " loaded!"
    
def mySaveFunction(path):
    global conf, dataFile
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
    global running
    running = False
    time.sleep(2)
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
