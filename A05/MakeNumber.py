from sympy.ntheory import isprime
import random

def getPrime(i):
	i-=1
	a=random.randrange(10**i,10**(i+1))
	while not isprime(a):
		a=random.randrange(10**i,10**(i+1))
	return a

for i in range(1,42):
	a=getPrime(i)
	b=getPrime(i)
	print(a*b)
	
	
