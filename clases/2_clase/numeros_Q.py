from fxpmath import Fxp
import numpy as np

M      = 1
N      = 2
SIGNED = True

if(SIGNED):
    MIN    = -2**(M-1)
    MAX    = 2**(M-1)-1/2**N
else:
    MIN    = 0
    MAX    = 2**(M)-1/2**N

n=np.arange(MIN,MAX+1/(2**N),1/(2**N))

Q = Fxp(n, signed = SIGNED, n_word = M+N, n_frac  = N,rounding  = "trunc")    # create fixed-point object (3 bit for intefer, 2 for fractional)

for i in range(len(n)):
    print("decimal: {0:.5f} \tbinary: {1:} \thex: {2:}"
          .format(n[i],     Fxp.bin(Q)[i], Fxp.hex(Q)[i]))

