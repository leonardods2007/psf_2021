import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


frecCircle=0
fig = plt.figure()
frec2=3


xfft, yfft               = [], []
xmass, ymass             = [1], [1]
xCircle, yCircle         = [0,0,0], [0,0,0]
xdata, ydata             = [], []
signalXdata, signalYdata = [], []
ax2=fig.add_subplot(2,2,2)
ln2,=plt.plot([],[],'b-')
ax2.grid(True)
ax1=fig.add_subplot(2,2,1)
ln1,ln3,ln4 =plt.plot([],[],'r-',[],[],'b-o',[],[],'go')
ax1.grid(True)
ax3=fig.add_subplot(2,2,3)
fft, =plt.plot([],[],'bo-')
ax3.grid(True)

def init():
    ax1.set_xlim(-2, 2)
    ax1.set_ylim(-2, 2)
    ax2.set_xlim(0, 10)
    ax2.set_ylim(-2, 2)
    ax3.set_xlim(-0.1, 30)
    ax3.set_ylim(-0.25, 1)
    return ln1,ln2,ln3,ln4,fft


def signal(t):
        return 1+np.cos (frec2*2*np.pi*t)+np.sin(frec2*3*np.pi*t)
def circleX(t):
    return np.cos(-frecCircle*2*np.pi*t)
def circleY(t):
    return np.sin(-frecCircle*2*np.pi*t)

def update(t):
    global frecCircle,xdata,ydata,signalXdata,signalYdata
    xdata.append(circleX(t)*signal(t))
    ydata.append(circleY(t)*signal(t))
    signalXdata.append(t)
    signalYdata.append(signal(t))
    xCircle[1]=circleX(t)*signal(t)
    yCircle[1]=circleY(t)*signal(t)
    xCircle[2]=5*circleX(t)
    yCircle[2]=5*circleY(t)

    xmass[0]=np.average(xdata)
    ymass[0]=np.average(ydata)

    if (t >= 2):
        xfft.append(frecCircle)
        yfft.append(xmass[0])
        #yfft.append(math.sqrt(xmass[0]**2+ymass[0]**2))
        frecCircle=frecCircle+0.1
        xdata=[0]
        ydata=[0]
        signalXdata=[0]
        signalYdata=[0]
    ln1.set_data(xdata,ydata)
    ln2.set_data(signalXdata,signalYdata)
    ln3.set_data(xCircle,yCircle)
    ln4.set_data(xmass,ymass)
    fft.set_data(xfft,yfft)
    return ln1,ln2,ln3,ln4,fft

def updateFft(f):
    global frecCircle,xdata,ydata,signalXdata,signalYdata
    frecCircle=f
    xdata=circleX(t)*signal(t)
    ydata=circleY(t)*signal(t)
    signalXdata=t
    signalYdata=signal(t)

    xmass[0]=np.average(xdata)
    ymass[0]=np.average(ydata)

    xfft.append(frecCircle)
    yfft.append(xmass[0])

    ln1.set_data(xdata,ydata)
    ln2.set_data(signalXdata,signalYdata)
    ln3.set_data(xCircle,yCircle)
    ln4.set_data(xmass,ymass)
    fft.set_data(xfft,yfft)
    return ln1,ln2,ln3,ln4,fft

t   = np.linspace(0, 2, 40,endpoint=False)
print (t)
f   = np.linspace(0, 200, 1000)

#ani = FuncAnimation(fig, update, t, init_func=init, blit=True, interval=10, repeat=True)
ani = FuncAnimation(fig, updateFft, f, init_func=init, blit=True, interval=100, repeat=True)
plt.show()

