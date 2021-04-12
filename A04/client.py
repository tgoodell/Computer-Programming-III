import socket, re
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 50000        # The port used by the server
import random
import time

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
            for lettern,letter in zip(node.upper(),word.upper()):
                if lettern=="_" or letter==lettern or letter==guess.upper():
                    pass
                else:
                    bad=True
        if not bad:
            newDict.append(word)

    return newDict,len(newDict)

def maximizer(node,dictionary,misses,hits):
    alpha={"a","b","c","d","e","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","x","y","z"}

    if misses:
        for n in misses:
            if n in alpha:
                alpha.remove(n)
    bestSize=0
    bestGuess=""
    for letter in alpha:
        _,newSize=genNewDictionary(dictionary,misses,node,guess=letter)
        bestSize=max(newSize,bestSize)
        if bestSize==newSize and letter not in hits:
            bestGuess=letter
    return bestGuess

def minimizer(node,dictionary,misses,hits):
    alpha={"a","b","c","d","e","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","x","y","z"}
    if misses:
        for n in misses:
            if n in alpha:
                alpha.remove(n)
    bestSize=100000000
    bestGuess=""
    for letter in alpha:
        _,newSize=genNewDictionary(dictionary,misses,node,guess=letter)
        bestSize=min(newSize,bestSize)
        if bestSize==newSize and letter not in hits:
            bestGuess=letter
        # print(bestGuess)
    return bestGuess.upper()

def negamax(node,depth,a=-100000,b=100000):
    if depth==0:
        return node.value(),None
    plays = [*node.getPlays()]
    if node.isHangmanTurn() and len(plays)==1 and "_" not in plays[0]: # done # terminal node
        return -10000000-depth, None
    # bestPlays=plays[0]
    bestV=-1000000
    for play in plays: # for every available play from the node
        child=node.play(play) # Go down to next game.
        v=-negamax(child.value(),depth-1,-b,-a)[0] # Get eval for the next game.
        if v>a:
            a=v
        if v>=bestV:
            bestV=v
            bestPlay=play
        if a>=b:
            break
    return bestV,bestPlay

# iterative deepening
def deepen(node):
    depth=1
    best=None
    while True:
        start=time.time()
        negamax(node,depth)
        end=time.timte()
        if end-start>1:
            break
        depth+=1
    return [*best,depth]

def minimax(node,depth,maxer,dictionary,misses,hits):
    alpha={"a","b","c","d","e","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","x","y","z"}
    if misses:
        for n in misses:
            if n in alpha:
                alpha.remove(n)
    
    if depth==0 or len(dictionary)==1:
        return -1
    if maxer:
        bestSize = 0
        bestGuess = ""
        for letter in alpha:
            guess, bSize = minimax(node,depth-1,False,dictionary,misses,hits)
            bestSize=max(guess, bestSize)
            if bSize==bestSize and letter not in hits:
                bestGuess = letter
        dict,size=genNewDictionary(dictionary,misses,node,guess=bestGuess)

    else:
        bestSize = 1000000000
        bestGuess = ""
        for letter in alpha:
            guess, bSize = minimax(node, depth - 1, True, dictionary, misses, hits)
            bestSize = min(guess, bestSize)
            if bSize == bestSize and letter not in hits:
                bestGuess = letter
        dict, size = genNewDictionary(dictionary, misses, node, guess=bestGuess)
    return bestGuess,size

def sepMissHit(node,guesses):
    hits=[]
    misses=[]
    for check in guesses:
        if check in node:
            hits.append(check.lower())
        else:
            misses.append(check.lower())

    return misses,hits

def guessLetter(node,word,guess):
    for lettern,letter in zip(node,word):
        if letter==guess:
            node=node[0:word.index(letter)] + letter + node[word.index(letter) + 1:]
    return node.upper()

def hangman(data,dictionary,sourceDict,currentWord):
    word,guesses,guess=re.findall(b"(\w+) \[(\w*),(\w*)\]".decode("utf-8"),data.decode("utf-8"))[0]
    misses,hits=sepMissHit(word,guesses)

    if len(misses)>8:
        return "Hangee Lost.",dictionary,currentWord

    dict,_ = genNewDictionary(sourceDict[len(word)], guesses, word.lower())
        
    bestGuess=minimax(word,3,True,dict,misses,hits)

    if len(dict)>0:
        currentWord=dict[random.randint(0,len(dict)-1)]

    print(currentWord + " " + guesses)
    if bestGuess==-1:
        return "Hangman Lost.",dict,currentWord
    elif bestGuess.upper()==guess.upper():
        return guessLetter(word.lower(),currentWord,bestGuess).upper(),dict,currentWord
    else:
        return word,dict,currentWord

def hangee(data,dictionary,sourceDict):
    word,guesses=re.findall(b"(\w+) \[(\w*)]".decode("utf-8"),data.decode("utf-8"))[0]
    misses,hits=sepMissHit(word,guesses)

    # if len(guesses)==0:

    dict, _ = genNewDictionary(sourceDict[len(word)], misses, word.lower())

    bestGuess=minimax(word,3,False,dict,misses,hits)

    return bestGuess.upper(),dict

sourceDict={}
for line in open("Collins Scrabble Words (2019).txt"):
    word=line.strip()
    if len(word) not in sourceDict:
        sourceDict[len(word)]=[]
    sourceDict[len(word)].append(word);

dictionary=[]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

firstTime=True
currentWord=""

while True:
    data = s.recv(1024)
    if(b"," in data):
        x,dictionary,currentWord=hangman(data,dictionary,sourceDict,currentWord)
        print(x + " " + str(len(dictionary))+"\n")
    else:
        x,dictionary=hangee(data,dictionary,sourceDict)
        print(x + " " + str(len(dictionary))+"\n")
    # ~ print(data)
    s.sendall(x.encode())
