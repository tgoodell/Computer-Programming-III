#1702107390854557

import time
import json
import socket
import math
import sympy
import numpy as np
from datetime import datetime
from threading import Thread

jobs=[]

class MyThread(Thread):
	def __init__(self,port,ip,number,top,end):
		self.port=port
		self.ip=ip
		self.number=number
		self.top=top
		self.end=end
		super().__init__()
	def run(self):
		f = open("logs.txt", "a")
		a,b=factor(int(self.number),int(self.top),int(self.end),self.port,self.ip)
		# print(str(self.port) + " is free.")
		# print((a,b))
		if a>0 and b>0:
			# jobs.pop(self.number)
			# print(str(self.port) + " is free.")
			# print((a,b))
			now = datetime.now()
			current_time = now.strftime("%H:%M:%S")
			# f.write("FOUND: " + str(current_time) + " - " + str(self.port) + " --> " + str(self.number) + ": " + str(self.top) + " " + str((a,b)) + "\n")
			logMsg="$ Machine " + str(self.ip) + " found factors " + str((a,b)) + " using range " + str((self.end,self.top)) + " for " + str(self.number) + " at " + str(current_time) + "\n"
			f.write(logMsg)
			print(logMsg)
			jobs = []
		else:
			now = datetime.now()
			current_time = now.strftime("%H:%M:%S")
			# f.write("NOT FOUND: " + str(current_time) + " - " + str(self.port) + " --> " + str(self.number) + ": " + str(self.top) + "\n")
			logMsg="* Machine " + str(self.ip) + " did not find factors using range " + str((self.end, self.top)) + " for " + str(self.number) + " at " + str(current_time) + "\n"
			f.write(logMsg)
			print(logMsg)
			# print("No dice.")
		f.close()

def factor(n,t,e,port,ip):
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('12.157.27.'+str(ip), port))
	s.recv(1024)
	# ~ print(s.recv(1024))
	s.sendall(("%d\n"%n).encode("utf-8"))
	s.recv(1024)
	s.sendall(("%d\n"%t).encode("utf-8"))
	s.recv(1024)
	s.sendall(("%d\n"%e).encode("utf-8"))

	a,b=s.recv(1024).split()
	a=float(a)
	b=float(b)
	if a==b"not":
		return n,1
	else:
		return a,b

productOfPrimeNumsToCrack=[]
for num in open("numbers.txt"):
	# print(str(num) + " " + str(int(num)/10000000))
	productOfPrimeNumsToCrack.append(int(num))


threads={i:None for i in range(201,232)}
initialTime=time.perf_counter()
f = open("logs.txt", "w")
f.write("")
f.close()
for num in productOfPrimeNumsToCrack:
	# print("Number: " + str(num))
	jobs=[]
	n=1
	squareRoot=int(math.sqrt(num))
	jobs.append(squareRoot)
	while squareRoot-100000000*n>0:
		jobs.append(squareRoot-100000000*n)
		n+=1
	while jobs:
		f = open("logs.txt", "a")
		for i in range(201,232):
			t=threads[i]
			if not jobs:
				break
			if not t or not t.is_alive():
				job=jobs.pop(0)
				if job>100000000:
					end=job-100000000
				else:
					end=0
				now = datetime.now()
				current_time = now.strftime("%H:%M:%S")
				logMsg="> Factoring " + str(num) + " on machine " + str(i) + " by starting at " + str(end) + " and ending at " + str(job) + " at " + str(current_time) + "\n"
				f.write(logMsg)
				print(logMsg)
				t=MyThread(9876,i,num,job,end)
				t.start()
				threads[i]=t
		f.close()
