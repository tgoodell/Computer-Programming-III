import socket, re
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 50000        # The port used by the server
import random
import math
import time

# def negamax(node,depth,a=-100000,b=100000):
#     if depth==0:
#         return node.value(),None
#     plays = [*node.getPlays()]
#     if node.isHangmanTurn() and len(plays)==1 and "_" not in plays[0]: # done # terminal node
#         return -10000000-depth, None
#     # bestPlays=plays[0]
#     bestV=-1000000
#     for play in plays: # for every available play from the node
#         child=node.play(play) # Go down to next game.
#         v=-negamax(child.value(),depth-1,-b,-a)[0] # Get eval for the next game.
#         if v>a:
#             a=v
#         if v>=bestV:
#             bestV=v
#             bestPlay=play
#         if a>=b:
#             break
#     return bestV,bestPlay

def sepMissHit(node,guesses):
    hits=[]
    misses=[]
    for check in guesses:
        if check in node:
            hits.append(check.lower())
        else:
            misses.append(check.lower())

    return misses,hits

def genNewDictionary(dictionary,misses,node,guess=""):
    newDict=[]
    for word in dictionary:
        bad=False

        for miss in misses:
            miss=miss[0]
            if miss.upper() in word.upper():
                bad=True
                break
        if not bad:
            for nodeLetter,letter in zip(node,word):
                if nodeLetter.upper()!="_" and letter.upper()!=nodeLetter.upper():
                    bad=True
        if not bad:
            newDict.append(word)

    return newDict,len(newDict)

def getPlays(node,dictionary,misses,guess=""):
    newDictionary,_=genNewDictionary(dictionary,misses,node,guess=guess)
    playDictionary={}
    for word in newDictionary:
        nodifiedWord=""
        for letter,nodeLetter in zip(word,node):
            if letter==nodeLetter:
                nodifiedWord+=letter
            elif nodeLetter=="_" and letter==guess:
                nodifiedWord+=letter
            else:
                nodifiedWord+="_"
        if nodifiedWord not in playDictionary:
            playDictionary[nodifiedWord]=[word]
        else:
            playDictionary[nodifiedWord].append(word)

    return playDictionary

def getMoves(node,misses,plays,maximizer):
    # alpha=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","X","Y","Z"]
    alpha=["E","A","R","I","O","T","U","S","L","C","N","D","P","M","H","G","B","F","Y","W","K","V","X","Z","J","Q"]
    newAlpha=[]
    for letter in alpha:
        if letter not in misses and letter not in node:
            newAlpha.append(letter)

    if not maximizer:
        newAlpha=newAlpha[::-1]

    return newAlpha[:int(math.ceil(len(newAlpha)/2))]

def evalChild(child,node,maximizer):
    if maximizer:
        bestValue=-10000000
    else:
        bestValue=10000000
    bestSubchild=""
    for subchild in child:
        if subchild!=node and subchild!="":
            if maximizer:
                bestValue=max(bestValue,len(child[subchild]))
                if bestValue==len(child[subchild]):
                    bestSubchild=subchild
            else:
                bestValue=min(bestValue,len(child[subchild]))
                if bestValue==len(child[subchild]):
                    bestSubchild=subchild

    return bestSubchild

def minimax(node,depth,maximizer,dictionary,misses):
    # print(depth)
    plays=getPlays(node,dictionary,misses)
    if depth==0 or "_" not in node:
        if maximizer:
            return len(plays[node]), None, None
        else:
            return len(plays[node]), None, None
    if maximizer:
        bestValue=-1000000
        bestSubChild=""
        bestMove=""
        possibleMoves=getMoves(node,misses,plays,maximizer)
        for move in possibleMoves:
            child=getPlays(node,dictionary,misses,guess=move)
            optimalSubChild=evalChild(child,node,maximizer)
            if move not in optimalSubChild:
                misses+=move
            if optimalSubChild!="":
                value,_,_=minimax(optimalSubChild,depth-1,False,dictionary,misses)
                bestValue=max(value,bestValue)
                if bestValue==value:
                    # print(move)
                    bestSubChild=optimalSubChild
                    bestMove=move

        # print(bestMove)
    
    else:
        bestValue=1000000
        bestSubChild=""
        bestMove=""
        possibleMoves=getMoves(node,misses,plays,maximizer)
        for move in possibleMoves:
            child=getPlays(node,dictionary,misses,guess=move)
            optimalSubChild=evalChild(child,node,maximizer)
            if move not in optimalSubChild:
                misses+=move
            if optimalSubChild!="":
                value,_,_=minimax(optimalSubChild,depth-1,True,dictionary,misses)
                bestValue=min(value,bestValue)
                if bestValue==value:
                    # print(move)
                    bestSubChild=optimalSubChild
                    bestMove=move

        # print(bestMove)

    return bestValue,bestMove,bestSubChild

# def negamax(node,depth,dictionary,misses,hangman,a=-100000,b=100000):
#     plays = getPlays(node, dictionary, misses)
#     if depth==0:
#         return len(plays),None, None
#     if hangman and len(plays)==1 and "_" not in node: # done # terminal node
#         return -10000000-depth, None, None
#     # bestPlays=plays[0]
#     bestV=-1000000
#     bestPlay=""
#     bestNode=node
#     possibleMoves = getMoves(node, misses, plays, hangman)
#     for move in possibleMoves: # for every available play from the node
#         child=getPlays(node,dictionary,misses,guess=move) # Go down to next game.
#         optimalSubChild = evalChild(child, node, hangman)
#         v=-negamax(optimalSubChild,depth-1,dictionary,misses,(not hangman),-b,-a)[0] # Get eval for the next game.
#         if v>a:
#             a=v
#         if v>=bestV:
#             bestV=v
#             bestNode=optimalSubChild
#             bestPlay=move
#         if a>=b:
#             break
#     return bestV,bestPlay,bestNode

def hangman(data, sourceDict, currentWord):
    node, guesses, guess = re.findall(b"(\w+) \[(\w*),(\w*)\]".decode("utf-8"), data.decode("utf-8"))[0]
    misses, hits = sepMissHit(node, guesses)

    dictionary,size=genNewDictionary(sourceDict[len(node)],guesses,node)
    print(len(dictionary))

    if len(misses)>8:
        return "Hangee Lost."
    if "_" not in node:
        return "Hangman Lost."

    bestV,bestPlay,bestNode=minimax(node,7,False,dictionary,guesses)

    if guess==bestPlay:
        return bestNode
    else:
        return node

def hangee(data, sourceDict):
    node, guesses = re.findall(b"(\w+) \[(\w*)]".decode("utf-8"), data.decode("utf-8"))[0]
    misses, hits = sepMissHit(node, guesses)

    dictionary,size=genNewDictionary(sourceDict[len(node)],guesses,node)
    print(len(dictionary))

    bestV,bestPlay,bestNode=minimax(node,7,True,dictionary,misses)

    print(bestPlay)

    return bestPlay

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

firstTime=True
currentWord=""

sourceDict={}
for line in open("Collins Scrabble Words (2019).txt"):
    word=line.strip()
    if len(word) not in sourceDict:
        sourceDict[len(word)]=[]
    sourceDict[len(word)].append(word);

while True:
    data = s.recv(1024)
    if(b"," in data):
        x=hangman(data,sourceDict,currentWord)
    else:
        x=hangee(data,sourceDict)
    # ~ print(data)
    print(x)
    s.sendall(x.encode())


