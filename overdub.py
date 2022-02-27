import pyaudio
import numpy as np

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

CLIPLENGTH = 650
#length in buffers of audio loop

LATENCY = -12
#this variable corrects for latency in overdubbing
#it is added to buffer index during write audio buffer to audio buffer array

isrecording = True

silence = np.zeros(CHUNK, dtype = np.int16)
#buffer containing silence for period between clicks during count-in
click = np.zeros(CHUNK, dtype = np.int16)
for i in range(CHUNK):
    click[i] = 100 * (i % 10)
#buffer click now contains a sawtooth wave. RHS of modulo controls frequency
metronome_clicktime = CLIPLENGTH / 16
#no of buffers i.e. time, between metronome clicks
metronome_beeplength = 5
#length in buffers of actual beeps during countdown

mix_ratio = 1;
#initializing overdub attenuation factor

pa = pyaudio.PyAudio()

class audioclip:
    
    def __init__(self):
        self.audio = np.zeros([CLIPLENGTH, CHUNK], dtype = np.int16)
        self.readp = 0
        self.writep = (CLIPLENGTH + LATENCY) % CLIPLENGTH

    def is_restarting(self):
        if (self.readp == 0):
            return True
        else:
            return False
        
    def incw(self):
        self.writep = ((self.writep + 1) % CLIPLENGTH)
        
    def incr(self):
        self.readp = ((self.readp + 1) % CLIPLENGTH)
        
    def write(self, data):
        self.audio[self.writep, :] = np.frombuffer(data, dtype = np.int16)
        self.incw()

    def read(self):
        tmp = self.readp
        self.incr()
        return(self.audio[tmp, :])

    def dub(self, data):
        datadump = np.frombuffer(data, dtype = np.int16)
        for i in range(CHUNK):
            self.audio[self.writep, i] = self.audio[self.writep, i] * 0.9 + datadump[i] * mix_ratio
        self.incw()    

clip1 = audioclip()
#main audio loop
        

def loop_callback(in_data, frame_count, time_info, status):
    global mix_ratio
    global clip1
    global isrecording
                                                              
    if (clip1.is_restarting()):
        clip1.writep = (CLIPLENGTH + LATENCY) % CLIPLENGTH   #reset latency
        mix_ratio = mix_ratio * 0.9                          #nth overdub is mixed with loop at 0.9**n : 0.9 ratio

    
    if isrecording:
        clip1.dub(in_data)
    return(clip1.read(), pyaudio.paContinue)

click_stream = pa.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=False,
    output=True,
    frames_per_buffer = CHUNK
)

loop_stream = pa.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer = CHUNK,
    stream_callback = loop_callback
)

for i in range(CLIPLENGTH):
    if (i % metronome_clicktime < metronome_beeplength):
        click_stream.write(click, CHUNK)
    else:
        click_stream.write(silence, CHUNK)

loop_stream.start_stream()

while True:
    input('OVERDUB...')
    isrecording = False
    input('PLAY...')
    isrecording = True
    
loop_stream.stop_stream()
loop_stream.close()

pa.terminate()