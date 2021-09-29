import socket, re
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 50000        # The port used by the server

wordsByLength={}
for line in open("Collins Scrabble Words (2019).txt"):
    word=line.strip()
    if len(word) not in wordsByLength:
        wordsByLength[len(word)]=[]
    wordsByLength[len(word)].append(word);





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
    
def sepMissHit(node,guesses):
    hits=[]
    misses=[]
    for check in guesses:
        if check in node:
            hits.append(check.lower())
        else:
            misses.append(check.lower())

    return misses,hits

def hangman(data):
    word,guesses,guess=re.findall(b"(\w+) \[(\w*),(\w*)\]".decode("utf-8"),data.decode("utf-8"))[0]
    misses,hits=sepMissHit(word,guesses+guess)
    if len(misses)>8:
        return "Hangee Lost."
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
