import cv2
import numpy as np
import random
import math

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

def genBoard(width,height):
    w=width//20
    h=height//20

    board=np.zeros((h*2+1,w*2+1),dtype=np.uint8)
    board[1::2,1::2]=254

    return board

def sewardMaze(width,height):
    imgWidth=width//20
    imgHeight=height//20
    unexplored=254
    explored=255

    img=genBoard(width,height)

    stack=[(1,1)]
    img[1,1]=explored
    count=0
    while stack:
        index=random.randrange(len(stack))*0+-1
        x,y=stack[index]
        possibles=[]
        for dx,dy in (1,0),(-1,0),(0,1),(0,-1):
            xp=x+2*dx
            yp=y+2*dy

            if 0<=xp<imgWidth and 0<=yp<imgHeight and img[yp,xp]==unexplored:
                possibles.append((xp,yp))
        if possibles:
            xt,yt=random.choice(possibles)
            img[yt,xt]=explored
            img[(y+yt)//2,(x+xt)//2]=explored
            stack.append((xt,yt))
        else:
            stack.pop(index)
        # cv2.imwrite(f"animation/maze{count:05d}.png",img)
        show(cv2.resize(img,dsize=(20*imgWidth,20*imgHeight),interpolation=cv2.INTER_AREA),wait=False)
        count+=1
        print(count)

# Recursive Backtracking
# Right/Left hand Maze Following
# Dead end filling
# Checkout: flood filling


def sidewinder(width,height):
    # 1.) Work through the grid row-wise, starting with the cell at 0,0. Initialize the “run” set to be empty.
    # 2.) Add the current cell to the “run” set.
    # 3.) For the current cell, randomly decide whether to carve east or not.
    # 4.) If a passage was carved, make the new cell the current cell and repeat steps 2-4.
    # 5.) If a passage was not carved, choose any one of the cells in the run set and carve a passage north. Then empty the run set, set the next cell in the row to be the current cell, and repeat steps 2-5.
    # 6.) Continue until all rows have been processed.

    board=genBoard(width,height)
    cboard=cv2.cvtColor(board,cv2.COLOR_GRAY2BGR)

    run=[]

    h,w=board.shape

    board[1,1:w-1]=255

    k=3
    while k<h:
        n=1
        while n<w-1:
            run.append(n-1)
            if random.randint(0,1)==1 and n<w-2:
                # cboard[k,n:n+1,2]=255
                board[k,n+1]=255
            else:
                first=run[0]
                last=run[-1]

                # if board[k-2,random.randint(first,last)]==254:
                board[k-1,random.randint(first,last)]=255

                # cboard=cv2.cvtColor(board,cv2.COLOR_GRAY2BGR)
                run=[]
            # show(cv2.resize(cboard, dsize=(20 * width, 20 * height), interpolation=cv2.INTER_AREA), wait=False)
            n+=2
        run=[]
        k+=2

    cv2.imwrite("maze.png",board)
    show(cv2.resize(board, dsize=(20 * width, 20 * height), interpolation=cv2.INTER_AREA), wait=True)

        
sidewinder(1920,1080)

