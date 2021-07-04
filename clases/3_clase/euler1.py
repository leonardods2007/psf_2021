import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig        = plt.figure()
fs         = 20
N          = 20

circleAxe  = fig.add_subplot(1,1,1)
circleLn,  = plt.plot([],[],'ro-',linewidth          = 5)
radioLn,   = plt.plot([0,0],[0.5,0.5],'g-',linewidth = 10,alpha = 0.2)
circleData = []
circleAxe.grid(True)
circleAxe.set_xlim(-1,1)
circleAxe.set_ylim(-1,1)
circleFrec = 1

def circle(f,n):
    return np.exp(-1j*2*np.pi*f*n*1/fs)

def init():
    circleData = []
    return circleLn,radioLn

def update(n):
    circleData.append(circle(circleFrec,n))
    circleLn.set_data(np.real(circleData),np.imag(circleData))
    radioLn.set_data([0,np.real(circle(circleFrec,n))],[0,np.imag(circle(circleFrec,n))])
    return circleLn,radioLn

ani=FuncAnimation(fig,update,N,init,interval=1000 ,blit=False,repeat=True)
plt.show()
