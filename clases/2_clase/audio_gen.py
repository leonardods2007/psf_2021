import numpy as np
import scipy.signal as sc
import simpleaudio as sa
import matplotlib.pyplot as plt

f   = 1300
fs  = 44100
sec = 20
B   = 600
t   = np.arange ( 0,sec,1/fs )
note = (2**15-1)*np.sin(2 * np.pi * f * t) #sin
#note = (2**15-1)*sc.sawtooth(2*np.pi*f*t,0) #saw
#note = (2**15-1)*np.sin(2 * np.pi * B*t/sec * t)  #sweept

audio = note.astype(np.int16)
for i in range(1000):
    print(i)
    play_obj = sa.play_buffer(audio, 1, 2, fs)
    play_obj.wait_done()

