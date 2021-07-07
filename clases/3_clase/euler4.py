import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig        = plt.figure()
fs         = 20.0
N          = 20
#--------------------------------------
circleAxe  = fig.add_subplot(2,2,1)
circleLn, = plt.plot([] ,[] ,'ro-' ,linewidth = 2)
radioLn,  = plt.plot([0 ,0] ,[0.5 ,0.5] ,'g-' ,linewidth = 3 ,alpha = 0.2)
massLn,   = plt.plot([] ,[] ,'bX' ,linewidth = 1 ,alpha = 1)

circleAxe.grid(True)
circleAxe.set_xlim(-1,1)
circleAxe.set_ylim(-1,1)
tSequence = np.arange(0,N,1) #arranco con numeros enteros para evitar errores de float
circleFrec = (tSequence-N/2)*fs/N

circleLn.set_label(circleFrec[0])
circleLg   = circleAxe.legend()
circleData = []
mass       = 0
frecIter   = -1
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
#-----------CONJUGADO----------------------
#conjugado=np.zeros(100,dtype=complex)
#conjugado+=0.2
#N=len(conjugado)
#conjugado[6]=0.5*N
#conjugado[100-6]=0.5*N
#def signal(f,n):
#    return conjugado[n]
#--------------------------------------
promAxe  = fig.add_subplot(2,2,3)
promRLn,promILn,promMagLn,promPhaseLn  = plt.plot([],[],'b-o',[],[],'r-o',[],[],'k-o',[],[],'y-')
promAxe.grid(True)
promAxe.set_xlim(-fs/2,fs/2)
promAxe.set_ylim(-1,1)
promData=np.zeros(N,dtype=complex)
#--------------------------------------

prom3DAxe = fig.add_subplot(2,2,4,projection = "3d")
def plot3DLn(x,y,z):
    prom3DAxe.clear()
    prom3DLn = prom3DAxe.plot3D(x,y,z,'g-o',linewidth=2)
    prom3DAxe.set_xlim(-fs/2,fs/2)
    prom3DAxe.set_ylim(-1,1)
    prom3DAxe.set_zlim(-1,1)

#--------------------------------------
tData=tSequence/fs

def init():
    global circleData,signalData,promData,frecIter,circleFrec,circleLg
    circleData = []
    signalData = []
    frecIter+=1
    if frecIter >= (N-1):
        ani.repeat=False
    return circleLn,circleLg,signalLn,massLn,promRLn,promILn,promMagLn,promPhaseLn,radioLn


def update(n):
    global circleData,signalData,promData,frecIter,circleFrec,circleLg
    circleData.append(circle(circleFrec[frecIter],n)*signal(signalFrec,n))
    mass=np.average(circleData)
    massLn.set_data(np.real(mass),
                    np.imag(mass))
    circleLn.set_data(np.real(circleData),
                      np.imag(circleData))
    signalData.append(signal(signalFrec,n))
    signalLn.set_data(tData[:n+1],signalData)
    promData[frecIter]=mass
    promRLn.set_data(circleFrec[:frecIter+1],np.real(promData[:frecIter+1]))
    promILn.set_data(circleFrec[:frecIter+1],np.imag(promData[:frecIter+1]))
    radioLn.set_data([0,10*np.real(circle(circleFrec[frecIter],n))],[0,10*np.imag(circle(circleFrec[frecIter],n))])
    #promMagLn.set_data(circleFrec[:frecIter+1],np.abs(promData[:frecIter+1])**2)
    #promPhaseLn.set_data(circleFrec[:frecIter+1],np.angle(promData[:frecIter+1])/np.pi)
    circleLn.set_label(circleFrec[frecIter])
    circleLg=circleAxe.legend()

    plot3DLn(circleFrec[:frecIter+1],np.real(promData[:frecIter+1]),np.imag(promData[:frecIter+1]))
    return circleLn,circleLg,signalLn,massLn,promRLn,promILn,promMagLn,promPhaseLn,radioLn

ani=FuncAnimation(fig,update,N,init,interval=1 ,blit=False,repeat=True)
plt.get_current_fig_manager().window.showMaximized()
plt.show()
