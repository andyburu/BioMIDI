#! /usr/bin/env python3
import imutils
import time
import cv2
import mido
import threading
import config
import logging
from mido import Message

class MotionDetectorWebcam:
    gHighestSeenChange = 1
    gMidiChange = 0
    gSync = 0
    gRun = True
    
    # use default value before setConfig has been called 
    conf = config.Config()
    
    def start(self,  conf):
        self.conf = conf
    
        threading.Thread(target=self.heartbeat_thread).start()
        threading.Thread(target=self.video_thread).start()
    
    def __init__(self): 
        #use JACK
        mido.set_backend('mido.backends.rtmidi/UNIX_JACK')
        
        return

    def die(self):
        self.gRun = False

    def video_thread(self):
        # open midi port
        self.out_port = mido.open_output('Output', client_name='Motion Detector (OUT)')
        logging.info('Output port: {}'.format(self.out_port))
        
        camera = cv2.VideoCapture(0)
        time.sleep(0.25)
        
        if self.conf.C_DISPLAY_VIDEO == 1:
            cv2.namedWindow("M2M Motion", cv2.WINDOW_NORMAL)
    
        # initialize the first frame in the video stream
        previousFrame = None
        gray = None

        # loop over the frames of the video
        while self.gRun:
            (grabbed, frame) = camera.read()
 
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
            if currentChange >= self.gHighestSeenChange:
                self.gHighestSeenChange = currentChange

            # calucate the amount of change and make it into a MIDI (0-127)     
            percent = float(currentChange) / float(self.gHighestSeenChange)
            self.gMidiChange = int(percent * 127)

            # send a MIDI message based on timing
            if self.conf.C_TRIGGER_BY_TIMING == 1:
                if self.gSync == 0:
                    self.gSync = self.conf.C_VIDEO_FPS / self.conf.C_MIDI_MPS
                    logging.debug("Sending " + str(self.gMidiChange))
                    cc = Message('control_change', channel=13, control=1, value=int(self.gMidiChange))
                    self.out_port.send(cc)
                else:
                    self.gSync = self.gSync -1

            # slowly readjust the highest found 
            if self.conf.C_READJUST_AMOUNT != 0 and self.gHighestSeenChange >= int(self.conf.C_READJUST_AMOUNT):
                self.gHighestSeenChange = self.gHighestSeenChange - self.conf.C_READJUST_AMOUNT

            # show display if needed
            if self.conf.C_DISPLAY_VIDEO == 1:
                cv2.putText(thresh, "Movement in MIDI: {}".format(self.gMidiChange), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.imshow("M2M Motion", thresh)

    
            # check for keyboard input  
            cv2.waitKey(1) & 0xFF

            ms = 1000 / self.conf.C_VIDEO_FPS
            time.sleep(ms / 1000.0) # 1000.0 because we want a float
 
        # cleanup the camera and close any open windows
        camera.release()
        cv2.destroyAllWindows()
        logging.info("Leaving Video thread.")

        
    def heartbeat_thread(self):
        in_port = mido.open_input('Heartbeat', client_name='Motion Detector (HB)')
        logging.info("Incoming port: {}".format(in_port))

        global gMidiChange
        
        while self.gRun:
            for msg in in_port.iter_pending():
                if self.conf.C_TRIGGER_BY_HEARTBEAT == 0:
                    continue
                
                logging.debug("[HB] Sending " + str(self.gMidiChange))
                cc = Message('control_change', channel=13, control=1, value=int(self.gMidiChange))
                self.out_port.send(cc)
                
            time.sleep(0.1)
        logging.info("Leaving Heartbeat thread.")

