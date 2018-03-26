# BioMIDI

This a project that sends data from various biometrical sensors as MIDI commands. The goal is to build a soundscape based on the human body.

## TODO
1. Add support for NMS protcol
2. Clean up threading, so everything terminates cleanly
3. Add more scales to Scalezor
4. Add support for Kinect
5. Let motion2MIDI splitt the screen and send multiple CC messages
6. Experiment with picking notes from cool note progressions
7. Add somekind of semi random effect changes, so keep the interest for longer periods of time
 
## DONE
1. Let the motion dector take a MIDI input singal from the heart beat to synchronize
2. Break out the Note-on-a-Scale selector from Motion dector
3. Add support for having multiple notes running at the same time

## ROADMAP
1. Add four channel mixing
2. Add DMX light protocol
3. Run on a stand-alone machine
