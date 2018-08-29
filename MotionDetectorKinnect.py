#! /usr/bin/env python3
import time
import cv2
import freenect
import mido
import threading
import config
import numpy as np
import logging
from mido import Message

#logging.getLogger().setLevel(logging.DEBUG)

class MotionDetectorKinnect:
    gMidiTotal= 0
    gMidiUpper = 0
    gMidiLower = 0
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

    def get_ir(self):
        array,_ = freenect.sync_get_video(0, freenect.VIDEO_IR_10BIT)
        np.clip(array, 0, 2**10-1, array)
        array >>=2
        array = array.astype(np.uint8)
        return array

    def get_video(self):
        array,_ = freenect.sync_get_video()
        array = cv2.cvtColor(array,cv2.COLOR_RGB2GRAY)
        return array

    def get_depth(self):
        array,_ = freenect.sync_get_depth()
        array = array.astype(np.uint8)
        return array

    def calc_percent(self,  img):
        height, width = img.shape[:2]
        max = float(height*width / self.conf.C_AMPLIFIER)
        percent = int((cv2.countNonZero(img) / max) * 100)
        if percent < 100:
            return percent
        else:
            return 100

    def send_midi(self):
        logging.debug("Sending total:" + str(self.gMidiTotal) + " lower:" + str(self.gMidiLower) + " upper:" + str(self.gMidiUpper))
        if self.gMidiTotal != 0:
            cc = Message('control_change', channel=0, control=1, value=int(self.gMidiTotal))
            self.out_port.send(cc)
            
        if self.gMidiLower != 0:
            cc = Message('control_change', channel=1, control=1, value=int(self.gMidiLower))
            self.low_port.send(cc)
        
        if self.gMidiUpper != 0:
            cc = Message('control_change', channel=2, control=1, value=int(self.gMidiUpper))
            self.up_port.send(cc)

    def video_thread(self):
        # open midi port
        self.out_port = mido.open_output('Full frame', client_name='Motion Detector')# (Full)')
        self.low_port = mido.open_output('Lower frame', client_name='Motion Detector')# (Lower)')
        self.up_port = mido.open_output('Upper frame', client_name='Motion Detector')# (Upper"')
        logging.info('Output port: {}'.format(self.out_port))
        
        if self.conf.C_DISPLAY_VIDEO == 1:
            cv2.namedWindow("M2M Motion", cv2.WINDOW_NORMAL)
    
        # initialize the first frame in the video stream
        previousFrame = None
        frame = None
        
        # loop over the frames of the video
        while self.gRun:
            # save the previous frame and grab a new
            previousFrame = frame
            
            frame = self.get_video()
            
            frame = cv2.GaussianBlur(frame, (7, 7), 0)
            # skip diff if this was the first frame
            if previousFrame is None:
                continue

            # compute the absolute difference between the current frame and
            # previous frame
            frameDelta = cv2.absdiff(previousFrame, frame)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
            # dilate the thresholded image to fill in holes, then find contours
            # on thresholded image
            thresh = cv2.dilate(thresh, None, iterations=2)

            # split in two
            height, width = thresh.shape[:2]
            start_col = int(0)
            end_col = int(width)
            start_row = int(0)
            end_row = int(height * 0.5)
            upper = thresh[start_row:end_row, start_col:end_col]
            #cv2.imshow("Upper", upper)
            
            start_row = int(height * 0.5)
            end_row = int(height)
            lower = thresh[start_row:end_row, start_col:end_col]
            #cv2.imshow("Lower", lower)
            
            percent = self.calc_percent(thresh)
            lowerPercent = self.calc_percent(lower)
            upperPercent = self.calc_percent(upper)
            
            # calucate the amount of change and make it into a MIDI (0-127)     
            self.gMidiTotal = int(percent * 1.27)
            self.gMidiLower = int(lowerPercent * 1.27)
            self.gMidiUpper = int(upperPercent * 1.27)

            # send a MIDI message based on timing
            if self.conf.C_TRIGGER_BY_TIMING == 1:
                if self.gSync == 0:
                    self.gSync = self.conf.C_VIDEO_FPS / self.conf.C_MIDI_MPS
                    self.send_midi()
                else:
                    self.gSync = self.gSync -1

            # show display if needed
            if self.conf.C_DISPLAY_VIDEO == 1:
                cv2.putText(thresh, 
                    "Total percent: " + str(percent), 
                    (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.putText(thresh,  
                    "Lower percent: " + str(lowerPercent), 
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.putText(thresh,  
                    "Upper percent: " + str(upperPercent), 
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.imshow("M2M Motion", thresh)
    
            # check for keyboard input  
            cv2.waitKey(1) & 0xFF

            ms = 1000 / self.conf.C_VIDEO_FPS
            time.sleep(ms / 1000.0) # 1000.0 because we want a float
 
        # cleanup the camera and close any open windows
        cv2.destroyAllWindows()
        logging.info("Leaving Video thread.")

        
    def heartbeat_thread(self):
        in_port = mido.open_input('Heartbeat', client_name='Motion Detector')
        logging.info("Incoming port: {}".format(in_port))

        global gMidiTotal
        
        while self.gRun:
            for msg in in_port.iter_pending():
                if self.conf.C_TRIGGER_BY_HEARTBEAT == 0:
                    continue
                self.send_midi()
            time.sleep(0.1)
        logging.info("Leaving Heartbeat thread.")

