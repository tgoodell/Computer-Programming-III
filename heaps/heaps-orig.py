# 100,75,50,74,73,40,30
#
# [cost,location]
# 32,87,08,23,1,78,65,09,34
#
# x -> 2*x+1,2*x+2
#
# heapify

import heapq
import cv2

class MinHeap:
    def __init__(self):
        self.heap=[]
        self.lookup={}

    def add(self,cost,location): # location needs to be a tuple
        if location in self.lookup :
            if self.lookup[location][0]>cost:
                self.remove(location)
            else:
                return
        entry=[cost,location,1]
        self.lookup[location]=entry
        heapq.heappush(self.heap,entry)

    def remove(self,location):
        if location in self.lookup:
            entry=self.lookup(location)
            entry[-1]=0

    def pop_task(self):
        while self.heap:
            cost,location,active=heapq.heappop(self.heap)
            if not active:
                continue
            elif active:
                del self.lookup[location]
                return cost,location

    def __bool__(self):
        return len(self.lookup)>0

# heap=MinHeap()
# heap.add(234,(0,2))
# heap.add(134,(7,2))
# heap.add(235,(9,2))
# heap.add(264,(2,2))
# heap.add(934,(11,2))
# heap.add(10,(11,2))
#
# while heap:
#     print(heap.pop())

# m*n*log(fringeSize) # complexity

fringe=MinHeap()
img=cv2.imread("map.png",0)
explored=set()
fringe.add(0,(10,10))

while fringe:
    cost,(x,y)=fringe.pop()
    explored.add((x,y))
    img[x,y]=128
    for dx,dy in (1,0),(0,1),(-1,0),(0-1):
        xp=x+dx
        yp=y+dy
        if 256>xp>0<yp<256 and (xp,yp) not in explored and img[xp,yp]==(255,255,255):
            fringe.add(cost+1,(xp,yp))

    print(cost)

    cv2.imshow("img",img)
    cv2.waitKey(1)