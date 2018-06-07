#! /usr/bin/env python3
from bluepy import btle
import time
import mido
import threading
import nsmclient
import logging
import pickle
import os
import config
import HeartDetectorWindow
from mido import Message


Wahoo = "ef:24:39:80:39:cd"
China = "18:93:d7:4d:e4:03"
addr = China
gRun = True
conf = config.Config()
dataFile = False
prettyName = "HeartDetector"
INI_FILE = prettyName + ".obj"
window = HeartDetectorWindow.HeartDetectorWindow()
#logging.getLogger().setLevel(logging.DEBUG)

def makeDramatic(normal):
    mid = normal - conf.C_HB_NORMAL
    dramatic = mid * conf.C_HB_DRAMATIC
    dramatic += conf.C_HB_NORMAL
    if dramatic > conf.C_HB_NORMAL * 2:
        dramatic = conf.C_HB_NORMAL * 2
    logging.debug("DRAMA " + str(normal) + ">>" + str(dramatic))
    return dramatic
    
def goConnectWithRetry(mac):
    while gRun:
        try:
            return goConnect(mac)
        except (btle.BTLEException):
            time.sleep(1)
            pass

def goConnect(mac):
    window.setConnectionStatus("Trying...")
    logging.info("Connecting to " + str(mac) + "...")
    p = btle.Peripheral(mac, addrType=btle.ADDR_TYPE_PUBLIC)

    cccid = btle.AssignedNumbers.client_characteristic_configuration
    hrmid = btle.AssignedNumbers.heart_rate
    hrmmid = btle.AssignedNumbers.heart_rate_measurement

    service, = [s for s in p.getServices() if s.uuid==hrmid]
    ccc, = service.getCharacteristics(forUUID=str(hrmmid))
    desc = p.getDescriptors(
        service.hndStart,
        service.hndEnd)
    d, = [d for d in desc if d.uuid==cccid]
    p.writeCharacteristic(d.handle, str.encode('\1\0'))

    p.setDelegate(MyDelegate(p))
    window.setConnectionStatus("Connected")
    logging.info("Connected!")
    return p

class MyDelegate(btle.DefaultDelegate, btle.Peripheral):
    global gWaitTime
    gWaitTime = 60.0 / 50

    def __init__(self, argP):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        global gWaitTime
        bpm = data[1]
        if bpm == 0:
            window.setConnectionStatus("Zero BPM.")
            logging.debug("Zero BPM.")
            return      
                
        bpm = makeDramatic(bpm)
        
        window.setConnectionStatus("Ok. " + str(bpm) + "bpm")
        gWaitTime = round(60.0 / bpm, 2)
        logging.debug("Current heartrate " + str(bpm) + "bpm equals " + str(gWaitTime) + "s sleep.")

def sender_thread(port):
    while gRun:
        on = Message('note_on', channel=13, note=1, velocity=127)
        port.send(on)
        time.sleep(gWaitTime)
        off = Message('note_off', channel=13, note=1, velocity=127)
        port.send(off)

def main_thread():
    #use JACK
    mido.set_backend('mido.backends.rtmidi/UNIX_JACK')

    # open midi port
    port = mido.open_output('Heartbeat', client_name='Heart Detector (OUT)')
    print('Using {}'.format(port))

    threading.Thread(target=sender_thread,  args=(port,)).start()
    p = goConnectWithRetry(addr)

    while gRun:
        try: 
            if p.waitForNotifications(3):
                continue
            else:
                window.setConnectionStatus("Time-out")
                logging.debug("TIMEOUT")
        except (btle.BTLEException):
            p = goConnectWithRetry(addr)



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
    threading.Thread(target=main_thread).start()
    
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
