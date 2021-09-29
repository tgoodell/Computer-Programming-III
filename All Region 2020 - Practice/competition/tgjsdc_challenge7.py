'''
Arkansas School for Mathematics Sciences and the Arts
Tristan Goodell
David Clark
Joshua Stallings
'''

def intToString(x,base):
    letterSet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    out=""
    while x:
        out=letterSet[x%base]+out
        x//=base
    if not out:
        return 0
    return out

# word equations
# BOOK + READ = BLAM

import math

validMoves=["1","2","3","4"]

repeat=True
while repeat:
    hexCoords=input("Please provide Hexilian Coordinates: ")
    
    hexCoordMoves=[]
    for coord in hexCoords:
        if coord not in validMoves:
            print(coord + " is not a valid coordniate. So, it will be ignored.")
        else:
            hexCoordMoves.append(coord)
    
    citySize=math.pow(4,len(hexCoordMoves))
    width=citySize/2
    height=citySize/2
    
    xMoves=[]
    yMoves=[]
    n=width*(-1)//2
    while n<=width//2:
        if n==0:
            n=1
        xMoves.append(n)
        yMoves.append(n)
        n+=1

    passes=0

    n=0
    while 0<len(hexCoordMoves):
        hexCoordPoint=hexCoordMoves.pop(0)
        print(xMoves,yMoves)
        if hexCoordPoint=="1":
            k=0
            while k<width//2:
                yMoves.pop(0)
                xMoves.pop(0)
                k+=1
        elif hexCoordPoint=="2":
            k=0
            while k<width//2:
                yMoves.pop(0)
                xMoves.pop()
                k+=1
        elif hexCoordPoint=="3":
            k=0
            while k<width//2:
                yMoves.pop()
                xMoves.pop()
                k+=1
        elif hexCoordPoint=="4":
            k=0
            while k<width//2:
                yMoves.pop()
                xMoves.pop(0)
                k+=1
        width=width//2
        height=height//2
        n+=1
    
    
    print(xMoves,yMoves)

    x=xMoves[0]
    y=yMoves[0]
    cartesianCoords=x,y
    
    sides=citySize/2
    
    print("Hexilian: " + str(hexCoords) + " --> Coordinate Address: " + str(cartesianCoords))
    print("Total Hexilian Buildings: " + str(citySize))
    
    badRepeatAnswer=True
    while badRepeatAnswer:
        repeatAnswer=input("Would you like to enter another address (Y/N)? ")

        if repeatAnswer=="Y" or repeatAnswer=="y":
            badRepeatAnswer=False
            print("\nAwesome!\n---\n")
        elif repeatAnswer=="N" or repeatAnswer=="n":
            badRepeatAnswer=False
            repeat=False
        else:
            print("Invalid answer.")

print("bye!")