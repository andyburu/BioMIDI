class Config:
    C_DISPLAY_VIDEO = 0
    C_TRIGGER_BY_HEARTBEAT = 1
    C_TRIGGER_BY_TIMING = 1
    C_VIDEO_FPS = 30
    C_MIDI_MPS = 5
    C_AMPLIFIER = 1
    C_OCTAVE_OFFSET = 1
    C_CURRENT_SCALE = 0
    
    def __init__(self):
        print("Created config instance.")
        
    def prettyPrint(self):
        print("C_DISPLAY_VIDEO=" + str(self.C_DISPLAY_VIDEO) + 
            " C_TRIGGER_BY_HEARTBEAT=" + str(self.C_TRIGGER_BY_HEARTBEAT) +
            " C_TRIGGER_BY_TIMING=" + str(self.C_TRIGGER_BY_TIMING) +
            " C_VIDEO_FPS=" + str(self.C_VIDEO_FPS) + 
            " C_MIDI_MPS=" + str(self.C_MIDI_MPS) + 
            " C_AMPLIFIER=" + str(self.C_AMPLIFIER) +
            " C_OCTAVE_OFFSET=" + str(self.C_OCTAVE_OFFSET) +
            " C_CURRENT_SCALE=" + str(self.C_CURRENT_SCALE)
            )
