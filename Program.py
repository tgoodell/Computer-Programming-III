import cv2
import numpy as np
import math
import random

# 410 x 410 image to perform calculations. When finding spot, look for plot that is fairly flat. Looking for min and max fairly the same.
# Down sample.
# Don't check every spot. Spot check every so often to find areas for further search.
# 100x100 blocks and kill off places with bad standard deviations

# Fancy Algorithm Cost
# allow dirt to errode and fall into place until no errosion. Recursion.
# build a pyramid, randomly extract dirt from board.
# have an inverse strcuture somewhere else on the board to get dirt as you build pyramid.
# build in corner so you only have to deal with two sides to prevent erosion.

# down sample image
# look for roughly good solutions and look at specifics later
# hill climbing (sledding) - gradient descent

# serielization - turn object into linear bytes that can then be written to file


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

def showPatch(img,x,y):
    nimg=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    nimg[y:y+400,x:x+400,2]=255
    show(nimg)

def makePatch(img,x,y):
    patch=1*img[y:y+400,x:x+400]
    print(np.std(patch))
    showPatch(img,x,y)
    patch[:,:]=int(np.average(patch))
    final=np.sum(patch)
    original=np.sum(img[y:y+400,x:x+400])
    cost=2*(original-final)
    print(cost)
    print("---")

def flattenArea(img,x,y):
    nimg=1*img

    patch=nimg[y:y+400,x:x+400]
    patch[:,:]=int(np.average(patch))
    nimg[y:y+400,x:x+400]=int(np.average(patch))
    final=np.sum(patch)
    original=np.sum(img[y:y+400,x:x+400])
    cost=2*(original-final)
    print(cost)
    dugPixels=original-final

    print(dugPixels)

    cimg=cv2.cvtColor(nimg,cv2.COLOR_GRAY2BGR)
    cimg[y:y+400,x:x+400,2]=255

    count=0
    while count<dugPixels:
        rx=random.randrange(2,4095)
        ry=random.randrange(2,4095)
        randPixel=nimg[ry,rx]

        if (rx>x and x<rx+400) or (ry>y and y<ry+400):
            pass
        elif randPixel==nimg[ry,rx-1]==nimg[ry-1,rx]==nimg[ry+1,rx]==nimg[ry,rx+1]:
            nimg[ry,rx]+=1
            cimg[ry,rx]+=1
            cimg[ry,rx,1]=255
            count+=1

    print(np.sum(img)-np.sum(nimg))
    return cimg





img=cv2.imread("input_erosion_safe.png",0)

# makePatch(img,2176,2900) # 9.170559336623008 | 180406.0 Accorns
# makePatch(img,3681,3556) # 3.4071271768713007 | 109432.0 Accorns
# makePatch(img,2475,441) # 4.04746946366936 | 310482.0 Accorns

show(flattenArea(img,3681,3556))

cv2.imwrite("out.png",flattenArea(img,3681,3556))



# candidates=np.empty(0)
# iValues=np.empty(0)
# jValues=np.empty(0)
# print(candidates)
#
# i=2904
# while i<3437-400:
#     j=1639
#     while j<2662-400:
#         nimg=1.0*img
#         patch=nimg[i:i+400,j:j+400]
#         patch[:,:]=int(np.average(patch))
#
#         if np.std(patch)<=1:
#             np.append(candidates,np.std(patch))
#             np.append(iValues,i)
#             np.append(jValues,j)
#         show(nimg)
#         j+=1
#     i+=1
#
# print(candidates)
# print(iValues)
# print(jValues)

