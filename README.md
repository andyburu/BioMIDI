# BioMIDI

This a project that sends data from various biometrical sensors as MIDI commands. The goal is to build a soundscape based on the human body.

## TODO
1. Add more scales to Scalezor
2. Let motion2MIDI splitt the screen and send multiple CC messages
3. Experiment with picking notes from cool note progressions
4. Add somekind of semi random effect changes, so keep the interest for longer periods of time
5. Make proper python naming of files, classes and packages
 
## DONE
1. Let the motion dector take a MIDI input singal from the heart beat to synchronize
2. Break out the Note-on-a-Scale selector from Motion dector
3. Add support for having multiple notes running at the same time
4. Add support for NMS protocol
5. Clean up threading
6. Add support for Kinnect

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

