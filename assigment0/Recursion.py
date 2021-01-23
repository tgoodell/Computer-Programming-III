import cv2
import numpy as np
import math

DEBUG=True
tx=3556 # 576
ty=3681 # 499

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

def safe(img,x,y):
    if np.abs(img[x,y-1]-img[x,y])<=1 and np.abs(img[x+1,y]-img[x,y])<=1 and np.abs(img[x,y+1]-img[x,y])<=1 and np.abs(img[x-x,y]-img[x,y])<=1:
        return True

def northSafe(img,x,y):
    compareValue=img[x,y]
    if img[x,y-1]<=img[x,y]+1 and img[x,y-1]>=img[x,y]-1:
        return True
    else:
        return False

def flowingDirt(img,cimg):
    n=0
    patch=img[ty:ty+100,tx:tx+100]
    maxV=np.max(patch)
    while n<100:
        k=0
        while k<100:
            x=tx+k
            y=ty+n

            while img[tx+k,ty+n]<maxV:
                img[x,y]+=1
                currentVal=img[x,y]
                cimg[x,y,2]+=1
                
                if y-1>0 and img[x,y-1]<currentVal-1:
                    img[x,y]-=1
                    y-=1
                if x+1<1024 and img[x+1,y]<currentVal-1:
                    img[x,y]-=1
                    x+=1
                if y-1<1024 and img[x,y+1]<currentVal-1:
                    img[x,y]-=1
                    y+=1
                if x-1>0 and img[x-1,y]<currentVal-1:
                    img[x,y]-=1
                    x-=1

                show(cimg,wait=False)

            if img[tx+k,ty+n]==maxV:
                cimg[tx+k,ty+n,0]=255
            show(cimg,wait=False)
            k+=1
        n+=1

count=0

def flowDirt(img,cimg,x,y):
    if img[x,y]<=208:
        if cimg[x,y,2]<255:
            cimg[x,y,2]+=1
        img[x,y]+=1
        cimg[x,y,0]+=1
        cimg[x,y,1]+=1
        # show(cimg, wait=False)
        if y>0 and img[x,y-1]<img[x,y]-1:
            img[x,y]-=1
            cimg[x,y,0]-=1
            cimg[x,y,1]-=1
            flowDirt(img,cimg,x,y-1)
        elif x<4095 and img[x+1,y]<img[x,y]-1:
            img[x,y]-=1
            cimg[x,y,0]-=1
            cimg[x,y,1]-=1
            flowDirt(img,cimg,x+1,y)
        elif y<4095 and img[x,y+1]<img[x,y]-1:
            img[x,y]-=1
            cimg[x,y,0]-=1
            cimg[x,y,1]-=1
            flowDirt(img,cimg,x,y+1)
        elif x>0 and img[x-1,y]<img[x,y]-1:
            img[x,y]-=1
            cimg[x,y,0]-=1
            cimg[x,y,1]-=1
            flowDirt(img,cimg,x-1,y)
    elif y>0 and img[x,y-1]<img[x,y]-1:
        flowDirt(img,cimg,x,y-1)
    elif x<4095 and img[x+1,y]<img[x,y]-1:
        flowDirt(img,cimg,x+1,y)
    elif y<4095 and img[x,y+1]<img[x,y]-1:
        flowDirt(img,cimg,x,y+1)
    elif x>0 and img[x-1,y]<img[x,y]-1:
        flowDirt(img,cimg,x-1,y)



oimg=cv2.imread("../input_erosion_safe.png",0)
h,w=oimg.shape

img=oimg # oimg[3*h//4:,3*w//4:]
cv2.imwrite("cropped-out.png",img)
print(oimg.shape)
cimg=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

print(cimg.shape)
# cimg[1000:1020,1000:1020,2]=255
# cv2.imwrite("out.png",cimg)

n=0
patch=img[ty:ty+400,tx:tx+400]
maxV=208 # np.max(patch)
print(maxV)
while n<401:
    k=0
    while k<401:
        while img[tx+k,ty+n]<maxV:
            flowDirt(img,cimg,tx+k,ty+n)
        if img[tx+k,ty+n]==maxV:
            cimg[tx+k,ty+n,0]=255
        print(str((((n)*0.0025+(k+1)/160000)*100)) + "%")
        # show(cimg,wait=False)
        k+=1
    n+=1

# n=0
# while n<451:
#     k=0
#     while k<451:
#         x=tx-25+k
#         y=ty-25+n
#         if y>0 and img[x,y-1]<img[x,y]-1:
#             print("False")
#             flowDirt(img,cimg,x,y-1)
#         if x<4095 and img[x+1,y]<img[x,y]-1:
#             print("False")
#             flowDirt(img,cimg,x+1,y)
#         if y<4095 and img[x,y+1]<img[x,y]-1:
#             print("False")
#             flowDirt(img,cimg,x,y+1)
#         if x>0 and img[x-1,y]<img[x,y]-1:
#             print("False")
#             flowDirt(img,cimg,x-1,y)
#         k+=1
#     n+=1

# flowingDirt(img,cimg)

patch=img[ty:ty+100,tx:tx+100]
print(np.std(patch))
print(np.average(patch))

cost=np.sum(np.abs(img-oimg))
print(cost)

cv2.imwrite("out.png",img)
cv2.imwrite("colorOut.png",cimg)

show(img,wait=True)
show(cimg,wait=True)

# some places go from 208 to 206 on the top and right