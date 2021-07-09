import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig        = plt.figure(1)
fs         = 20
N          = 20

#--------------------------------------
circleAxe  = fig.add_subplot(2,2,1)
circleLn,massLn,  = plt.plot([],[],'r-',[],[],'bo')
circleAxe.grid(True)
circleAxe.set_xlim(-1,1)
circleAxe.set_ylim(-1,1)
circleFrec = np.arange(-fs/2,fs/2,fs/N)
circleLn.set_label(circleFrec[0])
circleLg=circleAxe.legend()
circleData = []
mass       = 0
def circle(f,n):
    return   np.exp(-1j*2*np.pi*f*n*1/fs)

def circleInv(f,n,c):
    return c*np.exp( 1j*2*np.pi*f*n*1/fs)
#--------------------------------------
signalAxe  = fig.add_subplot(2,2,2)
signalRLn,  = plt.plot([],[],'b-o',linewidth=3,alpha=0.6)
signalILn,  = plt.plot([],[],'r-o',linewidth=3,alpha=0.6)
signalAxe.grid(True)
signalAxe.set_xlim(0,N/fs)
signalAxe.set_ylim(-1,1)
signalFrec = 1
signalData=[]

def signal(f,n):
    return np.cos(2*np.pi*f*n*1/fs)#+0.2j*np.sin(4*np.pi*f*n*1/fs)
#--------------------------------------
promAxe  = fig.add_subplot(2,2,3)
promRLn,promILn,  = plt.plot([],[],'g-o',[],[],'y-o')
promAxe.grid(True)
promAxe.set_xlim(-fs/2,fs/2)
promAxe.set_ylim(-1,1)
promData=np.zeros(N,dtype=complex)
#--------------------------------------
inversaAxe = fig.add_subplot(2,2,4)
inversaLn, = plt.plot([],[],'m-o')
penLn,     = plt.plot([],[],'k-',linewidth=10,alpha=0.2)
penRLn,    = plt.plot([],[],'b-')
penILn,    = plt.plot([],[],'r-')
inversaAxe.grid(True)
inversaAxe.set_xlim(-1,1)
inversaAxe.set_ylim(-1,1)
penData= []
#--------------------------------------
tData=np.arange(0,N/fs,1/fs)
signalsIter=0

def init():
    return circleLn,circleLg,signalRLn,signalILn,massLn,promRLn,promILn,inversaLn

s=[]
for f in range(N):
    s.append(np.zeros(N))

def updateF(frecIter):
    global promData,fData,penData
    inversaData=[0]
    for f in range(N):
        inversaData.append(inversaData[-1]+circleInv(circleFrec[f],frecIter,promData[f]))
    inversaLn.set_data(np.imag(inversaData),np.real(inversaData))
    penData.insert(0,inversaData[-1])
    penData=penData[0:N]
    t=np.linspace(0,-1,len(penData))
    penRLn.set_data(t,np.real(penData))
    penILn.set_data(np.imag(penData),t)
    penLn.set_data(np.imag(penData),np.real(penData))
    return inversaLn,penLn,penILn,penRLn,circleLn,signalRLn,signalILn,promRLn,promILn,

def updateT(frecIter):
    global circleData,signalData,promData,circleFrec,circleLg,signalsIter

    circleData = []
    signalData = []
    for n in range(N):
        circleData.append(circle(circleFrec[frecIter],n)*signal(signalFrec,n))
        mass=np.average(circleData)
        signalData.append(signal(signalFrec,n))
        promData[frecIter]=mass
    massLn.set_data(np.real(mass),
                    np.imag(mass))
    circleLn.set_data(np.real(circleData),
                      np.imag(circleData))
    signalRLn.set_data(tData[:n+1],np.real(signalData))
    signalILn.set_data(tData[:n+1],np.imag(signalData))
    promRLn.set_data(circleFrec[:frecIter+1],np.real(promData[:frecIter+1]))
    promILn.set_data(circleFrec[:frecIter+1],np.imag(promData[:frecIter+1]))
    circleLn.set_label(circleFrec[frecIter])
    circleLg=circleAxe.legend()
    if frecIter==N-1:
        aniT._func=updateF
        aniT._interval=5
        signalsiter=0

    return circleLn,circleLg,signalRLn,signalILn,massLn,promRLn,promILn,

aniT=FuncAnimation(fig,updateT,N,init,interval=10 ,blit=False,repeat=True,cache_frame_data=False)
plt.get_current_fig_manager().window.showMaximized()
plt.show()
plt.close(1)
plt.close(2)
