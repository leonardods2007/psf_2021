import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig        = plt.figure()
fs         = 20
N          = 20
#--------------------------------------
circleAxe = fig.add_subplot(2,2,1)
circleLn, = plt.plot([] ,[] ,'ro-' ,linewidth = 2)
radioLn,  = plt.plot([0 ,0] ,[0.5 ,0.5] ,'g-' ,linewidth = 3 ,alpha = 0.2)
massLn,   = plt.plot([] ,[] ,'bX' ,linewidth = 1 ,alpha = 1)

circleAxe.grid(True)
circleAxe.set_xlim(-2,2)
circleAxe.set_ylim(-2,2)
circleFrec = -1
circleLn.set_label(0)
circleLg   = circleAxe.legend()
circleData = []
mass       = 0
def circle(f,n):
    return np.exp(-1j*2*np.pi*f*n*1/fs)
#--------------------------------------
signalAxe  = fig.add_subplot(2,2,2)
signalLn,  = plt.plot([],[],'b-o')
signalAxe.grid(True)
signalAxe.set_xlim(0,N/fs)
signalAxe.set_ylim(-1,1)
signalFrec = 2
signalData=[]
def signal(f,n):
    return np.cos(2*np.pi*f*n*1/fs)
#--------------------------------------
tData=np.arange(0,N/fs,1/fs)

def init():
    global circleData,signalData,radioLn,circleFrec
    circleData = []
    signalData = []
    circleFrec+=1
    if(circleFrec>=(fs-1)):
        ani.repeat=False
    return circleLn,circleLg,signalLn,massLn,radioLn,

def update(n):
    global circleData,signalData,radioLn,circleFrec
    circleData.append(circle(circleFrec,n)*signal(signalFrec,n))
    mass=np.average(circleData)
    massLn.set_data(np.real(mass),
                    np.imag(mass))
    circleLn.set_data(np.real(circleData),
                      np.imag(circleData))
    radioLn.set_data([0,10*np.real(circle(circleFrec,n))],[0,10*np.imag(circle(circleFrec,n))])
    signalData.append(signal(signalFrec,n))
    signalLn.set_data(tData[:n+1],signalData)

    circleLn.set_label(circleFrec)
    circleLg=circleAxe.legend()
    return circleLn,circleLg,signalLn,massLn,radioLn

ani=FuncAnimation(fig,update,N,init,interval=1 ,blit=False,repeat=True)
plt.get_current_fig_manager().window.showMaximized()
plt.show()
