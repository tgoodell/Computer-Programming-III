# One dash = 3 dots
# Space between parts of letter = 1 dot
# Space between two different letters = 3 dots
# Space = / = 7 dots

import cv2
import numpy as np
import math

DEBUG=True

def show(img,title="image",wait=True,time=0):
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
        cv2.waitKey(time)

def normalize(img):
    img_copy=img*1.0
    img_copy-=np.min(img_copy)
    img_copy/=np.max(img_copy)
    img_copy*=255.9999
    return np.uint8(img_copy)

A="._"
B="_..."
C="_._."
D="_.."
E="."
F=".._."
G="__."
H="...."
I=".."
J=".___"
K="_._"
L="._.."
M="__"
N="_."
O="___"
P=".__."
Q="__._"
R="._."
S="..."
T="_"
U=".._"
V="..._"
W=".__"
X="_.._"
Y="_.__"
Z="__.."
zero="_____"
one=".____"
two="..___"
three="...__"
four="...._"
five="....."
six="_...."
seven="__..."
eight="___.."
nine="____."
endMsg="._.__."
betweenLetters="|"
space="/"
period="._._._"

morseLookup=[A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,space,zero,one,two,three,four,five,six,seven,eight,nine,period]
alphaLookup=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"," ","0","1","2","3","4","5","6","7","8","9","."]

message=input("Type in your message: ")
message=message.upper()

morseMessage=""
for letter in message:
    for aletter in alphaLookup:
        if letter==aletter:
            morseMessage = morseMessage + morseLookup[alphaLookup.index(aletter)] + betweenLetters

morseMessage+=endMsg

black=np.zeros((512,512,3),dtype=np.uint8)
white=np.ones((512,512,3),dtype=np.uint8)*255

light=cv2.imread("leaf-present.png")
dark=cv2.imread("leaf-gone.png")

dotLength=10
dashLength=3*dotLength

show(white)

height,width,layers=light.shape

video = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"MJPG"),30,(width,height))

for symbol in morseMessage:
    print(symbol)
    if symbol==".":
        for frame in range(dotLength//30):
            video.write(light)
        # show(light,wait=False,time=dotLength)
    if symbol=="_":
        for frame in range(dashLength//30):
            video.write(light)
        # show(light,wait=False,time=dashLength)
    if symbol=="|":
        for frame in range(dotLength//30):
            video.write(dark)
        # show(dark,wait=False,time=dotLength)
    if symbol=="/":
        for frame in range(dotLength*7//30):
            video.write(dark)
        # show(dark,wait=False,time=dotLength*7)
    for frame in range(dotLength//2//30):
        video.write(dark)
    # show(dark,wait=False,time=dotLength//2)

cv2.destroyAllWindows()
video.release()