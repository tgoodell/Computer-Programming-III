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

def recursiveBacktracking(width,height):
    unexplored=254
    explored=255

    maze=genBoard(width,height)
    cmaze=cv2.cvtColor(maze,cv2.COLOR_GRAY2BGR)

    darkRed=(12,20,146)
    copper=(77,124,190)

    mazeHeight,mazeWidth=maze.shape
    stack=[(1,1)]
    maze[1,1]=explored
    count=0
    video = cv2.VideoWriter("rb-maze.avi", cv2.VideoWriter_fourcc(*"MJPG"), 60, (1920, 1080))
    while stack:
        index=random.randrange(len(stack))*0+-1
        x,y=stack[index]
        possibles=[]
        for dx,dy in (1,0),(-1,0),(0,1),(0,-1):
            xp=x+2*dx
            yp=y+2*dy

            if 0<=xp<mazeWidth and 0<=yp<mazeHeight and maze[yp,xp]==unexplored:
                possibles.append((xp,yp))
        if possibles:
            xt,yt=random.choice(possibles)
            maze[yt,xt]=explored
            cmaze[yt,xt,:]=darkRed
            maze[(y+yt)//2,(x+xt)//2]=explored
            cmaze[(y+yt)//2,(x+xt)//2,:]=darkRed
            stack.append((xt,yt))
        else:
            x,y=stack[index]
            cmaze[y,x,:]=copper
            stack.pop(index)
        # cv2.imwrite(f"animation/maze{count:05d}.png",img)
        frame=cv2.resize(cmaze, dsize=(1920, 1080), interpolation=cv2.INTER_AREA)
        video.write(frame)
        count+=1
        if count%100==0:
            print(count)
            # show(cv2.resize(cmaze, dsize=(20 * width, 20 * height), interpolation=cv2.INTER_AREA), wait=False)

    show(cv2.resize(cmaze, dsize=(20 * width, 20 * height), interpolation=cv2.INTER_AREA), wait=True)
    cv2.imwrite("rb-maze.png",maze)

def sidewinder(width,height):
    board=genBoard(width,height)
    cboard=cv2.cvtColor(board,cv2.COLOR_GRAY2BGR)
    video = cv2.VideoWriter("sw-maze.avi", cv2.VideoWriter_fourcc(*"MJPG"), 30, (1920, 1080))

    blueCrayola=(217,142,5)
    pistachio=(109,190,144)

    run=[]

    h,w=board.shape

    board[1,1:w-1]=255
    cboard[1,1:w-1,:]=blueCrayola

    k=3
    while k<h:
        n=1
        while n<w-1:
            run.append(n)
            if random.randint(0,1)==1 and n<w-2:
                cboard[k,n,:]=blueCrayola
                cboard[k,n+1,:]=blueCrayola
                board[k,n+1]=255
                # show(cv2.resize(cboard, dsize=(20 * width, 20 * height), interpolation=cv2.INTER_AREA), wait=False)
            else:
                first=run[0]
                last=run[-1]
                cboard[k,n,:]=blueCrayola

                # if board[k-2,random.randint(first,last)]==254:
                badRand=True
                while badRand:
                    place=random.randint(first,last)
                    if place%2==1:
                        board[k-1,place]=255
                        cboard[k-1,place]=pistachio
                        badRand=False
                # show(cv2.resize(cboard, dsize=(20 * width, 20 * height), interpolation=cv2.INTER_AREA), wait=False)

                run=[]
            frame=cv2.resize(cboard, dsize=(1920, 1080), interpolation=cv2.INTER_AREA)
            video.write(frame)
            n+=2
        run=[]
        k+=2

    cv2.imwrite("sw-maze.png",board)
    # show(cv2.resize(board, dsize=(20 * width, 20 * height), interpolation=cv2.INTER_AREA), wait=True)

    return board

def leftFree(dir,maze,x,y):
    if dir==0 and maze[y,x-1]>0:
        return True
    elif dir==1 and maze[y-1,x]>0:
        return True
    elif dir==2 and maze[y,x+1]>0:
        return True
    elif dir==3 and maze[y+1,x]>0:
        return True
    else:
        return False
    
def rightFree(dir,maze,x,y):
    if dir==0 and maze[y,x+1]>0:
        return True
    elif dir==1 and maze[y+1,x]>0:
        return True
    elif dir==2 and maze[y,x-1]>0:
        return True
    elif dir==3 and maze[y-1,x]>0:
        return True
    else:
        return False

def turnLeft(dir):
    dir-=1
    if dir<0:
        dir=3

    return dir

def turnRight(dir):
    dir+=1
    if dir>3:
        dir=0

    return dir

def straightFree(dir,maze,x,y):
    if dir==0 and maze[y-1,x]>0:
        return True
    if dir==1 and maze[y,x+1]>0:
        return True
    if dir==2 and maze[y+1,x]>0:
        return True
    if dir==3 and maze[y,x-1]>0:
        return True
    else:
        return False

def moveStraight(dir,x,y):
    if dir==0:
        y-=1
    elif dir==1:
        x+=1
    elif dir==2:
        y+=1
    elif dir==3:
        x-=1

    return x,y

def turnAround(dir):
    dir+=2
    if dir==5:
        dir=1
    elif dir==4:
        dir=0

    return dir

def randDir(dir,maze,x,y):
    available=[]
    if straightFree(dir,maze,x,y):
        available.append("s")
    if leftFree(dir,maze,x,y):
        available.append("l")
    if rightFree(dir,maze,x,y):
        available.append("r")
    else:
        return turnAround(dir)

    dirChoice=random.randint(0,len(available)-1)

    if dirChoice=="s":
        return dir
    elif dirChoice=="l":
        return turnLeft(dir)
    elif dirChoice=="r":
        return turnRight(dir)


def leftHandFollow(maze):
    h,w=maze.shape

    cmaze=cv2.cvtColor(maze,cv2.COLOR_GRAY2BGR)

    cmaze[1,1,:]=(98,96,213)
    cmaze[h-2,w-2,:]=(11,195,236)
    
    video = cv2.VideoWriter("lefthand-rbSolve.avi", cv2.VideoWriter_fourcc(*"MJPG"), 30, (1920, 1080))

    dir=2
    count=0
    x,y=1,1
    while True:
        if x==w-2 and y==h-2:
            break
        elif leftFree(dir,maze,x,y):
            dir=turnLeft(dir)
            x,y=moveStraight(dir,x,y)
        elif straightFree(dir,maze,x,y):
            x,y=moveStraight(dir,x,y)
        elif rightFree(dir,maze,x,y):
            dir=turnRight(dir)
            x,y=moveStraight(dir,x,y)
        else:
            dir=turnAround(dir)
        cmaze[y,x,1]-=50
        frame=cv2.resize(cmaze, dsize=(1920, 1080), interpolation=cv2.INTER_AREA)
        video.write(frame)
        count+=1

    show(cv2.resize(cmaze, dsize=(20 * 1920, 20 * 1080), interpolation=cv2.INTER_AREA), wait=True)

def deadEndFill(maze):
    h,w=maze.shape
    maze[maze>128]=255
    cmaze=cv2.cvtColor(maze,cv2.COLOR_GRAY2BGR)

    cmaze[1,1,:]=(98,96,213)
    cmaze[h-2,w-2,:]=(11,195,236)
    
    video = cv2.VideoWriter("deadEndFill-swSolve.avi", cv2.VideoWriter_fourcc(*"MJPG"), 24, (1920, 1080))

    count=0
    while True:
        stack=[]

        n=0
        while n<h-1:
            k=0
            while k<w-1:
                if (n==1 and k==1) or (n==h-2 and k==w-2):
                    pass
                elif maze[n,k]>250 and deadEnd(maze,k,n):
                    stack.append((k,n))
                    cmaze[n,k,1]=0
                k+=1
            n+=1
            
        frame=cv2.resize(cmaze, dsize=(1920, 1080), interpolation=cv2.INTER_AREA)
        video.write(frame)

        if len(stack)==0:
            break

        print(len(stack))
        for x in range(len(stack)):
            x,y=stack.pop(0)
            cmaze[y,x,:]=0
            maze[y,x,]=0

        count+=1
        
    dir=2
    count=0
    x,y=1,1
    while True:
        if x==w-2 and y==h-2:
            break
        elif leftFree(dir,maze,x,y):
            dir=turnLeft(dir)
            x,y=moveStraight(dir,x,y)
        elif straightFree(dir,maze,x,y):
            x,y=moveStraight(dir,x,y)
        elif rightFree(dir,maze,x,y):
            dir=turnRight(dir)
            x,y=moveStraight(dir,x,y)
        else:
            dir=turnAround(dir)
        cmaze[y,x,:]=(122,174,124)
        frame=cv2.resize(cmaze, dsize=(1920, 1080), interpolation=cv2.INTER_AREA)
        video.write(frame)
        count+=1
        
    show(cv2.resize(cmaze, dsize=(20 * 1920, 20 * 1080), interpolation=cv2.INTER_AREA), wait=True)

def deadEnd(maze,x,y):
    check=maze[y-1,x]+maze[y+1,x]+maze[y,x-1]+maze[y,x+1]
    if check==255:
       return True
    else:
        return False

sidewinder(1920,1080)
maze=cv2.imread("sw-maze.png",0)
deadEndFill(maze)

recursiveBacktracking(1920,1080)
maze=cv2.imread("rb-maze.png")
leftHandFollow(maze)
