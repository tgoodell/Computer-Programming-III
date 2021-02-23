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
        elif x+1<399 and img[y,x+1]<img[y,x]-1:
            img[y,x]-=1
            cimg[y,x,0]-=1
            cimg[y,x,1]-=1
            flowDirt(img,cimg,x+1,y,maxV)
        elif y+1<399 and img[y+1,x]<img[y,x]-1:
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
    elif x+1<399 and img[y,x+1]<img[y,x]-1:
        flowDirt(img,cimg,x+1,y,maxV)
    elif y+1<399 and img[y+1,x]<img[y,x]-1:
        flowDirt(img,cimg,x,y+1,maxV)
    elif x-1>0 and img[y,x-1]<img[y,x]-1:
        flowDirt(img,cimg,x-1,y,maxV)

def placeDirt(img,cimg,needed):
    count=0
    while count<needed:
        rx=random.randrange(0,999)
        ry=random.randrange(0,999)

        if count%100000==0:
            print(str(needed-count))
            # show(img, wait=False)
        flowDirt(img,cimg,rx,ry,255)
        count+=1

    return img,cimg

def checkSpot(patch,x,y):
    value=patch[y,x]
    if value-1<=patch[y-1,x]<=value+1 and value-1<=patch[y+1,x]<=value+1 and value-1<=patch[y,x+1]<=value+1 and value-1<=patch[y,x-1]<=value+1:
        return True
    else:
        return False

img=cv2.imread("Arkansas_Terrain_Map.jpg",0)
patch=img[1000:1400,1000:1400]

cimg=cv2.cvtColor(patch,cv2.COLOR_GRAY2BGR)

show(patch)

max=np.max(patch)

n=0
while n<400:
    k=0
    while k<400:
        while checkSpot(patch,k,n):
            flowDirt(patch,cimg,k,n,max)
            show(cimg,wait=False)
        k+=1
    print(n)
    n+=1


show(patch,wait=True)