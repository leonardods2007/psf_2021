import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

fsC = 300 #frec de sampleo que imita el 'continuo' cuando mas mejor
fsD = 30  #frec de sampleo discreta. Como el ejemplo es para una senial de 1hz, segun shanon no se podria recuperar si fsD es menor o igual a 2
N   = 50

t   = np.arange(0,N/fsC,1/fsC)

td  = np.arange(0,(N+1)/fsC,1/fsD) #un poquito mas largo para evitar erl redondeo
nd  = 0
s1  = np.zeros(len(td))
s2  = np.zeros(len(t))
s3  = np.zeros(len(t))
s4  = np.zeros(len(t))

fig    = plt.figure()
fftAxe = fig.add_subplot ( 2,1,2      )
fftLn, = plt.plot        ( [],[],'b-',linewidth=4 )
fftAxe.grid              ( True       )
fftAxe.set_ylim          ( 0 ,0.25 )

signal = fig.add_subplot(2,1,1)
signal.grid(True)

signal.set_xlim(0, np.max(t))
signal.set_ylim(0,10)

ln1, =plt.plot([],[],'ro',linewidth=8,alpha=0.8)
ln2, =plt.plot([],[],'b-')
ln3, =plt.plot([],[],'g-',linewidth=10,alpha=0.5)

signalF      = 1
signalFExtra = 40+35

def signal(n):
    return [5,2,8][int(n*fsD)%3] 
 #   return np.sin(2*np.pi*n*signalF) + 0.3 * np.sin(2*np.pi*n*signalFExtra)

def interpolate(timeC, x, B):
    y=[]
    for t in timeC:
        prom=0
        for n in range(len(x)):
           prom += x[n]*np.sinc(2*B*t-n)
        y.append(prom)
    #input("wait press")
    #print("n:",len(x),"t:",2*B*timeC,"y:",y)
    return y

def init():
    global nd,signal
    nd=0
    return ln1, ln2, ln3, fftLn

def update(n):
    global nd,signal
    s2[n]=signal(t[n]) #que pasa si agrego ruido
    ln2.set_data(t[:n],s2[:n])

    if(t[n]>=td[nd]):
        s1[nd] = signal(td[nd])                     #voy agregando a medida que el tiempo avanza
        sp     = s1[nd] * np.sinc(2*(fsD/2)*t)      #[:nd])#-td[nd]*2*fsD/2)
        sm     = s1[nd] * np.sinc(2*(fsD/2)*-t)      #[:nd])#-td[nd]*2*fsD/2)
        plt.plot(t+td[nd],sp,'y-',linewidth=5,alpha=0.2)
        plt.plot(td[nd]-t,sm,'y-',linewidth=5,alpha=0.2)
        if (nd+1)<len(td):
            nd+=1
        ln1.set_data(td[:nd],s1[:nd])
#
    s3=interpolate(t[:n],s1[:nd],fsD/2)
    ln3.set_data(t[0:len(s3)],s3)
##
#    fft=np.abs ( 1/N*np.fft.fft(s2 ))**2
#    fftAxe.set_ylim ( 0 ,np.max(fft)+0.01)
#    fftAxe.set_xlim ( 0 ,fsC/2 )
#    fftLn.set_data ( (fsC/N )*fsC*t ,fft)
    return ln1, ln2, ln3, fftLn


ani=FuncAnimation(fig,update,N,init_func=init,blit=False,interval=500,repeat=False)
#mng=plt.get_current_fig_manager()
#mng.resize(mng.window.maxsize())
plt.get_current_fig_manager().window.showMaximized() #para QT5
plt.show()

