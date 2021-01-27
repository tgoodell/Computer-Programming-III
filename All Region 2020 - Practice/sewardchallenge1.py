# Time: 25 minutes

# a.) specify Upper left and Lower Right of Rectangle, give area. Heavy User Interface. Rectangle Area Finder. Input: (3, 4) , (7,8)
    # Correctly Calculate Area
    # Right Format
    # Invalid points - not upper left and lower right
    # Meaningful Error Message

# b.) Specify multiple rectangles. Calculate coverage area.

# c.) Add color. Provide coordinates and color. Report back coverage area of each color.

print("Welcome!")
print("This program provides the area of a rectangle given an upper left and upper right coordinate.")
print("All numbers must be 0 to 100 inclusive.")
print("Please provide coordinates in the format of (x,y).")
print("---")
upperLeft=input("Upper Left Coordinate: ")
lowerRight=input("Lower Right Coordinate: ")

upperLeft=upperLeft.split(",")
while len(upperLeft)!=2:
    print("Upper Left coordinate is invalid. Please use the format (x,y).")
    upperLeft=input("Upper Left Coordinate: ")
    upperLeft=upperLeft.split(",")

lowerRight=lowerRight.split(",")
while len(lowerRight)!=2:
    print("Lower Right coordinate is invalid. Please use the format (x,y).")
    lowerRight=input("Lower Right Coordinate: ")
    lowerRight=lowerRight.split(",")

# Get rid of not relevant chars
upperLeft[0]=upperLeft[0].replace('(', '')
upperLeft[1]=upperLeft[1].replace(')', '')
upperLeft[0]=upperLeft[0].replace(' ', '')
upperLeft[1]=upperLeft[1].replace(' ', '')
lowerRight[0]=lowerRight[0].replace('(', '')
lowerRight[1]=lowerRight[1].replace(')', '')
lowerRight[0]=lowerRight[0].replace(' ', '')
lowerRight[1]=lowerRight[1].replace(' ', '')

if upperLeft[0]>=lowerRight[0] or upperLeft[1]>=lowerRight[1]:
    print("ERROR: Lower left and upper right are not in order.")

while upperLeft[0]>=lowerRight[0] or upperLeft[1]>=lowerRight[1]:
    upperLeft = input("Upper Left Coordinate: ")
    lowerRight = input("Lower Right Coordinate: ")

    upperLeft = upperLeft.split(",")
    while len(upperLeft) != 2:
        print("Upper Left coordinate is invalid. Please use the format (x,y).")
        upperLeft = input("Upper Left Coordinate: ")
        upperLeft = upperLeft.split(",")

    lowerRight = lowerRight.split(",")
    while len(lowerRight) != 2:
        print("Lower Right coordinate is invalid. Please use the format (x,y).")
        lowerRight = input("Lower Right Coordinate: ")
        lowerRight = lowerRight.split(",")

    # Get rid of not relevant chars
    upperLeft[0] = upperLeft[0].replace('(', '')
    upperLeft[1] = upperLeft[1].replace(')', '')
    upperLeft[0] = upperLeft[0].replace(' ', '')
    upperLeft[1] = upperLeft[1].replace(' ', '')
    lowerRight[0] = lowerRight[0].replace('(', '')
    lowerRight[1] = lowerRight[1].replace(')', '')
    lowerRight[0] = lowerRight[0].replace(' ', '')
    lowerRight[1] = lowerRight[1].replace(' ', '')

length=int(lowerRight[0])-int(upperLeft[0])
height=int(lowerRight[1])-int(upperLeft[1])
area=length*height

print(area)

# 20 mins