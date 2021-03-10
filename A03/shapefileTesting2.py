import geopandas as gpd
import matplotlib.pyplot as plt
import shapefile
import turtle
import math
shapef=gpd.read_file("HIGHWAY_LINEAR_REF_SYSTEM_ARNOLD.shx")
shapez=shapefile.Reader("HIGHWAY_LINEAR_REF_SYSTEM_ARNOLD.shx")
points = {}
bob=turtle.Turtle()
bob.ht()
screen=turtle.Screen()
screen.tracer(10000)
screen.setworldcoordinates(354965.71889999975,3652539.9209000003,794703.8134000003,4044411.3215999994)


def add(p1, p2):
    global points
    p1 = clean(p1)
    p2 = clean(p2)
    if p1 not in points:
        points[p1] = [p2]
    else:
        points[p1].append(p2)
    if p2 not in points:
        points[p2] = [p1]
    else:
        points[p2].append(p1)


def clean(p):
    x, y = p
    return int(x), int(y)


def dist(p1, p2):
    x, y = p1
    i, j = p2
    return math.hypot(x - i, y - j)


for feature in shapez.shapeRecords():
    first = feature.shape.__geo_interface__
    try:
        if isinstance(first["coordinates"][0][0], float):
            add(first["coordinates"][0], first["coordinates"][-1])
            # ~ print(dist(first["coordinates"][0],first["coordinates"][-1]))

        for m in first["coordinates"][0], first["coordinates"][-1]:
            if isinstance(m[0], float):

                x, y = m
                # ~ bob.goto(x,y)
                # ~ bob.down()
            else:
                # ~ bob.up()
                add(m[0], m[-1])
                # ~ print(dist(m[0],m[-1]))
                # ~ for x,y in m[0],m[-1]:
                # ~ bob.goto(x,y)
                # ~ bob.down()
            # ~ a=min(a,x)
            # ~ b=min(b,y)
            # ~ c=max(c,x)
            # ~ d=max(d,y)

    except:
        print(first)
print(len(points))
deleteList = []
for point in points.keys():
    if len(points[point]) == 2:
        a, b = points[point]
        points[a].remove(point)
        points[b].remove(point)
        points[a].append(b)
        points[b].append(a)
        deleteList.append(point)
for p in deleteList:
    del points[p]
print(len(points))
# ~ for point in points.keys():
# ~ for other in points[point]:
# ~ bob.up()
# ~ bob.goto(*point)
# ~ bob.down()
# ~ bob.goto(*other)

f = open("roads.txt", "w")
for point in points.keys():
    f.write("(%d %d) =>" % point)
    for other in points[point]:
        f.write(" (%d %d)" % other)
    f.write("\n")
f.close()