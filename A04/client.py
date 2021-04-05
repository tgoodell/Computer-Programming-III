import socket, re
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 50000        # The port used by the server

wordsByLength={}
for line in open("dictionary.txt"):
    word=line.strip()
    if len(word) not in wordsByLength:
        wordsByLength[len(word)]=[]
    wordsByLength[len(word)].append(word);

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



def isMatch(w,word, goodLetters, badLetters):
    for a,b in zip(w,word):
        if b=="_" and a not in goodLetters|badLetters:
            pass
        elif b!="_" and b==a:
            pass
        else:
            return False
    return True

def mask(word, guesses):
    return "".join("_" if letter not in guesses else letter for letter in word)

def bestReturn(word,guesses,guess):
    goodLetters=set(letter for letter in word if letter!='_')
    badLetters=set(letter for letter in guesses if letter not in goodLetters)
    words=[w for w in wordsByLength[len(word)] if isMatch(w,word, goodLetters, badLetters)]
    # ~ print(words)
    guesses+=guess
    counts={}
    for w in words:
        q=mask(w,guesses)
        if q in counts:
            counts[q]+=1
        else:
            counts[q]=0
    best=0
    bestWord=word
    # ~ print(counts)
    for m in counts:
        if counts[m]>best or (counts[m]==best and bestWord.count("_")>m.count("_")):
            best=counts[m]
            bestWord=m
    return bestWord,best
    

def hangman(data):
    word,guesses,guess=re.findall(b"(\w+) \[(\w*),(\w*)\]".decode("utf-8"),data.decode("utf-8"))[0]
    return bestReturn(word,guesses,guess)[0]

def hangee(data):
    word,guesses=re.findall(b"(\w+) \[(\w*)]".decode("utf-8"),data.decode("utf-8"))[0]
    best="A"
    bestMask=word
    smallest=10**10
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if letter not in guesses:
            currentMask,c=bestReturn(word,guesses,letter)
            # ~ print(letter,bestMask,c,smallest,currentMask)
            if c<smallest or (c==smallest and bestMask.count("_")>currentMask.count("_")):
                best=letter
                bestMask=currentMask
                smallest=c
    # ~ print(smallest)
    return best
# ~ print(hangman(b"TOAD_ [ABCSREILNUOGDT,Y]"))
# ~ print(hangee(b"TOAD_ [ABCSREILNUOGDT]"))

# def minimax(node, depth, maximizingPlayer):
#     if depth==0 or node is a terminal node then
#         return the heuristic value of node
#     if maximizingPlayer:
#         value=-10000000
#         for each child of node do
#             value := max(value, minimax(child, depth − 1, FALSE))
#         return value
#     else:
#         value=10000000
#         for each child of node do
#             value := min(value, minimax(child, depth − 1, TRUE))
#         return value

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
