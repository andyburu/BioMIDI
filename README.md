# BioMIDI

This a project that sends data from various biometrical sensors as MIDI commands. The goal is to build a soundscape based on the human body.

## TODO
1. Add more scales to Scalezor
2. Make proper python naming of files, classes and packages
3. Add a dramatic curve module, that can modulate MIDI signals over time.
 
## DONE
1. Let the motion dector take a MIDI input singal from the heart beat to synchronize
2. Break out the Note-on-a-Scale selector from Motion dector
3. Add support for having multiple notes running at the same time
4. Add support for NMS protocol
5. Clean up threading
6. Add support for Kinnect
7. Let motion2MIDI splitt the screen and send multiple CC messages
8. Add GUI for heartbeat monitor that shows connection status and allows for modulation
9. Aded FadeBack that connect to the motion detector, and sends gradually decreasing CCs, to let motions fade out.

## PROTOTYPES and their STATUS
1. Use object tracking instead of motion detection. Status: Tracking dancing bodies is too unstable and CPU heavy.
2. Use the Kinnect depth sensor for motion detection in a pitch black room. Status: Works, but Kinnect can't see futher than four meters. Need to experiment with the camera placement. Maybe in the roof?
3. Add analog input via contact microphones. Status: Tested two setups, either modulating the analog singal using loopers, or converting the analog to CC and notes. However this seams to be outside this project.

## ROADMAP
1. Add four channel mixing
2. Add DMX light protocol
3. Run on a stand-alone machine

## DEPENDENCICES
1. *python3*
2. *liblo* for Open Sound Protocol, used by Non-Session-Manager via pip3
3. *mido* for MIDI, via pip3
4. *bluepy* for Bluetooth, via pip3
5. *cv2* for video manipulation, via pip3
6. *freenect1* for Kinnect 360, via git https://github.com/OpenKinect/libfreenect/
7. *numpy* for calculations, via pip3
8. *tkinter* for GUI drawing, via pip3
9. *rtmidi* for MIDI backend, via apt package python3-rtmidi


