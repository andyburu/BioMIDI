import argparse
import datetime
import imutils
import time
import cv2
import mido
import sys
from mido import Message

# MIDI conversion
gHighestSeenChange = 1
gMidiChange = 1
gLastNote = 0
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-d", "--display", help="display a video window", action="store_true");
ap.add_argument("-m", "--map", help="send only one mapping midi command", action="store_true");
ap.add_argument("-r", "--readjust", help="continously readjust what is a big movement", type=int)
ap.add_argument("-n", "--note", help="send notes instead of midi commands", action="store_true")
ap.add_argument("-f", "--fullscreen", help="fullscreen mode", action="store_true")
args = ap.parse_args()
 
# if the video argument is None, then we are reading from webcam
if args.video is None:
	camera = cv2.VideoCapture(1)
	time.sleep(0.25)
 
# otherwise, we are reading from a video file
else:
	camera = cv2.VideoCapture(args["video"])


if args.fullscreen:
	cv2.namedWindow("M2M Motion", cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty("M2M Motion", cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
if args.display:
	cv2.namedWindow("M2M Motion", cv2.WINDOW_NORMAL)
#	cv2.namedWindow("M2M Raw", cv2.WINDOW_NORMAL)
	
# open midi port
port = mido.open_output(None, autoreset=False)
print('Using {}'.format(port))

# send mapping command
if args.map:
	cmd1 = Message('control_change', channel=13, control=1, value=0)
	print('Sending {}'.format(cmd1))
	port.send(cmd1)
	sys.exit(0)
else:
	print("Not in mapping mode.")
 
# initialize the first frame in the video stream
previousFrame = None
gray = None

# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	(grabbed, frame) = camera.read()
	text = "Still"
 
	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if not grabbed:
		break

	# save the previous frame and grab a new
	previousFrame = gray

	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (7, 7), 0)

	# skip diff if this was the first frame
	if previousFrame is None:
		continue

	# compute the absolute difference between the current frame and
	# previous frame
	frameDelta = cv2.absdiff(previousFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)

	# compress image array to one int
        currentChange = sum(sum(thresh))

	# update the highest found if needed
	if currentChange >= gHighestSeenChange:
		gHighestSeenChange = currentChange
		
	percent = float(currentChange) / float(gHighestSeenChange)
	gMidiChange = int(percent * 127)

	# slowly readjust the highest found	
	if args.readjust and gHighestSeenChange >= int(args.readjust):
                gHighestSeenChange = gHighestSeenChange - args.readjust

	# send midi message
	if args.note:
		note = int(gMidiChange/12)
		if note != gLastNote: 
			cmd1 = Message('note_off', channel=13, note=gLastNote)
			port.send(cmd1)
			cmd2 = Message('note_on', channel=13, note=note)
			port.send(cmd2)
			print("note:" + str(note))
		gLastNote = note
	else:
        	cmd3 = Message('control_change', channel=13, control=1, value=int(gMidiChange))
        	port.send(cmd3)

	# show display if needed
        if args.display:
                cv2.putText(thresh, "Movement in MIDI: {}".format(gMidiChange), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.imshow("M2M Motion", thresh)
#		cv2.imshow("M2M Raw", gray)

	# show fullscreen if needed
	if args.fullscreen:
		cv2.imshow("M2M Motion", thresh)

	# check for keyboard input	
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break

	# if the 'd' key is pressed, dump the threshold frame
	if key == ord("d"):
		print('midi:' + str(gMidiChange))
		print('high:' + str(gHighestSeenChange));
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
