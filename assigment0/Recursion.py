import cv2
import numpy as np
import math
import random

DEBUG=True
tx=3556 # 576
ty=3681 # 499
cost=0

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

def flowDirt(img,cimg,x,y):
    if img[y,x]<=208:
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
            flowDirt(img,cimg,x,y-1)
        elif x+1<4095 and img[y,x+1]<img[y,x]-1:
            img[y,x]-=1
            cimg[y,x,0]-=1
            cimg[y,x,1]-=1
            flowDirt(img,cimg,x+1,y)
        elif y+1<4095 and img[y+1,x]<img[y,x]-1:
            img[y,x]-=1
            cimg[y,x,0]-=1
            cimg[y,x,1]-=1
            flowDirt(img,cimg,x,y+1)
        elif x-1>0 and img[y,x-1]<img[y,x]-1:
            img[y,x]-=1
            cimg[y,x,0]-=1
            cimg[y,x,1]-=1
            flowDirt(img,cimg,x-1,y)
    elif y-1>0 and img[y-1,x]<img[y,x]-1:
        flowDirt(img,cimg,x,y-1)
    elif x+1<4095 and img[y,x+1]<img[y,x]-1:
        flowDirt(img,cimg,x+1,y)
    elif y+1<4095 and img[y+1,x]<img[y,x]-1:
        flowDirt(img,cimg,x,y+1)
    elif x-1>0 and img[y,x-1]<img[y,x]-1:
        flowDirt(img,cimg,x-1,y)

def dirtDriver(img,tx=3681,ty=3556):
    cimg=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    n=0
    cost=0
    patch=img[ty:ty+400,tx:tx+400]
    maxV=208 # np.max(patch)
    print(maxV)
    while n<401:
        k=0
        while k<401:
            while img[ty+n,tx+k]<maxV:
                cost+=1
                flowDirt(img,cimg,tx+k,ty+n)
            if img[ty+n,tx+k]==maxV:
                cimg[ty+n,tx+k,0]=255
            print(str((((n)*0.0025+(k+1)/160000)*100)) + "%")
            # show(cimg,wait=False)
            k+=1
        n+=1

    return img,cimg,cost

def depositDirt(img,cimg,x,y,dugPixels):
    count=0
    while count<dugPixels:
        rx=random.randrange(2,4095)
        ry=random.randrange(2,4095)
        randPixel=img[ry,rx]

        if (rx>x and x<rx+400) or (ry>y and y<ry+400):
            pass
        elif randPixel==img[ry,rx-1]==img[ry-1,rx]==img[ry+1,rx]==img[ry,rx+1]:
            img[ry,rx]+=1
            cimg[ry,rx]+=1
            cimg[ry,rx,1]=255
            count+=1

    return img,cimg

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



img=cv2.imread("../input_erosion_safe.png",0)
outImg=cv2.imread("out.png")
outImg,cimg,cost=dirtDriver(img,2870,20)

# 316451

# print(np.sum(outImg)-np.sum(img))
print(np.sum(outImg))
print(np.sum(img))
print(cost)
print("Seward Cost: " + str(np.sum(np.abs(outImg-img))))
cv2.imwrite("out.png",outImg)
cv2.imwrite("colorOut.png",cimg)

# cimg=cv2.imread("colorOut.png")

# format: img[y,x]

show(img,wait=True)
show(cimg,wait=True)

# some places go from 208 to 206 on the top and right