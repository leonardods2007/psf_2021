import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig        = plt.figure()
fs         = 10
N          = 10
#--------------------------------------
circleAxe  = fig.add_subplot(2,2,1)
circleLn,promLn  = plt.plot([],[],'r-',[],[],'bo')
circleAxe.grid(True)
circleAxe.set_xlim(-2,2)
circleAxe.set_ylim(-2,2)
circleFrec = 0
circleLn.set_label(circleFrec)
circleLg   = circleAxe.legend()
circleData = []
prom       = 0
frecIter   = 0
circle     = lambda c,f,n: c*np.exp(-1j*2*np.pi*f*n*1/fs)
#--------------------------------------
signalAxe  = fig.add_subplot(2,2,2)
signalLn,  = plt.plot([],[],'b-')
signalAxe.grid(True)
signalAxe.set_xlim(0,N/fs)
signalAxe.set_ylim(-1,1)
signalFrec = 2
signalData=[]
signal  = lambda f,n: np.cos(2*np.pi*f*n*1/fs)
#--------------------------------------
fourierAxe  = fig.add_subplot(2,2,3)
fourierLn,  = plt.plot([],[],'g-o')
fourierAxe.grid(True)
fourierAxe.set_xlim(0,fs)
fourierAxe.set_ylim(0,1)
fourierData=[]
#--------------------------------------
dftn=np.linspace(0,N,N)
dftData=np.abs(np.fft.fft(signal(signalFrec,dftn)/N))**2
dftf=np.linspace(0,fs,N,endpoint=False)
dftAxe  = fig.add_subplot(2,2,4)
dftLn,  = plt.plot(dftf,dftData,'g-o')
dftAxe.grid(True)
dftAxe.set_xlim(0,fs)
dftAxe.set_ylim(0,1)
#--------------------------------------
tData=[]
fData=[]

def init():
    return circleLn,
def update(n):
    global circleData,signalData,tData,promData,frecIter,circleFrec,fourierData,fData,circleLg
    circleData.append(circle(1,circleFrec,n)*signal(signalFrec,n))
    prom=np.average(circleData)
    promLn.set_data(np.real(prom),
                    np.imag(prom))
    circleLn.set_data(np.real(circleData),
                      np.imag(circleData))
    signalData.append(signal(signalFrec,n))
    tData.append(n/fs)
    signalLn.set_data(tData,signalData)

    if n==N-1:
        circleData = []
        signalData = []
        tData      = []
        fourierData.append(np.real(prom)**2)
        fData.append(circleFrec)
        fourierLn.set_data(fData,fourierData)
        prom       = 0
        frecIter+=1
        if frecIter == N:
            ani.repeat=False
        else:
            circleFrec = frecIter*fs/N
            circleLn.set_label(circleFrec)
            circleLg=circleAxe.legend()
    return circleLn,circleLg,signalLn,promLn,fourierLn

ani=FuncAnimation(fig,update,N,init,interval=100 ,blit=True,repeat=True)
plt.show()
