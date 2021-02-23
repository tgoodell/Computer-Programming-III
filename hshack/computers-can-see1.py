# Program to read a Numpy array and display as image.
# Coded by gm-tristan

import cv2
import numpy as np

def show(img,wait=0,destroy=True):
    img=np.uint8(img)
    cv2.imshow("image",img)
    cv2.waitKey(wait)
    if destroy:
        cv2.destroyAllWindows()

def read(pixels):
    h,w=720,960

    npixels=[]
    index=0
    while index<len(pixels)-1:
        npixels.append(int(pixels[index]))
        index+=1

    npixels.append(1)

    spixels=""
    turn=0
    index=0
    while index<len(pixels)-1:
        if turn%2==1:
            spixels+=npixels[index]*"0"
        elif turn%2==0:
            spixels+=npixels[index]*"1"
        turn+=1
        index+=1

    spixels+="0"

    m = np.array(list(spixels))
    img = np.uint8(np.reshape(m[:h * w], (h, w)) == "1") * 255
    return img

pixels=np.load("flag.npy")
img=read(pixels)

show(img)
