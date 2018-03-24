from bluepy import btle
import time
import argparse
import imutils
import time
import mido
import sys
import threading
from mido import Message

# deprecated because it belongs to Ableton
heart_to_bpm = {
0 : 0,
27 : 1,
35 : 2,
43 : 3,
50 : 4,
58 : 5,
66 : 6,
73 : 7,
81 : 8,
89 : 9,
97 : 10,
104 : 11,
112 : 12,
120 : 13,
127 : 14,
135 : 15,
143 : 16,
151 : 17,
158 : 18,
166 : 19,
174 : 20,
181 : 21,
197 : 22,
205 : 24,
212 : 25,
220 : 26,
228 : 27,
235 : 28}

def findBPM(hr):
	while hr not in heart_to_bpm:
		hr -=1
	return heart_to_bpm[hr]

def goConnectWithRetry(mac):
	while True:
		try:
			return goConnect(mac)
		except (btle.BTLEException):
			time.sleep(1)
			pass

def goConnect(mac):
	print "Connecting to",mac,"..."
	p = btle.Peripheral(mac, addrType=btle.ADDR_TYPE_PUBLIC)

	cccid = btle.AssignedNumbers.client_characteristic_configuration
	hrmid = btle.AssignedNumbers.heart_rate
	hrmmid = btle.AssignedNumbers.heart_rate_measurement

	service, = [s for s in p.getServices() if s.uuid==hrmid]
	ccc, = service.getCharacteristics(forUUID=str(hrmmid))
	desc = p.getDescriptors(service.hndStart,
	                        service.hndEnd)
	d, = [d for d in desc if d.uuid==cccid]
	p.writeCharacteristic(d.handle, '\1\0')

	p.setDelegate(MyDelegate(p))
	print "Connected!"
	return p




class MyDelegate(btle.DefaultDelegate, btle.Peripheral):
	global gWaitTime
    	gWaitTime = 60.0 / 50

	def __init__(self, argP):
        	btle.DefaultDelegate.__init__(self)
		p = argP

    	def handleNotification(self, cHandle, data):
		global gWaitTime
       		bpm = ord(data[1])
		if bpm == 0:
			print "Zero BPM."
			return		

		#cc = findBPM(bpm)
                gWaitTime = round(60.0 / bpm, 2)
		print "Current heartrate " + str(bpm) + "bpm equals " + str(gWaitTime) + "s sleep."

def sender_thread():
	while True:
		on = Message('note_on', channel=13, note=1, velocity=127)
        	port.send(on)
		time.sleep(gWaitTime)
		off = Message('note_off', channel=13, note=1, velocity=127)
		port.send(off)


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
args = ap.parse_args()

#use JACK
mido.set_backend('mido.backends.rtmidi/UNIX_JACK')

# open midi port
port = mido.open_output('Output', client_name='heart2MIDI')
print('Using {}'.format(port))

threading.Thread(target=sender_thread).start()


p = goConnectWithRetry('18:93:d7:4d:e4:03')

while True:
	try: 
		if p.waitForNotifications(3):
			continue
		else:
			print "TIMEOUT"
	except (btle.BTLEException):
		p = goConnectWithRetry('18:93:d7:4d:e4:03')


