# This challenge will have your team create a simple, simulated robot that can be controlled by the user on a play grid.

def toString(board,dimen):
    n=0
    index=0
    while n<dimen:
        k=0
        line=""
        while k<dimen:
            line+=board[index]
            index+=1
            k+=1
        print(line)
        n+=1

def border(board,dimen):
    nlength=len(board)
    n=0
    while n<nlength:
        board[n]="#"
        n+=dimen

    n=0
    while n<nlength-dimen:
        board[n+dimen-1]="#"
        n+=dimen

    for n in range(dimen):
        board[n]="#"

    for n in range(dimen):
        board[nlength-1-n]="#"

    return board

dimen = input("Provide the dimensions of the square grid between 2 and 10 inclusive: ")
while dimen == None or dimen.isdigit() == False or int(dimen)<2 or int(dimen)>10:
    dimen = input("Bad input. Provide the dimensions of the square grid between 2 and 10 inclusive: ")

dimen=int(dimen)+2
board=[]
board+="O"*dimen*dimen

board=border(board,dimen)

toString(board,dimen)