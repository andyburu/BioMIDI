import argparse
import imutils
import time
import cv2
import mido
import sys
from mido import Message

# globals
global gHighestSeenChange 
gHighestSeenChange = 1
global gMidiChange 
gMidiChange = 0
global args 

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--display", help="display a video window", action="store_true");
ap.add_argument("-r", "--readjust", help="continously readjust what is a big movement", type=int)
ap.add_argument("-f", "--fullscreen", help="fullscreen mode", action="store_true")
ap.add_argument("-v", "--verbose", help="spam trace message", action="store_true")
args = ap.parse_args()


#use JACK
mido.set_backend('mido.backends.rtmidi/UNIX_JACK')

# open midi port
port = mido.open_output('Output', client_name='Motion2MIDI')
print('Using {}'.format(port))


# if the video argument is None, then we are reading from webcam
camera = cv2.VideoCapture(0)
time.sleep(0.25)

if args.fullscreen:
	cv2.namedWindow("M2M Motion", cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty("M2M Motion", cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)

if args.display:
	cv2.namedWindow("M2M Motion", cv2.WINDOW_NORMAL)
	
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


	if args.verbose: print("Sending " + str(gMidiChange))
        cc = Message('control_change', channel=13, control=1, value=int(gMidiChange))
        port.send(cc)

	# slowly readjust the highest found	
	if args.readjust and gHighestSeenChange >= int(args.readjust):
                gHighestSeenChange = gHighestSeenChange - args.readjust

	# show display if needed
        if args.display:
                cv2.putText(thresh, "Movement in MIDI: {}".format(gMidiChange), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.imshow("M2M Motion", thresh)

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

	time.sleep(0.1)
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
