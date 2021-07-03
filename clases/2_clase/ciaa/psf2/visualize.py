#!python3
import numpy as np
import matplotlib.pyplot as plt
from   matplotlib.animation import FuncAnimation
import os
import io
import serial

SERIAL_PORT="/dev/ttyUSB2"
header = { "mark": b"*header*", "id": 0, "N": 128, "fs": 10000 }
fig    = plt.figure      ( 1          )

adcAxe = fig.add_subplot ( 2,1,1       )
adcLn, = plt.plot        ( [],[],'r-',linewidth=4  )
adcAxe.grid              ( True        )
adcAxe.set_ylim          ( -1.65 ,1.65 )

fftAxe = fig.add_subplot ( 2,1,2      )
fftLn, = plt.plot        ( [],[],'b-',linewidth=4 )
fftAxe.grid              ( True       )
fftAxe.set_ylim          ( 0 ,0.25 )

def findHeader(f,h):
    index = 0
    sync  = False
    while sync==False:
        data=b''
        while len(data) <1:
            data = f.read(1)
        logFile.write(data)
        if data[0]==h["mark"][index]:
            index+=1
            if index>=len(h["mark"]):
                sync=True
        else:
            index=0
    h["id"] = readInt4File(f,4)
    h["N" ] = readInt4File(f)
    h["fs"] = readInt4File(f)
    print(h)
    return h["id"],h["N"],h["fs"]


def readInt4File(f,size=2,sign=False):
    raw=b''
    while(len(raw)<size):
        data=f.read(1)
        raw+=data
        logFile.write(data)
    return (int.from_bytes(raw,"little",signed=sign))

def findThresh(f,th,h):
    state=1
    sample=0
    for chunk in range(h["N"]):
        sample=readInt4File(f,sign=True)
        if(state==1):
            if(sample<th):
                state=2
        else:
            if(state==2):
                if(sample>=th):
                    return chunk+1,sample
    return N,sample
                
def flushStram(f,h):
    if(f.name): #pregunto si estoy usando la bibioteca pyserial o un file
        f.flushInput()
    else:
        f.seek ( 2*h["N"],io.SEEK_END)

def update(t):
    global header
    flushStram ( streamFile,header )
    id,N,fs=findHeader ( streamFile,header )
    adc   = np.ndarray(N)
    time  = np.ndarray(N)
    index = 0
    t     = 0
    #index,sample=findThresh(streamFile,0,header)
    for chunk in range(N-index):
        sample   = readInt4File(streamFile,sign = True)
        adc[t]   = sample/512*1.65
        time[t]  = t/fs
        t       += 1

    adcAxe.set_xlim ( 0    ,N/fs )
    adcLn.set_data  ( time ,adc  )

    fft=np.abs ( 1/N*np.fft.fft(adc ))**2
    fftAxe.set_ylim ( 0 ,np.max(fft)+0.05)
    fftAxe.set_xlim ( 0                ,fs/8 )
    fftLn.set_data ( (fs/N )*fs*time ,fft)
    return adcLn, fftLn

#seleccionar si usar la biblioteca pyserial o leer desde un archivo log.bin
#streamFile=open("log.bin","rb",0)
streamFile = serial.Serial(port=SERIAL_PORT,baudrate=460800,timeout=None)

logFile=open("log.bin","wb",0)

ani=FuncAnimation(fig,update,1000,init_func=None,blit=False,interval=1,repeat=True)
plt.draw()
#mng=plt.get_current_fig_manager()
#mng.resize(mng.window.maxsize())
plt.get_current_fig_manager().window.showMaximized() #para QT5
plt.show()
streamFile.close()
logFile.close()
