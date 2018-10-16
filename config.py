class Config:
    C_DISPLAY_VIDEO = 0
    C_TRIGGER_BY_HEARTBEAT = 1
    C_TRIGGER_BY_TIMING = 1
    C_VIDEO_FPS = 30
    C_MIDI_MPS = 5
    C_AMPLIFIER = 1
    C_OCTAVE_OFFSET = 1
    C_CURRENT_SCALE = 0
    C_HB_DRAMATIC = 1
    C_HB_NORMAL = 80
    C_FB_FACTOR = 1
    C_FB_STYLE = 0
    C_FB_FILTER = 10
    C_FB_MIN = 1
    C_MD_CHANNEL = 31
    C_MD_WAIT = 1
    C_MD_MOD = 100
    
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
            " C_CURRENT_SCALE=" + str(self.C_CURRENT_SCALE) +
            " C_HB_DRAMATIC=" + str(self.C_HB_DRAMATIC) + 
            " C_HB_NORMAL=" + str(self.C_HB_NORMAL) +
            " C_FB_STYLE=" + str(self.C_FB_STYLE) +
            " C_FB_FACTOR=" + str(self.C_FB_FACTOR) +
            " C_FB_FILTER=" + str(self.C_FB_FILTER) +
            " C_FB_MIN=" + str(self.C_FB_MIN) +
            " C_MD_WAIT=" + str(self.C_MD_WAIT) + 
            " C_MD_CHANNEL=" + str(self.C_MD_CHANNEL) + 
            " C_MD_MOD=" + str(self.C_MD_MOD)
            )
