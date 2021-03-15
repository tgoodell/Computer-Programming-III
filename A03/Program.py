import turtle
import heapq
import math

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

t=turtle.Turtle()
screen=turtle.Screen()
roadNetwork={}
allPoints=[]
screen.tracer(20000)
screen.setworldcoordinates(354965.71889999975,3652539.9209000003,794703.8134000003,4044411.3215999994)
t.color("black")
count=0
with open("UpdatedRoads.txt") as f:
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
            t.penup()
            t.goto((int(ox),int(oy)))
            t.pendown()
            t.goto((int(tx),int(ty)))
            count+=1

        roadNetwork[(int(ox),int(oy))]=coords

heuristic=genHeuristic(allPoints,(495022,3817992))

# screen.tracer(20)

fringe = MinHeap()
explored=set()
x,y=(355115,4040572)
fringe.add(0,(x,y))

costmap = {}
routes={}
count=0
while fringe:
    cost, (x,y) = fringe.pop()
    costmap[(x,y)] = cost
    explored.add((x,y))
    if (x,y)==(666045,3653235):
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
x,y=666045,3653235
with open("routes.txt","w") as f:
    while (x,y)!=(355115,4040572):
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
    t.goto((355115,4040572))

screen.getcanvas().postscript(file="route.eps")