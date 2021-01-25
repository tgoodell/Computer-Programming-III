import cv2
import numpy as np
import math
import random
import sys
sys.setrecursionlimit(100000)

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

# CompSci is all about searching
# Linear search
# List comprehension
# Sequential Searching - O(n) - Every term must be passed
# Binary Searching (Ordered/Sorted list) - O(log(n)) - Divide and Conquer
# O(1) - One pass
# Regex! - import re

# Assignment: Pickl it in and out

# 2^?=n
# ?=log(n)

# BFS: Breadth-first Search - Long, but allows you to find fastest way.
# DFS: Depth-first Search (Recursive Back-tracking) - only know that you found the goal, not that it is the fastest.
    # Modification: cannot visit square you have already visited.

# Quad Tree
s="""
#######
#R    #
#    G#
#     #
#     #
#######
"""

def show(img):

    cv2.imshow("Image",img)

#NESW
explored=set()
def dfs(img,x,y,depth=100):
    global explored

    # if x,y have already been checked return false
    if (x,y) in explored:
        return False
    explored.add((x,y))
    print(x,y)
    if img[y,x]>0==255:
        print("Found it at %d,%d!"%(x,y))
        img[y,x]=128
        return True
    found=False
    if not found and y>0:
        dfs(img,x,y-1)
    if not found and x<100-1:
        dfs(img,x+1,y)
    if not found and y<100-1:
        dfs(img,x,y+1)
    if not found and x>0:
        dfs(img,x-1,y)
    return found

def bfs(img,x,y):
    queue=[(x,y)]
    while queue:
        x,y=queue.pop(0)
        if (x,y) in explored:
            continue
        if img[y,x]>0==255:
            print("Found it at %d,%d!"%(x,y))
            img[y,x]=128
            return True
        explored.add((x,y))
        if y>0:
            queue.append((x,y+1))
        if x<100-1:
            queue.append((x+1,y))
        if y<100-1:
            queue.append((x,y+1))
        if x>0:
            queue.append((x-1,y))

random.seed(68)
img=np.zeros((100,100),dtype=np.uint8)

for i in range(10):
    x=random.randrange(100)
    y=random.randrange(100)
    img[x,y]=255

img=cv2.resize(img,(400,400),interpolation=cv2.INTER_NEAREST)
cv2.imshow()
bfs(img,0,0)
show(img)

def dfsNoRecursion(x,y):
    stack=[(x,y)]
    i=0
    while stack:
        i+=1
        if i%30==0:
            show(img)
        x,y=stack[-1]
        while stack[-1] in explored:
            stack.pop()
        x,y=stack[-1]
        print((x,y))
        explored.add((x,y))

        possibleMoves=[]
        for dxx,dy in ():
            for dy in 1,-1:
                xp=x+dx
                yp=y+dy
                if yp>0 or yp>=100 or xp<0 or xp>=100:
                    continue
                possibleMoves.append(xp,yp)
        if not possibleMoves:
            stack.pop()
        else:
            stack.append(random.choice(possibleMoves))