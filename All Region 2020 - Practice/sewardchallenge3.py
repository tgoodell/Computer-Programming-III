# Time: 11 minutes

def checkLeft(upperLeft):
    loopInvalid=False
    if "," in upperLeft:
        upperLeft = upperLeft.split(",")
    while len(upperLeft) != 2 or loopInvalid:
        print("Upper Left coordinate is invalid. Please use the format (x,y).")
        upperLeft = input("Upper Left Coordinate: ")
        if "," in upperLeft:
            loopInvalid=False
            upperLeft = upperLeft.split(",")
        else:
            loopInvalid=True
    upperLeft[0] = upperLeft[0].replace('(', '')
    upperLeft[1] = upperLeft[1].replace(')', '')
    upperLeft[0] = upperLeft[0].replace(' ', '')
    upperLeft[1] = upperLeft[1].replace(' ', '')

    return upperLeft

def checkRight(lowerRight):
    loopInvalid = False
    if "," in lowerRight:
        lowerRight = lowerRight.split(",")
    while len(lowerRight) != 2 or loopInvalid:
        print("Lower Right coordinate is invalid. Please use the format (x,y).")
        lowerRight = input("Lower Right Coordinate: ")
        if "," in lowerRight:
            loopInvalid=False
            lowerRight = upperLeft.split(",")
        else:
            loopInvalid=True
    lowerRight[0] = lowerRight[0].replace('(', '')
    lowerRight[1] = lowerRight[1].replace(')', '')
    lowerRight[0] = lowerRight[0].replace(' ', '')
    lowerRight[1] = lowerRight[1].replace(' ', '')

    return lowerRight

def count(board,color):
    counter=0
    n=0
    while n<100:
        k=0
        while k<100:
            if board[n][k]==color:
                counter+=1
            k+=1
        n+=1
    return counter

print("Welcome!")
print("This program provides the coverage of multiple rectangles of differing colors given an upper left and upper right coordinate of each rectangle.")
print("All numbers must be 0 to 100 inclusive.")
print("Please provide coordinates in the format of (x,y).")
print("---")

coords=[]

addTrue=True
while addTrue:
    ncorrect=True
    while ncorrect:
        upperLeft = input("Upper Left Coordinate: ")
        lowerRight = input("Lower Right Coordinate: ")
        rectColor = input("Rectangle Color: ")
        upperLeft = checkLeft(upperLeft)
        lowerRight = checkRight(lowerRight)
        if upperLeft[0] >= lowerRight[0] and upperLeft[1] <= lowerRight[1]:
            print("ERROR: Lower left and upper right are not in order.")
        else:
            coords.append(upperLeft)
            coords.append(lowerRight)
            coords.append(rectColor)
            ncorrect=False

    another=input("Add another (Y/N): ")

    if another=="N":
        addTrue=False

colors=[]
for n in range(len(coords)//3):
    if coords[n*3+2] not in colors:
        colors.append(coords[n*3+2])

board = [[0 for x in range(100)] for y in range(100)]

print(coords)
print(colors)

for n in range(len(coords)//3):
    upperLeftCoord=coords.pop(0)
    bottomRightCoord=coords.pop(0)
    rectangleColor=coords.pop(0)

    ux=int(upperLeftCoord[0])
    uy=int(upperLeftCoord[1])

    bx=int(bottomRightCoord[0])
    by=int(bottomRightCoord[1])

    k=by
    while k<uy:
        i=ux
        while i<bx:
            board[k][i]=rectangleColor
            i+=1
        k+=1

print("---")

print("Rectangle Coverage")

for color in colors:
    print(str(color) + ": " + str(count(board,color)))