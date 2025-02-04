import cv2
import numpy as np
import math
import random

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
            show(cimg,wait=False)
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

        if (rx>x and rx<x+400) and (ry>y and ry<y+400):
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

# ---
# First Step:
# Use Erosion Recursion to establish flat terrain that is erosion safe.
# ---

xList=[2870,3646,1579]
yList=[20,3505,912]

for n in range(3):
    img=cv2.imread("input_erosion_safe.png",0)
    show(img,wait=True)
    x=xList.pop(0)
    y=yList.pop(0)

    rawImg,cimg,cost=dirtDriver(img,x,y)
    cv2.imwrite("raw/site" + str(n) + "-" + str(x) + "-" + str(y) + ".png",rawImg)
    cv2.imwrite("raw/site" + str(n) + "-" + str(x) + "-" + str(y) + "_color.png",cimg)

# ---
# Second Step:
# Take note of dirt debt and randomly remove dirt from around the map, while avoiding the base, to pay off the dirt debt.
# ---

xList=[2870,3646,1579]
yList=[20,3505,912]

for n in range(3):
    img=cv2.imread("input_erosion_safe.png",0)
    x=xList.pop(0)
    y=yList.pop(0)

    initialRaw=cv2.imread("raw/site" + str(n) + "-" + str(x) + "-" + str(y) + ".png",0)
    initialColor=cv2.imread("raw/site" + str(n) + "-" + str(x) + "-" + str(y) + "_color.png")

    finalImg,finalColorImg=takeDirt(initialRaw,initialColor,getCostDiff(img,initialRaw),x,y)

    cv2.imwrite("sites/base" + str(n) + "-" + str(x) + "-" + str(y) + ".png",finalImg)
    cv2.imwrite("sites/base" + str(n) + "-" + str(x) + "-" + str(y) + "_color.png", finalColorImg)

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

    initialRaw=cv2.imread("raw/site" + str(n) + "-" + str(x) + "-" + str(y) + ".png",0)
    final=cv2.imread("sites/base" + str(n) + "-" + str(x) + "-" + str(y) + ".png",0)

    initialCosts.append(getCostDiff(img,initialRaw))
    dirtDebt.append(getCostDiff(img,final))
    costInAcorns.append(getFinalDirtCost(img,final))

print(initialCosts)
print(dirtDebt) # Should be 0 if dirt debt is paid off
print(costInAcorns)

