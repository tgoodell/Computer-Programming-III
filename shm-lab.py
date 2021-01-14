import numpy as np

print(np.sin(0.5))

i=0
while i<1:
    if np.sin(i)<i*1.05 and np.sin(i)>i*0.95:
        print(i)
    i+=0.0001

print(np.sin(0.5518999999999555))