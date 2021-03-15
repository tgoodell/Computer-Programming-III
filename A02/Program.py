import cv2
import numpy as np
import math
import random
import heapq

DEBUG=True

def show(img,title="image",wait=True):
    d=max(img.shape[:2])
    if d>1000:
        step=int(math.ceil(d/1000))
        img=img[::step,::step]
    if not DEBUG:
        return
    if np.all(0<=img) and np.all(img<256):
        cv2.imshow(title,np.uint8(img))
    else:
        cv2.imshow(title,normalize(img))
    if wait:
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        cv2.waitKey(1)

def normalize(img):
    img_copy=img*1.0
    img_copy-=np.min(img_copy)
    img_copy/=np.max(img_copy)
    img_copy*=255.9999
    return np.uint8(img_copy)

def flowDirt(img,cimg,x,y,maxV):
    if img[y,x]<=maxV:
        if cimg[y,x,2]<255:
            cimg[y,x,2]+=1
        img[y,x]+=1
        cimg[y,x,0]+=1
        cimg[y,x,1]+=1
        # show(cimg, wait=False)
        if y-1>0 and img[y-1,x]<img[y,x]-1:
            img[y,x]-=1
            cimg[y,x,0]-=1
            cimg[y,x,1]-=1
            flowDirt(img,cimg,x,y-1,maxV)
        elif x+1<4095 and img[y,x+1]<img[y,x]-1:
            img[y,x]-=1
            cimg[y,x,0]-=1
            cimg[y,x,1]-=1
            flowDirt(img,cimg,x+1,y,maxV)
        elif y+1<4095 and img[y+1,x]<img[y,x]-1:
            img[y,x]-=1
            cimg[y,x,0]-=1
            cimg[y,x,1]-=1
            flowDirt(img,cimg,x,y+1,maxV)
        elif x-1>0 and img[y,x-1]<img[y,x]-1:
            img[y,x]-=1
            cimg[y,x,0]-=1
            cimg[y,x,1]-=1
            flowDirt(img,cimg,x-1,y,maxV)
    elif y-1>0 and img[y-1,x]<img[y,x]-1:
        flowDirt(img,cimg,x,y-1,maxV)
    elif x+1<4095 and img[y,x+1]<img[y,x]-1:
        flowDirt(img,cimg,x+1,y,maxV)
    elif y+1<4095 and img[y+1,x]<img[y,x]-1:
        flowDirt(img,cimg,x,y+1,maxV)
    elif x-1>0 and img[y,x-1]<img[y,x]-1:
        flowDirt(img,cimg,x-1,y,maxV)

def dirtDriver(img,tx=3681,ty=3556):
    cimg=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    n=0
    cost=0
    patch=img[ty:ty+400,tx:tx+400]
    maxV=np.max(patch)
    print(maxV)
    while n<401:
        k=0
        while k<401:
            while img[ty+n,tx+k]<maxV:
                cost+=1
                flowDirt(img,cimg,tx+k,ty+n,maxV)
            if img[ty+n,tx+k]==maxV:
                cimg[ty+n,tx+k,0]=255
            if (((n)*0.0025+(k+1)/160000)*100)%0.01==0:
                print(str((((n)*0.0025+(k+1)/160000)*100)) + "%")
            # show(cimg,wait=False)
            k+=1
        # print(str((((n)*0.0025/160000)*100)) + "%")
        n+=1

    return img,cimg,cost

