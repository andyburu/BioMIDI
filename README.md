# BioMIDI

This a project that sends data from various biometrical sensors as MIDI commands. The goal is to build a soundscape based on the human body.

## TODO
1. Add note sender to the motion tracker that corresponds to stillness
2. Create a sound for stillness
3. Add support for two physical vibration microphones
4. Add more scales to Scalezor
5. Experiment with picking notes from cool note progressions
6. Add somekind of semi random effect changes, so keep the interest for longer periods of time
7. Make proper python naming of files, classes and packages
 
## DONE
1. Let the motion dector take a MIDI input singal from the heart beat to synchronize
2. Break out the Note-on-a-Scale selector from Motion dector
3. Add support for having multiple notes running at the same time
4. Add support for NMS protocol
5. Clean up threading
6. Add support for Kinnect
7. Let motion2MIDI splitt the screen and send multiple CC messages
8. Add GUI for heartbeat monitor that shows connection status and allows for modulation

## PROTOTYPES and their STATUS
1. Use object tracking instead of motion detection. Status: Tracking dancing bodies is too unstable and CPU heavy.
2. Use the Kinnect depth sensor for motion detection in a pitch black room. Status: Works, but Kinnect can't see futher than four meters. Need to experiment with the camera placement. Maybe in the roof?

## ROADMAP
1. Add four channel mixing
2. Add DMX light protocol
3. Run on a stand-alone machine

## DEPENDENCICES
1. *python3*
2. *liblo* for Open Sound Protocol, used by Non-Session-Manager
3. *mido* for MIDI
4. *bluepy* for Bluetooth
5. *cv2* for video manipulation
6. *freenect1* for Kinnect 360
7. *numpy* for calculations
8. *tkinter* for GUI drawing


