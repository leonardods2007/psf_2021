import numpy as np
import matplotlib.pyplot as plt

signalFrec = 2
NC         = 2000
fsC        = 400
tC         = np.arange(-NC/fsC,NC/fsC,1/fsC)

B=1
sinc=np.sinc(2*B*(tC))
#sinc=np.sin(np.pi*tC)/(np.pi*tC)

fig        = plt.figure()

contiAxe = fig.add_subplot(2,1,1)
plt.plot(tC,sinc,'b-',tC,tC*0,'r-')
plt.grid()

contiAxe = fig.add_subplot(2,1,2)
plt.plot(fsC/2*(fsC/(2*NC))*tC[len(tC)//2:],np.abs(np.fft.fft(sinc))[0:len(tC)//2],'b-')
plt.grid()

plt.get_current_fig_manager().window.showMaximized() #para QT5
plt.show()
