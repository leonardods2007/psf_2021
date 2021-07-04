import numpy as np
from  matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

fig = plt.figure()
fs =100
N =100

circleAxe = fig.add_subplot(2,2,1)
circleLn,massLn = plt.plot([],[],'r-',[],[],'bo')
circleAxe.grid(True)
circleAxe.set_xlim(-1,1)
circleAxe.set_ylim(-1,1)
circleFrec=1.9
circleData=[]
circleLg=circleAxe.legend()
circleLn.set_label(0)

def circle(c,f,n):
  return c*np.exp(-1j*2*np.pi*f*n/fs)

signalAxe = fig.add_subplot(2,2,2)
signalLn, = plt.plot([],[],'b-')
signalAxe.grid(True)
signalAxe.set_xlim(0,N*1/fs)
signalAxe.set_ylim(-1,1)
signalFrec = 2
signalData=[]

promAxe = fig.add_subplot(2,2,3)
promILn,promRLN = plt.plot([],[],'r-',[],[],'b-')
promAxe.grid(True)
promAxe.set_xlim(-fs/2,fs/2)
promAxe.set_ylim(-1,1)
promData=np.zeros(N,dtype=complex)

def signal(f,n):
  return np.sin(2*np.pi*f*n/fs)

tData=np.arange(0,N/fs,1/fs)

def init():
  return circleLn,signalLn,circleLg,massLn
def update(n):
  global circleData,signalData,circleLn
  
  circleData.append(circle(1,circleFrec,n)*signal(signalFrec,n))
  mass=np.average(circleData)
  circleLn.set_data(np.real(circleData), np.imag(circleData))
  massLn.set_data(np.real(mass), np.imag(mass))
 	 
  signalData.append(signal(signalFrec,n))
  signalLn.set_data(tData[:n+1],signalData)
  circleLn.set_label(n)
  circleLg=circleAxe.legend()
  
  if n == N-1:
    circleData=[]
    signalData=[]
    
  return circleLn,signalLn,circleLg,massLn

ani = FuncAnimation(fig, update,N,init, interval=100,blit=True,repeat=True)
plt.show()
