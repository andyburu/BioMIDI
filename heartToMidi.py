from bluepy import btle
import time
import argparse
import imutils
import time
import mido
import sys
from mido import Message

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
    def __init__(self, argP):
        btle.DefaultDelegate.__init__(self)
	p = argP

    def handleNotification(self, cHandle, data):
        bpm = ord(data[1])
	if bpm == 0:
		print "Zero BPM."
		return		

	cc = findBPM(bpm)
        print "Sending",bpm,"=",cc
        cmd3 = Message('control_change', channel=14, control=1, value=int(cc))
        port.send(cmd3)


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--map", help="send only one mapping midi command", action="store_true");
args = ap.parse_args()

# open midi port
port = mido.open_output(None, autoreset=False)
print('Using {}'.format(port))

# send mapping command
if args.map:
        cmd1 = Message('control_change', channel=14, control=1, value=0)
        print('Sending {}'.format(cmd1))
        port.send(cmd1)
        sys.exit(0)
else:
        print("Not in mapping mode.")

p = goConnectWithRetry('18:93:d7:4d:e4:03')

while True:
	try: 
		if p.waitForNotifications(3):
			continue
		else:
			print "TIMEOUT"
	except (btle.BTLEException):
		p = goConnectWithRetry('18:93:d7:4d:e4:03')


