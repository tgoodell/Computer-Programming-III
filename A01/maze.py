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

# Recursive Backtracking
# Right/Left hand Maze Following
# Dead end filling
# Checkout: flood filling


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

def workerRB(board,x,y):
    # 01234 : NESW
    badDirection=True
    while badDirection:
        direction=random.randint(0,3)
        if direction==0 and board[y-1,x]==255:
            pass
        elif direction==1 and board[y,x+1]==255:
            pass
        elif direction==2 and board[y+1,x]==255:
            pass
        elif direction==3 and board[y,x-1]==255:
            pass
        else:
            badDirection=False

    if direction==0 and board[y-2,x]==254:
        board[y-2:y,x]!=0
        workerRB(board,x,y-2)
    elif direction==1 and board[y,x+2]==254:
        board[y,x:x+2]!=0
        workerRB(board,x+2,y)
    elif direction==2 and board[y+2,x]==254:
        board[y:y+2,x]!=0
        workerRB(board,x,y+2)
    elif direction==3 and board[y,x-2]==254:
        board[y,x-2:x]!=0
        workerRB(board,x-2,y)
    else:
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
    return (dir+2)%3

def wallFollower(maze,cmaze):
    # If left is free:
    #     Turn Left
    # Else if left is occupied and straight is free:
    #     Go Straight
    # Else if left and straight are occupied:
    #     Turn Right
    # Else if left/right/straight are occupied or you crashed:
    #     Turn 180 degrees

    h,w=maze.shape

    x,y=0,1
    dir=2
    count=0
    while cmaze[h-2,w-2,2]>0:
        if x==w-1:
            x-=1
        if y==h-1:
            y-=1
        if leftFree(dir,maze,x,y):
            dir=turnLeft(dir)
            x,y=moveStraight(dir,x,y)
            cmaze[y,x,2]-=70
        elif straightFree(dir,maze,x,y):
            while straightFree(dir,maze,x,y) and not leftFree(dir,maze,x,y):
                x,y=moveStraight(dir,x,y)
                cmaze[y,x,2]-=70
        elif rightFree(dir,maze,x,y):
            dir=turnRight(dir)
            x,y=moveStraight(dir,x,y)
            cmaze[y,x,2]-=70
        else:
            dir=(dir+2)%3
            x,y=moveStraight(dir,x,y)
            cmaze[y,x,2]-=70


        if count%1000==0:
            show(cv2.resize(cmaze, dsize=(20 * 1920, 20 * 1080), interpolation=cv2.INTER_AREA), wait=False)
            print(x,y)
        count+=1


def tremaux(maze,cmaze):
    # Choose Random Direction
    # Walk straight until you get to dead end.
    # Mark Location
    # Go left, right, or backwards.
    # If you encounter a deadend again, mark it

    x=1
    y=1

    h,w=maze.shape

    while x!=w-1 and y!=y-1:
        dir=random.randint(0,3)
        # Go North
        if dir==0 and maze[y-1,x]>253:
            while maze[y-1,x]>253:
                y-=1
                cmaze[y,x,2]=0
            maze[y-1,x]-=1
        # Go East
        elif dir==1 and maze[y,x-1]>253:
            while maze[y,x+1]>253:
                x+=1
                cmaze[y,x,2]=0
            maze[y,x+1]-=1
        # Go South
        elif dir==2 and maze[y+1,x]>253:
            while maze[y+1,x]>253:
                y+=1
                cmaze[y,x,2]=0
            maze[y+1,x]-=1
        # Go West
        elif dir==3 and maze[y,x-1]>253:
            while maze[y,x-1]>253:
                x-=1
                cmaze[y,x,2]=0
            maze[y,x-1]-=1
        show(cv2.resize(cmaze, dsize=(20 * 1920, 20 * 1080), interpolation=cv2.INTER_AREA), wait=False)

def mazeFollow(maze):
    h,w=maze.shape
    print(h,w)

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

maze=cv2.imread("rb-maze.png",0)
mazeFollow(maze)

# recursiveBacktracking(1920,1080)
# maze=recursiveBacktracking(1920,1080)
# cmaze=cv2.cvtColor(maze,cv2.COLOR_GRAY2BGR)
#
# wallFollower(maze,cmaze)

# cap = cv2.VideoCapture("rb-maze.avi")
#
# out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc(*"MJPG"), 30, (1920,1080))
#
# while True:
#     ret, frame = cap.read()
#     if ret == True:
#         b = cv2.resize(frame,(1920,1080),fx=0,fy=0, interpolation = cv2.INTER_AREA)
#         out.write(b)
#     else:
#         break
#
# cap.release()
# out.release()
# cv2.destroyAllWindows()