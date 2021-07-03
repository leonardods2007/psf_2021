import matplotlib.pyplot as plt
import numpy as np


fig = plt.figure(1)
Nc=50
tc = np.linspace(0, 10, Nc)
signal=1/np.exp(tc)

ax1 = fig.add_subplot(2,1,1)
ax1.plot(tc, signal,"b-o")
ax1.grid(True)

ax2 = fig.add_subplot(2,1,2)
pot = signal**2
potAcum=np.cumsum(pot)
ax2.stem(tc,potAcum ,"b-o")
ax2.grid(True)

plt.show()
