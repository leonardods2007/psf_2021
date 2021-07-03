import numpy as np
import matplotlib.pyplot as plt

s1=[20,10,30]
s=np.tile(s1,3)
t=np.arange(0,len(s),1)

plt.plot(t,s,'ro-')
plt.show()

