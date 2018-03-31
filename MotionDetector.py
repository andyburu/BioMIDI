#! /usr/bin/env python3
import nsmclient 
import MotionDetectorWindow
import MotionDetectorWebcam
import config
import pickle
import os

conf = config.Config()
dataFile = False
prettyName = "MotionDetector"
INI_FILE = prettyName + ".obj"
window = MotionDetectorWindow.MotionDetectorWindow()

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
        
        return True,  "Found no file to load."

    filehandler = open(dataFile, 'rb')
    conf = pickle.load(filehandler)
    
    conf.prettyPrint()
    
    window.setConfig(conf)
    
    global webcam
    webcam = MotionDetectorWebcam.MotionDetectorWebcam(conf)
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
    window.destroy()
    webcam.die()
    return True

#Optional functions
optionalFunctions = {
        "function_quit" : myQuit,  #Accept zero parameters. Return True or False
        "function_showGui" : myShowGui, #Accept zero parameters. Return True or False
        "function_hideGui" : myHideGui, #Accept zero parameters. Return True or False
        "function_sessionIsLoaded" : None, #No return value needed.
        } 

ourNsmClient, process = nsmclient.init(prettyName = prettyName, capabilities = capabilities, requiredFunctions = requiredFunctions, optionalFunctions = optionalFunctions,  sleepValueMs = 0) 

#Direct send only functions for your program.
#ourNsmClient.updateProgress(value from 0.1 to 1.0) #give percentage during load, save and other heavy operations
#ourNsmClient.setDirty(True or False) #Inform NSM of the save status. Are there unsaved changes?
#ourNsmClient.sendError(errorCode or String, message string) #for a list of error codes: http://non.tuxfamily.org/nsm/API.html#n:1.2.5.

while True:
    process()
