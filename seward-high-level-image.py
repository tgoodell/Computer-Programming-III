import cv2
import numpy as np
import math

# Integral Image
# O(1) using Integral Image and lookup
# Lookup tables

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

scale=5
d=400//scale

img=cv2.imread("input_erosion_safe.png")[::scale,::scale]
h,w=img.shape[:2]
out=np.zeros((h-d,w-d))

for row in range(h-d):
    print(row)
    for col in range(w-d):
        s=np.std(img[row:row+d,col:col+d])
        out[row,col]=s

print(np.where(out==out.min()))

# out-=out.min()
out/=out.max()
out*=255
out=np.uint8(out)

show(out) # Darker/Blacker is better, lower Stdev
