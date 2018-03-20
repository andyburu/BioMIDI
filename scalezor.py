import argparse
import time
import mido
import sys
import threading
from mido import Message

# globals
global args 

SCALE_PENTATONIC_ONE = [ 0, 2, 4, 7, 9 ]
SCALE_PENTATONIC_TWO = [ 0, 2, 4, 7, 9, 12, 14, 16, 19, 21 ]
SCALE_PENTATONIC_THREE = [ 0, 2, 4, 7, 9, 12, 14, 16, 19, 21, 24, 26, 28, 31, 33 ] 
OCTAVE = 3 * 12 
SCALE = SCALE_PENTATONIC_THREE

# pick a note from a scale
def midi_to_note_on_scale(midi):
	scale_pos = midi / (127 / len(SCALE))
	if len(SCALE) == scale_pos: scale_pos = scale_pos-1

	return SCALE[scale_pos] + (OCTAVE)

def send_midi_message(midi):
	# select note
        note = midi_to_note_on_scale(midi)

        # turn on note
        on = Message('note_on', channel=13, note=note, velocity=int(midi))
        out_port.send(on)

        # note lenght is either dynamic or static
        if args.time:
       		 ms = args.time
        else:
                 ms = 10000 / midi;

        # log and sleep
        if args.verbose: print("lenght:" + str(ms) + "ms velocity:" + str(midi) + " note:" + str(note) + " thread:" + str(threading.currentThread().getName()))
     	time.sleep(ms / 1000.0)

        # turn off note
        off = Message('note_off', channel=13, note=note, velocity=int(midi))
        out_port.send(off)


# main thread
def scalezor_start():
	lastMidi = 0
	global out_port
	
	#use JACK
	mido.set_backend('mido.backends.rtmidi/UNIX_JACK')

	# open midi port
	out_port = mido.open_output('Output', client_name='Scalezor')
	print("Outgoing port: {}".format(out_port))

	in_port = mido.open_input('Input', client_name='Scalezor')
	print("Incoming port: {}".format(in_port))
	
	for msg in in_port:
		midi = msg.value

               	if midi == lastMidi or midi == 0:
			continue
		
#		send_midi_message(midi)
		threading.Thread(target=send_midi_message, args=(midi, )).start()

                lastMidi = midi	
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--verbose", help="spam trace message", action="store_true")
ap.add_argument("-t", "--time", help="time between note is fixed to this.", type=int)
args = ap.parse_args()

# start scalezor
scalezor_start()


