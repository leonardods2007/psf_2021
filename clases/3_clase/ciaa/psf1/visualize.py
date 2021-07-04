import numpy as np
import matplotlib.pyplot as plt
from   matplotlib.animation import FuncAnimation
import os
import scipy.fftpack as sc
from   scipy.io.wavfile import write

fftLength          = 32
fig                = plt.figure()
time, dft, ciaaFft = [0,1],[0,1],[0,1]
ax1     = fig.add_subplot ( 2,1,1                 )
ln1,    = plt.plot        ( [0],[0],'r-'          )
ax2     = fig.add_subplot ( 2,2,3                 )
ln2,    = plt.step        ( [],[],'b-o'            )
ax3     = fig.add_subplot ( 2,2,4                 )
ln3,ln4 = plt.step        ( [0],[0],'g-o',0,0,'bo' )
ax1.grid(True)
ax2.grid(True)
ax3.grid(True)

maxIndex = 0
maxValue = 0

def initFiles():
    global logFile
    last      = 1000
    logFile   = open("log.bin","rb")
    logFile.seek(0, os.SEEK_END)

def fileForward(f):
    packetLegth=((4*fftLength)+0+len(b'header')+2)
    oldPos = f.tell()
    f.seek(0, os.SEEK_END)
    size = f.tell()
    f.seek(oldPos+((size-oldPos)//packetLegth)*packetLegth, os.SEEK_SET)

def findHeader(f):
    index  = 0
    sync   = False
    header = b'header'
    while sync==False:
        data=b''
        while len(data) <1:
            data = f.read(1)
        if data[0] ==header[index]:
            index+=1
            if index>=len(header):
                sync=True
                print(sync)
        else:
            index=0
            print(sync)

def readInt4File(f):
    raw=b''
    while len(raw)<2:
        raw   += f.read(1)
    return (int.from_bytes(raw[0:2],"little",signed=True))

def readFile(f):
    fileForward(f)
    findHeader(f)
    fftLength= readInt4File(f)
    ciaaFft = []
    adc     = []
    for chunk in range(fftLength):
        adc.append     ( readInt4File(f )/(2**15))
        if(chunk%2==0):
            real = readInt4File(f )/2**15
        else:
            im   = readInt4File(f )*1j/2**15
            ciaaFft.append (real+im)
    maxValue = readInt4File(f)/2**15
    maxIndex = readInt4File(f)/2**15
    #maxValue = (np.abs(ciaaFft[maxIndex])**2)
    return maxIndex,maxValue,adc,ciaaFft,fftLength

def initAnimation():
    ax1.set_xlim ( 0,fftLength)
    ax2.set_xlim ( 0,10000/2)
    ax3.set_xlim ( 0,10000/2)
    ax1.set_ylim ( -1                    ,1 )
    ax2.set_ylim ( 0 , np.max(dft))
    ax3.set_ylim ( 0 , np.max(np.abs(ciaaFft)**2))
    plt.draw()
    return ln1,ln2,ln3,ln4

def update(t):
    global logFile,fftLength,time,dft,ciaaFft
    maxIndex,maxValue,adc,ciaaFft,fftLength=readFile(logFile)
    time    = [i for i in range(fftLength)]
    dft=(np.abs(np.fft.fft(adc))/len(adc))**2
    frec=np.linspace(0,10000/2,fftLength//2)

    ln1.set_data(time,adc)
    ln2.set_data(frec,dft[:fftLength//2])
    ln3.set_data(frec,np.abs(ciaaFft)**2)
    ln4.set_data(maxIndex,maxValue)
    return ln1,ln2,ln3,ln4


initFiles()
ani=FuncAnimation(fig, update, 30, init_func=initAnimation, blit=True, interval=20, repeat=True)
plt.show()

