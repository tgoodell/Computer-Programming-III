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

        if (rx>x and rx<x+400) and (ry>y and ry<y+400):
            pass
        elif randPixel==img[ry,rx-1]==img[ry-1,rx]==img[ry+1,rx]==img[ry,rx+1]:
            print(str(count/needed*100)+"%")
            # show(cimg, wait=False)
            img[ry,rx]+=1
            cimg[ry,rx]+=1
            cimg[ry,rx,1]=255
            count+=1

    return img,cimg

# 2870,20
# 3556,3681
# 2700,2134
img=cv2.imread("../input_erosion_safe.png",0)

xList=[2870,1974,1005]
yList=[20,2967,2067]
costs=[]

# for n in range(3):
#     img=cv2.imread("../input_erosion_safe.png",0)
#     x=xList.pop(0)
#     y=yList.pop(0)
#
#     rawImg,cimg,cost=dirtDriver(img,x,y)
#     costs.append(cost)
#     cv2.imwrite("raw/site" + str(n) + "-" + str(x) + "-" + str(y) + ".png",rawImg)
#     cv2.imwrite("raw/site" + str(n) + "-" + str(x) + "-" + str(y) + "_color.png",cimg)
#
#     initialRaw=cv2.imread("raw/site" + str(n) + "-" + str(x) + "-" + str(y) + ".png",0)
#     initialColor=cv2.imread("raw/site" + str(n) + "-" + str(x) + "-" + str(y) + "_color.png")
#
#     finalImg,finalColorImg=takeDirt(initialRaw,initialColor,getCostDiff(img,initialRaw),x,y)
#
#     cv2.imwrite("sites/base" + str(n) + "-" + str(x) + "-" + str(y) + ".png",finalImg)
#     cv2.imwrite("sites/base" + str(n) + "-" + str(x) + "-" + str(y) + "_color.png", finalColorImg)


xList=[2870,1974,1005]
yList=[20,2967,2067]
for n in range(3):
    img=cv2.imread("../input_erosion_safe.png",0)
    x=xList.pop(0)
    y=yList.pop(0)

    initialRaw=cv2.imread("raw/site" + str(n) + "-" + str(x) + "-" + str(y) + ".png",0)
    initialColor=cv2.imread("raw/site" + str(n) + "-" + str(x) + "-" + str(y) + "_color.png")

    finalImg,finalColorImg=takeDirt(initialRaw,initialColor,getCostDiff(img,initialRaw),x,y)

    cv2.imwrite("sites/base" + str(n) + "-" + str(x) + "-" + str(y) + ".png",finalImg)
    cv2.imwrite("sites/base" + str(n) + "-" + str(x) + "-" + str(y) + "_color.png", finalColorImg)

print(costs)






# img=cv2.imread("../input_erosion_safe.png",0)
# outImg=cv2.imread("out1.png",0)
# cimg=cv2.imread("colorOut1.png")
# outImg,cimg,cost=dirtDriver(img,2870,20)

# 316451

# print(np.sum(outImg)-np.sum(img))

# print(cost)
# print("Seward Cost: " + str(np.sum(np.abs(outImg-img))))
# cv2.imwrite("out.png",outImg)
# cv2.imwrite("colorOut.png",cimg)
# print(getCostDiff(img,outImg))
# nimg,ncimg=takeDirt(img,cimg,getCostDiff(img,outImg),2870,20)
#
# print(getCostDiff(img,outImg))
# print(patchCheck(outImg,2870,20))

# cimg=cv2.imread("colorOut.png")

# format: img[y,x]

# show(img,wait=True)
# show(cimg,wait=True)

# cv2.imwrite("out5.png",outImg)
# cv2.imwrite("colorOut5.png",cimg)

# some places go from 208 to 206 on the top and right

# 2870,20
# 3556,3681
# 2700,2134

