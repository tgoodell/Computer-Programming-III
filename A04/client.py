import socket, re
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 50000        # The port used by the server

wordsByLength={}
for line in open("dictionary.txt"):
    word=line.strip()
    if len(word) not in wordsByLength:
        wordsByLength[len(word)]=[]
    wordsByLength[len(word)].append(word);

def genNewDictionary(dictionary,misses,node,guess=""):
    newDict=[]
    for word in dictionary:
        bad=False

        for miss in misses:
            miss=miss[0]
            if miss in word:
                bad=True
                break
        if not bad:
            for lettern,letter in zip(node,word):
                if lettern=="_" or letter==lettern or letter==guess:
                    pass
                else:
                    bad=True
        if not bad:
            newDict.append(word)

    return newDict,len(newDict)

def maximizer(node,dictionary,misses,hits):
    alpha={"a","b","c","d","e","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","x","y","z"}
    # alpha = cutAlpha(dictionary, alpha)
    # tdictionary=[]
    if misses:
        for n in misses:
            if n in alpha:
                alpha.remove(n)
    bestSize=0
    bestGuess="-1"
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
    bestGuess="-1"
    for letter in alpha:
        _,newSize=genNewDictionary(dictionary,misses,node,guess=letter)
        bestSize=min(newSize,bestSize)
        if bestSize==newSize and letter not in hits:
            bestGuess=letter
    return bestGuess

def minimax(node,depth,maxer,dictionary,misses,hits):
    if depth==0 or len(dictionary)==1:
        return 0
    if maxer:
        bestGuess=maximizer(node,dictionary,misses,hits)
        dict,_=genNewDictionary(dictionary,misses,node,guess=bestGuess)
        minimax(node,depth-1,False,dict,misses,hits)

    else:
        bestGuess=minimizer(node, dictionary, misses, hits)
        dict,_=genNewDictionary(dictionary,misses,node,guess=bestGuess)
        minimax(node,depth-1,True,dict,misses,hits)
    return bestGuess

def getWordGroup(progress,currentDict):
    newDict={}
    for word in currentDict:
        bad=False
        for letter,cletter in word,progress:
            if cletter!="_" and cletter==letter:
                pass
            else:
                bad=True
        if not bad:
            newDict.append(word)

    return newDict

def sepMissHit(node,guesses):
    hits=[]
    misses=[]
    for check in guesses:
        if check in node:
            hits.append(check)
        else:
            misses.append(check)

    return misses,hits

def hangman(data,dictionary):
    word,guesses,guess=re.findall(b"(\w+) \[(\w*),(\w*)\]".decode("utf-8"),data.decode("utf-8"))[0]
    misses,hits=sepMissHit(word,guesses)
    dict,_=genNewDictionary(dictionary,misses,word,guess=guess)
    bestGuess=minimax(guess,26,True,dict,misses,hits)

    if bestGuess==guess:
        return word+" "+guesses
    
    return bestReturn(word,guesses,guess)[0]

def hangee(data):
    word,guesses=re.findall(b"(\w+) \[(\w*)]".decode("utf-8"),data.decode("utf-8"))[0]


# ~ print(hangman(b"TOAD_ [ABCSREILNUOGDT,Y]"))
# ~ print(hangee(b"TOAD_ [ABCSREILNUOGDT]"))



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
    data = s.recv(1024)
    x=""
    if(b"," in data):
        x=hangman(data)
    else:
        x=hangee(data)
    # ~ print(data)
    s.sendall(x.encode())
