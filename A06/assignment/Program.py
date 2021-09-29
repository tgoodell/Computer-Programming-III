import random
import time
import numpy as np
import reference.hashtable

class HashMap:
    def __init__(self,size=20,itemCount=0):
        self.size = size
        self.itemCount=itemCount
        self.map = np.array()
        for n in range(self.size):
            self.map.append((-1, -1))

    def hasher(self,key):
        output = 0
        for c in key:
            random.seed(ord(c))
            output += ord(c) * random.randint(1, 10000000)
        return output%self.size
    
    def upsize(self):
        self.size*=2
        newMap=[]
        for n in range(self.size):
            newMap.append((-1, -1))

        for item in self.map:
            k,v=item
            if item!=(-1,-1):
                if newMap[self.hasher(k)]==(-1,-1):
                    newMap[self.hasher(k)]=item
                else:
                    n=1
                    while newMap[(self.hasher(k)+n)%self.size]!=(-1,-1):
                        if n>self.size:
                            break
                        n+=1
                    newMap[(self.hasher(k)+n)%self.size]=item

        self.map=newMap

        return self

    def add(self,key,value):
        self.itemCount+=1
        if self.itemCount>self.size*.8:
            self.upsize()

        hashed=self.hasher(key)

        if self.map[hashed]==(-1,-1):
            self.map[hashed]=(key,value)
        else:
            n=1
            while self.map[(hashed+n)%self.size]!=(-1,-1):
                if n>self.size:
                    break
                n+=1
            self.map[(hashed+n)%self.size]=(key,value)

        return self.map
        
    def delete(self,key):
        hashed=self.hasher(key,self.size)
        k,_=self.map[hashed]
        if k==key:
            self.map[hashed]=(-1,-1)
        else:
            n=1
            while k!=key:
                k,_=self.map[(hashed+n)%self.size]
                if n>self.size:
                    return False
                n+=1
            self.map[(hashed+n)%self.size]=(-1,-1)

        return self.map
    
    def get(self,key):
        k,v=self.map[self.hasher(key)]
        if k==key:
            return v
        else:
            n=0
            while k!=key:
                k,_=self.map[(self.hasher(key)+n)%self.size]
                if n>self.size:
                    return False
                n+=1
            _,v2=self.map[self.hasher(key)+n-1]
            return v2
        
    def getHashMap(self):
        return self.map

    def getItemCount(self):
        return self.itemCount

    def getSize(self):
        return self.size

class IRHashMap:
    def __init__(self,size=20,itemCount=0):
        self.size = size
        self.transferSize=size*2
        self.itemCount=itemCount
        self.map = []
        self.transferMap=[]
        self.thingsToTransfer=[]
        self.currentlyResizing=False
        for n in range(self.size):
            self.map.append((-1, -1))

        self.currentlyResizing = False
        
    def hasher(self,key):
        if self.currentlyResizing:
            size=self.size*2
        else:
            size=self.size

        output = 0
        for c in key:
            random.seed(ord(c))
            output += ord(c) * random.randint(1, 10000000)

        return output%size

    def add(self,key,value):
        if self.currentlyResizing:
            self.transfer()

            self.itemCount+=1

            hashed=self.hasher(key)

            if self.transferMap[hashed]==(-1,-1):
                self.transferMap[hashed]=(key,value)
            else:
                n=1
                while self.transferMap[(hashed+n)%self.transferSize]!=(-1,-1):
                    if n>self.transferSize:
                        break
                    n+=1
                self.transferMap[(hashed+n)%self.transferSize]=(key,value)

        else:
            self.itemCount+=1
            if self.itemCount>self.size*.8:
                self.upsize()

            hashed=self.hasher(key)

            if self.map[hashed%self.size]==(-1,-1):
                self.map[hashed%self.size]=(key,value)
            else:
                n=1
                while self.map[(hashed+n)%self.size]!=(-1,-1):
                    if n>self.size:
                        break
                    n+=1
                self.map[(hashed+n)%self.size]=(key,value)

        return self

    def upsize(self):
        self.transferSize=self.size*2
        self.transferMap=[]
        for n in range(self.transferSize):
            self.transferMap.append((-1, -1))

        self.currentlyResizing=True

        self.thingsToTransfer=self.map

        return self


    def transfer(self):
        n=0
        while self.thingsToTransfer and n<4:
            key,value=self.thingsToTransfer.pop()
            if (key,value)!=(-1,-1):
                hashed=self.hasher(key)

                if self.transferMap[hashed]==(-1,-1):
                    self.transferMap[hashed]=(key,value)
                else:
                    n=1
                    while self.transferMap[(hashed+n)%self.transferSize]!=(-1,-1):
                        if n>self.size:
                            break
                        n+=1
                    self.transferMap[(hashed+n)%self.transferSize]=(key,value)

                n+=1

        if not self.thingsToTransfer:
            self.currentlyResizing=False
            self.map=self.transferMap
            self.size=self.transferSize
    
    def getHashMap(self):
        if self.currentlyResizing:
            while self.thingsToTransfer:
                self.transfer()

        return self.map

    def getItemCount(self):
        return self.itemCount

    def getSize(self):
        return self.size
            

# store=HashMap()

random.seed("Seward")
target=2**random.randint(10,100000000)

HashTable = reference.hashtable.new()

f=open("benchmarkReferenceByTens.csv","w")
n=0
startTime=time.time()
while n<target and time.time()<startTime+300:
    key,value=str(int(random.random()*100000)),str(int(random.random()*100000))
    # store.insert(key,value)
    reference.hashtable.set(HashTable, key, value)

    if n%10==0:
        timeNow=str(time.time()-startTime)
        f.write(timeNow + ", " + str(n) + "\n")

    n+=1

reference.hashtable.list(HashTable)

# print(store.getHashMap())
# print(store.getItemCount())
# print(store.getSize())


# store.add("hello","howdy")
# print(store.get("hello"))
# print(store.getItemCount())
# print(store.getSize())