# x=2870
# y=20
#
# img=cv2.imread("../input_erosion_safe.png",0)
# outImg=cv2.imread("site1.png",0)
# cimg=cv2.imread("site1_color.png")
# final=cv2.imread("T1baseSite-2870,20-0.png",0)
#
# print(np.sum(img))
# print(np.sum(final))

# nimg,ncimg=takeDirt(outImg,cimg,getCostDiff(img,outImg),x,y)
# cv2.imwrite("T1baseSite-" + str(x) + "," + str(y) + "-" + str(cost) + ".png",nimg)
# cv2.imwrite("T1baseSite-" + str(x) + "," + str(y) + "-" + str(cost) + "_color.png",ncimg)

# img,cimg,cost=dirtDriver(img,x,y)
#
# cv2.imwrite("site1.png",img)
# cv2.imwrite("site1_color.png",cimg)


# cimg=cv2.imread("RAW_2870-20_color.png")
# outImg=cv2.imread("RAW_2870-20.png",0)
# final=cv2.imread("TbaseSite-2870,20-1382333.png",0)
#
# print(patchCheck(final,x,y))

# print(np.sum(img))
# print(np.sum(final))
#
# cost=getCostDiff(img,outImg)
# nimg,ncimg=takeDirt(img,cimg,getCostDiff(img,outImg),x,y)

# cv2.imwrite("TbaseSite-" + str(x) + "," + str(y) + "-" + str(cost) + ".png",nimg)
# cv2.imwrite("TbaseSite-" + str(x) + "," + str(y) + "-" + str(cost) + "_color.png",ncimg)

# temp=cv2.imread("temp.png")
# nimg,ncimg=takeDirt(img,cimg,getCostDiff(img,outImg),x,y)

# x=2870
# y=20
# outImg,cimg,cost=dirtDriver(img,x,y)
# cv2.imwrite("RAW_" + str(x) + "-" + str(y) + ".png",outImg)
# cv2.imwrite("RAW_" + str(x) + "-" + str(y) + "_color.png",cimg)
# print(getCostDiff(outImg,img))
#
# show(cimg)


# nimg,ncimg=takeDirt(img,cimg,getCostDiff(img,outImg),x,y)
# print(patchCheck(nimg,x,y))
# cv2.imwrite("NbaseSite-" + str(x) + "," + str(y) + "-" + str(cost) + ".png",nimg)
# cv2.imwrite("NbaseSite-" + str(x) + "," + str(y) + "-" + str(cost) + "_color.png",ncimg)
# show(ncimg,wait=True)
#
# img=cv2.imread("../input_erosion_safe.png",0)
#
# x=3556
# y=3681
# outImg,cimg,cost=dirtDriver(img,x,y)
# cv2.imwrite("temp.png",outImg)
# fimg=cv2.imread("temp.png",0)
# cost=getCostDiff(img,fimg)
# nimg,ncimg=takeDirt(fimg,cimg,cost,x,y)
# print(patchCheck(nimg,x,y))
# cv2.imwrite("NbaseSite-" + str(x) + "," + str(y) + "-" + str(cost) + ".png",nimg)
# cv2.imwrite("NbaseSite-" + str(x) + "," + str(y) + "-" + str(cost) + "_color.png",ncimg)
# show(ncimg,wait=True)
#
# img=cv2.imread("../input_erosion_safe.png",0)
#
# x=2700
# y=2134
# outImg,cimg,cost=dirtDriver(img,x,y)
# cv2.imwrite("temp.png",outImg)
# fimg=cv2.imread("temp.png",0)
# cost=getCostDiff(img,fimg)
# nimg,ncimg=takeDirt(fimg,cimg,cost,x,y)
# print(patchCheck(nimg,x,y))
# cv2.imwrite("NbaseSite-" + str(x) + "," + str(y) + "-" + str(cost) + ".png",nimg)
# cv2.imwrite("NbaseSite-" + str(x) + "," + str(y) + "-" + str(cost) + "_color.png",ncimg)
# show(ncimg,wait=True)