import random

# Hangman Questions
# Is it Computer vs Human or Computer vs Computer?
#

def genBoard(missNum):
    if missNum==0:
        board='''
    __________
     |/      |
     |     
     |      
     |       
     |      
     |
    _|___'''

    elif missNum==1:
        board='''
    __________
     |/      |
     |     (;_;)
     |      
     |       
     |      
     |
    _|___'''

    elif missNum==2:
        board='''
    __________
     |/      |
     |     (;_;)
     |       |
     |       |
     |      
     |
    _|___'''

    elif missNum==3:
        board='''
    __________
     |/      |
     |     (;_;)
     |      \|
     |       |
     |      
     |
    _|___'''

    elif missNum==4:
        board='''
    __________
     |/      |
     |     (;_;)
     |      \|/
     |       |
     |      
     |
    _|___'''

    elif missNum==5:
        board='''
    __________
     |/      |
     |     (;_;)
     |      \|/
     |       |
     |      /
     |
    _|___'''

    elif missNum==6:
        board='''
    __________
     |/      |
     |     (;_;)
     |      \|/
     |       |
     |      / \\
     |
    _|___'''

    return board

def readDictionary():
    with open("Collins Scrabble Words (2019).txt") as f:
        words = f.readlines()
        dictionary=[]
        for word in words:
            dictionary.append(word.replace("\n","").lower())

        dictionary=dictionary[2:]

    return dictionary

def randomWord(dictionary):
    return dictionary[random.randint(0,len(dictionary)-1)]

def guessLetter(guess,word,progress):
    wincon=False
    if guess in word:
        if guess==word:
            wincon=True
        n=0
        for letter in word:
            if letter==guess:
                progress[n]=guess
            n+=1
        return True, wincon, progress
    else:
        return False, wincon, progress

def toString(array):
    word=""
    for letter in array:
        word+=letter
    return word

def missesToString(missList):
    misses=""
    for miss in missList:
        misses+=miss+", "
    return misses[:-2]

def miniMax(word,progress,depth,maximizingPlayer):
    alpha=["a","b","c","d","e","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","x","y","z"]
    if depth==0: # or node is a terminal node then
        return 0 # heuristic
    if maximizingPlayer:
        value=-10000000
        for letter in alpha:
            bullseye, wincon, progress = guessLetter(letter, word, progress)
            temp,_=miniMax(word,progress,depth-1,False)
            if temp>value:
                value=temp
                guess=letter
    elif not maximizingPlayer:
        value=10000000
        guess=""
        for letter in alpha:
            bullseye, wincon, progress = guessLetter(guess, word, progress)
            temp,_=miniMax(word,progress,depth-1,True)
            if temp<value:
                value=temp
                guess=letter
        return value,guess

def getWordGroup(guess,progress,currentDict):
    newDict={}
    for word in currentDict:
        bad=False
        for letter,cletter in word,progress:
            if cletter!="_" and cletter==letter or guess==letter:
                pass
            else:
                bad=True
        if not bad:
            newDict.append(word)

    return newDict

def minimax(node, depth, maximizingPlayer, word, progress, referenceDict):
    alpha=["a","b","c","d","e","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","x","y","z"]
    if depth==0 or "_" not in node:
        return 0
    if maximizingPlayer:
        value=-10000000
        for letter in alpha:
            child=getWordGroup(letter,progress,referenceDict)

            value = max(value, minimax(child,depth-1, False, word, progress, referenceDict))
        return value
    else:
        value=10000000
        for letter in alpha:
            value = min(value, minimax(child,depth-1,True), word, progress, referenceDict)
        return value

def genRefDict(dictionary,length):
    refDict={}
    for word in dictionary:
        if len(word)==length:
            refDict.append(word)

    return refDict

win=False
missNum=0
guess=""
misses=[]
progress=[]
dictionary = readDictionary()
word=randomWord(dictionary)
referenceDict=genRefDict(dictionary,len(word))

for n in range (len(word)):
    progress.append("_")

while missNum<6:
    print(genBoard(missNum))
    print(toString(progress))
    print("Last Guess: " + guess)
    print("Misses: " + missesToString(misses))
    print("\n+++++\n")
    # print(miniMax(word,progress,10,True))
    guess=input("Your Next Guess: ")
    bullseye, wincon, progress = guessLetter(guess, word, progress)

    if wincon==True or toString(progress)==word:
        print("You win!")
        win=True
        break
    elif bullseye==False:
        missNum+=1
        misses.append(guess)

if not win:
    print(genBoard(missNum))
    print("Gameover!")
