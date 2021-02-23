# Assignment: Make a maze using 1 of the 3 main ones and one weird one.
# Perfect Maze
# Animation
# Pretty Colors
# Maze Solved
# Passage Ways green channel>128
# Walls green channel<128

# Classic Maze
# Fancy Maze that interests you
# Colorize different parts of process
# Step-by-step Animation
# On stack colored one way, off stack another
# Lots of info you can embed.
# Path and not path carved out.
# Video should look nice.

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

w=10
h=10
unexplored=254
explored=255
img=np.zeros((h*2+1,w*2+1),dtype=np.uint8)
imgHeight,imgWidth=img.shape
img[1::2,1::2]=254

show(img)


# REcusive backtracking
stack=[(1,1)]
img[1,1]=explored
count=0
while stack:
    x,y=stack[-1]
    possibles=[]
    for dx,dy in (1,0),(-1,0),(0,-1):
        xp=x+dx
        yp=y+dy
        if 0<=xp<=imgWidth and 0<=yp<imgHeight and img[yp,xp]==unexplored:
            possibles.append((xp,yp))
    if possibles:
        xt,yt=random.choice(possibles)
        img[yt,xt]=explored
        img[(y+yt)//2,(x+xt)//2]=explored
        stack.append((xt,yt))
    else:
        stack.pop(-1)
    count+=1
    cv2.imwrite(f"animations/maze{count:05d}.png", img)
    print(count)

show(img)
