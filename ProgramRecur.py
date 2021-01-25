import cv2
import numpy as np
import math

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

def evalFlatten(img,x,y):
    nimg=1*img
    patch=nimg[y:y+400,x:x+400]
    avg=int(np.average(patch))

    h,w=patch.shape[:2]
    n=0
    cost=0
    while n<h:
        k=0
        while k<w:
            diff=np.abs(patch[n,k]-avg)
            # cpatch[n,k,2]=255
            # show(cpatch)
            cost+=diff
            k+=1
        n+=1
    return 2*cost

def flatten(img,x,y):
    nimg=1*img
    patch=nimg[y:y+400,x:x+400]
    avg=int(np.average(patch))
    flattenCost=evalFlatten(nimg,x,y)

    cpatch = cv2.cvtColor(patch, cv2.COLOR_GRAY2BGR)

    nimg[y:y+400,x:x+400]=int(avg)
    cimg=cv2.cvtColor(nimg, cv2.COLOR_GRAY2BGR)

    # Top
    n=0
    while n<400:
        k=0
        if nimg[y-k,n]>nimg[y-k+1,n]+1 or nimg[y-k,n]<nimg[y-k+1,n]-1:
            nimg[y-k,n]=nimg[y-k+1,n]-1
            cimg[y-k,n,:]=cimg[y-k+1,n,:]-1
            cimg[y-k,n,2]=255
            show(cimg,wait=False)
            k+=1
        n+=1

    show(nimg)


# makePatch(img,2176,2900) # 9.170559336623008 | 180406.0 Accorns
# makePatch(img,3681,3556) # 3.4071271768713007 | 109432.0 Accorns
# makePatch(img,2475,441) # 4.04746946366936 | 310482.0 Accorns

img=cv2.imread("../input_erosion_safe.png",0)

flatten(img,3681,3556)

cimg=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

