import turtle
import heapq
import math
import pyproj

# Seward Questions:
# - Animation Tips?
# - Ways to standardize coordniates so origin is (0,0)?
# - Would using OpenCV to draw Lines/Paths of circles be better for the animation?
#   - i.e. Dividing each edge into lots of pixels instead of a straight line for smoother animation. 

maxX=794701
minX=355115
maxY=4044411
minY=3652539

start=(554326, 3856136)
end=(494821, 3819654)

class MinHeap:
    def __init__(self):
        self.heap = []
        self.lookup = {}

    def add(self, cost, location):  # location needs to be a tuple
        if location in self.lookup:
            if self.lookup[location][0] > cost:
                self.remove(location)
            else:
                return
        entry = [cost, location, 1]
        self.lookup[location] = entry
        heapq.heappush(self.heap, entry)

    def remove(self, location):
        if location in self.lookup:
            entry = self.lookup.pop(location)
            entry[-1] = 0

    def pop(self):
        while self.heap:
            cost, location, active = heapq.heappop(self.heap)
            if active:
                del self.lookup[location]
                return cost, location

    def __bool__(self):
        return len(self.lookup) > 0

def genHeuristic(points,goal):
    gx,gy=goal
    map=[]
    heuristic={}

    for line in points:
        px,py=line
        map.append((px,py))
        if (px,py) not in heuristic:
            heuristic[(px,py)]=math.sqrt(abs(gx-px)*abs(gx-px)+abs(gy-py)*abs(gy-py))

    return heuristic

def adjustRoads():
    wgs84 = pyproj.Proj(projparams='epsg:4326')
    InputGrid = pyproj.Proj(projparams='epsg:26915')
    text=""
    with open("UpdatedRoads.txt") as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace("=>", "").replace("\n", "").replace("(", "").replace(")", "").split(" ")
            ox, oy = line.pop(0), line.pop(0)
            ox, oy = pyproj.transform(InputGrid, wgs84, ox, oy)
            line.pop(0)
            coords = []
            newLine="("+str(int(ox)-minX)+" "+str(int(oy)-minX)+") =>"
            for num in line:
                tx,ty,type=line.pop(0),line.pop(0),line.pop(0)

                tx,ty=pyproj.transform(InputGrid, wgs84, tx, ty)
                new=" ("+str(tx)+" "+str(ty)+" "+type+")"
                print(new)
                newLine+=new
            newLine+="\n"
            text+=newLine

    with open("adjustedRoadNetwork.txt","w") as f:
        f.write(text)

adjustRoads()
print("next")

t=turtle.Turtle()
screen=turtle.Screen()
roadNetwork={}
allPoints=[]
screen.tracer(0)
# screen.setworldcoordinates(354965.71889999975,3652539.9209000003,794703.8134000003,4044411.3215999994)
screen.setworldcoordinates(36.5,36,-94.03,-94.22)
t.color("black")
count=0
xList=[]
yList=[]
with open("adjustedRoadNetwork.txt") as f:
    lines=f.readlines()
    for line in lines:
        line=line.replace("=>","").replace("\n","").replace("(","").replace(")","").split(" ")
        # line.remove(line.index(''))
        ox,oy=line.pop(0),line.pop(0)
        line.pop(0)
        coords=[]
        for num in line:
            tx,ty,type=line.pop(0),line.pop(0),line.pop(0)
            coords.append((int(tx),int(ty),type))
            allPoints.append((int(tx),int(ty)))
            xList.append(int(tx))
            yList.append(int(ty))
            t.penup()
            t.goto((int(ox),int(oy)))
            t.pendown()
            t.goto((int(tx),int(ty)))
            count+=1

        roadNetwork[(int(ox),int(oy))]=coords
    print(min(xList))

heuristic=genHeuristic(allPoints,(495022,3817992))

# screen.tracer(20)

fringe = MinHeap()
explored=set()
# 36.499363,-94.617611
# Top Left: 355115,4040572
#
x,y=start
fringe.add(0,(x,y))

costmap = {}
routes={}
count=0
while fringe:
    cost, (x,y) = fringe.pop()
    costmap[(x,y)] = cost
    explored.add((x,y))
    if (x,y)==end:
        print("Finished")
        break
    elif (x,y) in roadNetwork:
        for xp,yp,dtype in roadNetwork[(x,y)]:
            if (xp,yp) not in explored:
                # t.color("red")
                # heuristic[(xp,yp)]
                if dtype=="US":
                    t.color("dark blue")
                    fringe.add(cost+20,(xp,yp))
                elif dtype=="Interstate":
                    t.color("orange")
                    fringe.add(cost+5,(xp,yp))
                elif dtype=="State":
                    t.color("spring green")
                    fringe.add(cost+25,(xp,yp))
                elif dtype=="Local":
                    t.color("medium slate blue")
                    fringe.add(cost+40,(xp,yp))
                # else:
                #     print(dtype)
                t.penup()
                t.goto((int(x),int(y)))
                t.pendown()
                t.goto((xp,yp))

                routes[(xp,yp)] = (x,y)


    # if len(explored) % 10000 == 0:
    #     print(len(explored))
        # show(cv2.resize(cimg,(1000,1000)),wait=False)

#
screen.getcanvas().postscript(file="out.eps")
print((x,y))

t.color("red")
t.width(3)
x,y=end
# x,y=567817, 3855997
with open("routes.txt","w") as f:
    while (x,y)!=start:
        f.write(str((x,y)) + "-->" + str(routes[(x,y)]) + "\n")
        ix,iy=x,y
        x,y=routes[(x,y)]
        t.penup()
        t.goto((int(ix), int(iy)))
        t.pendown()
        t.goto((x, y))

    t.penup()
    t.goto(x, y)
    t.pendown()
    t.goto(start)

screen.getcanvas().postscript(file="route.eps")