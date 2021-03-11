import heapq, cv2
import numpy as np

class MinHeap:
    def __init__(self):
        self.heap=[]
        self.lookup={}
        
    def add(self,cost, location): #location needs to be a tuple
        if location in self.lookup:
            if self.lookup[location][0]>cost:
                self.remove(location)
            else:
                return
        entry=[cost,location,1]
        self.lookup[location]=entry
        heapq.heappush(self.heap, entry)

    def remove(self,location):
        if location in self.lookup:
            entry = self.lookup.pop(location)
            entry[-1] = 0
            
    def pop(self):
        while self.heap:
            cost, location ,active = heapq.heappop(self.heap)
            if active:
                del self.lookup[location]
                return cost, location
    def __bool__(self):
        return len(self.lookup)>0
        
def h(x,y):
    return (255-x)/10+(255-y)/10

fringe=MinHeap()
# ~ heap.add(234,(0,2))
# ~ heap.add(134,(7,2))
# ~ heap.add(235,(2,2))
# ~ heap.add(264,(4,2))
# ~ heap.add(934,(0,7))
# ~ heap.add(10,(0,7))
# ~ while heap:
    # ~ print(heap.heap)
    # ~ print(heap.pop())
# ~ print(heap.heap)

# ~ n*log(n)

img=cv2.imread("map.png")
explored=set()
fringe.add((h(10,10),0),(10,10))
costmap={}
while fringe:
    (f,cost),(x,y)=fringe.pop()
    costmap[(x,y)]=cost
    explored.add((x,y))
    img[x,y,0]=0
    for dx,dy in (1,0),(0,1),(-1,0),(0,-1):
        xp=x+dx
        yp=y+dy
        if 256>xp>0<yp<256 and (xp,yp) not in explored :
            color=list(img[xp,yp])
            if color==[255,255,255]:
                fringe.add(cost+1+h(xp,yp),(xp,yp))
            if color==[128,128,128]:
                fringe.add(cost+.1,(xp,yp))
            if color==[255,0,0]:
                fringe.add(cost+5,(xp,yp))
    if len(explored)%10==0:
        cv2.imshow("img",img)
        cv2.waitKey(1)