def spotFinder(img):
    candidates=[]

    h,w=img.shape
    nimg=cv2.resize(img,dsize=(w//10,h//10))

    nh,nw=nimg.shape
    n=0
    while n<nh:
        k=0
        while k<nw:
            candidates.append([k*10,n*10,np.std(nimg[n:n+40,k:k+40])])
            k+=1
        n+=1

    np.sort(candidates)
    for n in range(25):
        print(candidates[n])

def patchCheck(img,x,y):
    patch=img[y:y+400,x:x+400]
    return np.all(np.max(patch)==patch)

def getCostDiff(original,final):
    return np.sum(final)-np.sum(original)

def takeDirt(img,cimg,needed,x,y):
    count=0
    while count<needed:
        rx=random.randrange(2,4095)
        ry=random.randrange(2,4095)
        randPixel=img[ry,rx]

        xList=[2870,3646,1579]
        yList=[20,3505,912]
        badSpot=False
        for x,y in xList,yList:
            if (rx>x and rx<x+400) and (ry>y and ry<y+400):
                badSpot=True
        if badSpot:
            pass
        elif randPixel==img[ry,rx-1]==img[ry-1,rx]==img[ry+1,rx]==img[ry,rx+1] or randPixel==img[ry,rx-1]+1==img[ry-1,rx]+1==img[ry+1,rx]+1==img[ry,rx+1]+1:
            if count%10000==0:
                print(str(needed-count))
            show(cimg, wait=False)
            img[ry,rx]-=1
            cimg[ry,rx]-=1
            cimg[ry,rx,1]=255
            count+=1

    return img,cimg

def getFinalDirtCost(original,final):
    h,w=original.shape
    totalDiff=0
    n=0
    while n<h:
        k=0
        while k<w:
            diff=int(original[n,k])-int(final[n,k])
            if diff<0:
                diff=diff*-1
            totalDiff+=diff
            k+=1
        n+=1
    return totalDiff

def generateBases():
    # ---
    # First Step:
    # Use Erosion Recursion to establish flat terrain that is erosion safe.
    # ---

    xList=[2870,3646,1579]
    yList=[20,3505,912]

    img=cv2.imread("input_erosion_safe.png",0)
    for n in range(3):
        # img=cv2.imread("input_erosion_safe.png",0)
        show(img,wait=True)
        x=xList.pop(0)
        y=yList.pop(0)

        rawImg,cimg,cost=dirtDriver(img,x,y)
        img=rawImg

    # ---
    # Second Step:
    # Take note of dirt debt and randomly remove dirt from around the map, while avoiding the base, to pay off the dirt debt.
    # ---

    xList=[2870,3646,1579]
    yList=[20,3505,912]

    for n in range(3):
        # img=cv2.imread("input_erosion_safe.png",0)
        x=xList.pop(0)
        y=yList.pop(0)

        # initialRaw=cv2.imread("raw/site" + str(n) + "-" + str(x) + "-" + str(y) + ".png",0)
        # initialColor=cv2.imread("raw/site" + str(n) + "-" + str(x) + "-" + str(y) + "_color.png")

        initialRaw=img
        initialColor=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

        finalImg,finalColorImg=takeDirt(initialRaw,initialColor,getCostDiff(img,initialRaw),x,y)

        cv2.imwrite(str(n) + "-" + str(x) + "-" + str(y) + ".png",finalImg)
        cv2.imwrite(str(n) + "-" + str(x) + "-" + str(y) + "_color.png", finalColorImg)

    # ---
    # Final Step
    # Double check to make sure dirt debt is paid (finalCost) and get cost in acorns.
    # ---

    initialCosts=[]
    dirtDebt=[]
    costInAcorns=[]
    xList=[2870,3646,1579]
    yList=[20,3505,912]

    for n in range(3):
        img=cv2.imread("input_erosion_safe.png",0)
        x=xList.pop(0)
        y=yList.pop(0)

        initialRaw=cv2.imread(str(n) + "-" + str(x) + "-" + str(y) + ".png",0)
        final=cv2.imread(str(n) + "-" + str(x) + "-" + str(y) + ".png",0)

        initialCosts.append(getCostDiff(img,initialRaw))
        dirtDebt.append(getCostDiff(img,final))
        costInAcorns.append(getFinalDirtCost(img,final))

    print(initialCosts)
    print(dirtDebt) # Should be 0 if dirt debt is paid off
    print(costInAcorns)

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

def genVideos():
    fringe = MinHeap()

    img = cv2.imread("three-bases.png",0)
    cimg=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    h,w=img.shape
    y,x=(20,2870+400)

    # marble rolling
    # check around base, start at smallest cost, look through each of its neighbors until you reach cost of 0 / hit goal. Prefer lower costs.

    xList=[2870,3646,1579]
    yList=[20,3505,912]

    firstSiteBorder=[]
    for n in range(402):
        firstSiteBorder.append((20,2870+n))
        firstSiteBorder.append((420,2870+n))
        firstSiteBorder.append((20+n,2870))
        firstSiteBorder.append((20+n,2870+400))

    secondSiteBorder=[]
    for n in range(402):
        secondSiteBorder.append((3505,3646+n))
        secondSiteBorder.append((3905,3646+n))
        secondSiteBorder.append((3505+n,3646))
        secondSiteBorder.append((3505+n,3646+400))

    thirdSiteBorder=[]
    for n in range(402):
        thirdSiteBorder.append((912,1579+n))
        thirdSiteBorder.append((912+400,1579+n))
        thirdSiteBorder.append((912+n,1579))
        thirdSiteBorder.append((912+n,1579+400))

    explored = set()
    for point in secondSiteBorder:
        fringe.add(0,point)

    video=cv2.VideoWriter("SecondToThird.avi", cv2.VideoWriter_fourcc(*"MJPG"), 60, (4096, 4096))
    costmap = {}
    routes = {}
    count=0
    final=(0,0)
    while fringe:
        cost, (y,x) = fringe.pop()
        costmap[(y,x)] = cost
        explored.add((y,x))
        cimg[y,x,1] = 0
        cimg[y,x,2] = 0
        if (y,x) in thirdSiteBorder:
            final=(y,x)
            print("Finished")
            break
        else:
            # ,(1, 1), (1, -1), (-1, -1), (-1, 1):
            for dy,dx in (1, 0), (0, 1), (-1, 0), (0, -1):
                xp = x + dx
                yp = y + dy

                # and not ((2870<xp<2870+400 and 20<yp<20+400) or (3646<xp<3646+400 and 3505<yp<3505+400) or (1579<xp<1579+400 and 912<yp<912+400))
                if w > xp > 0 < yp < h and (yp,xp) not in explored and not ((2870<xp<2870+400 and 20<yp<20+400) or (3646<xp<3646+400 and 3505<yp<3505+400) or (1579<xp<1579+400 and 912<yp<912+400)):
                    # add(cost + 1, (yp, xp))
                    # color=list(cimg[yp,xp])

                    routes[(yp,xp)]=(y,x)

                    if int(img[y,x])-int(img[yp,xp])==0:
                        fringe.add(cost + 1, (yp,xp))
                    elif np.abs(int(img[y,x])-int(img[yp,xp]))==1:
                        fringe.add(cost + 25, (yp,xp))
                    elif np.abs(int(img[y,x])-int(img[yp,xp]))==2:
                        fringe.add(cost + 100, (yp,xp))

        if len(explored) % 1000 == 0:
            print(len(explored)//1000/60)
            # show(cv2.resize(cimg,(1000,1000)),wait=False)
            video.write(cimg)
            # show(cimg,wait=False)
        # if len(lookup)%100:

    print("done")

    path=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    # video=cv2.VideoWriter("thirdToFirstRoute.avi", cv2.VideoWriter_fourcc(*"MJPG"), 60, (4096, 4096))
    n=0
    with open('SecondToThirdRoutes.txt', 'w') as f:
        while (y,x) not in firstSiteBorder:
            f.write(str((y,x)) + " --> " + str(routes[(y,x)]) + "\n")
            y,x=routes[(y,x)]
            # print(y,x)
            path[y,x,:]=(85,95,254)
            # video.write(path)
            # print(n//60)
            # show(path,wait=False)

    cv2.imwrite("path.png",path)

    show(path,wait=True)

    points12=[]
    with open('FirstToSecondRoutes.txt') as f:
        contents = f.readlines()
        for line in contents:
            coord,_=line.replace("(","").replace(")","").split(" --> ")
            y,x=coord.split(", ")
            points12.append((int(y),int(x)))
        f.close()

    video=cv2.VideoWriter("firstToSecondRoutePlayback.avi", cv2.VideoWriter_fourcc(*"MJPG"), 60, (4096, 4096))
    for point in points12:
        y,x=point
        cimg[y,x,1]=0
        video.write(cimg)
        # show(cimg,wait=False)

    points23=[]
    with open('SecondToThirdRoutes.txt') as f:
        contents = f.readlines()
        for line in contents:
            coord,_=line.replace("(","").replace(")","").split(" --> ")
            y,x=coord.split(", ")
            points23.append((int(y),int(x)))
        f.close()

    video=cv2.VideoWriter("secondToThirdRoutePlayback.avi", cv2.VideoWriter_fourcc(*"MJPG"), 60, (4096, 4096))
    for point in points23:
        y,x=point
        cimg[y,x,2]=0
        video.write(cimg)
        # show(cimg,wait=False)

    points31=[]
    with open('ThirdToFirstRoutes.txt') as f:
        contents = f.readlines()
        for line in contents:
            coord,_=line.replace("(","").replace(")","").split(" --> ")
            y,x=coord.split(", ")
            points31.append((int(y),int(x)))
        f.close()

    video=cv2.VideoWriter("thirdTofirstRoutePlayback.avi", cv2.VideoWriter_fourcc(*"MJPG"), 60, (4096, 4096))
    for point in points31:
        y,x=point
        cimg[y,x,1]=0
        video.write(cimg)
        # show(cimg,wait=False)

    cv2.imwrite("route.png",cimg)

def getCost(filename):
    img=cv2.imread("three-bases.png")
    cost=0
    with open(filename) as f:
        contents = f.readlines()
        for line in contents:
            coord1,coord2=line.replace("(","").replace(")","").split(" --> ")
            y1,x1=coord1.split(", ")
            y2,x2=coord2.split(", ")
            y1=int(y1)
            y2=int(y2)
            x1=int(x1)
            x2=int(x2)
            d=(abs(1.0*x1-1.0*x2)*abs(1.0*x1-1.0*x2))+(abs(1.0*y1-1.0*y2)*abs(1.0*y1-1.0*y2))
            cost=cost+(d+(abs(img[y1,x1]-img[y2,x2]))*(abs(img[y1,x1]-img[y2,x2])))/d
        f.close()

    return cost

genVideos()
getCost("FirstToSecondRoutes.txt")
getCost("SecondToThirdRoutes.txt")
getCost("ThirdToFirstRoutes.txt")