import random


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

def miniMax(guess,depth,maximizingPlayer):
    if depth==0: # or node is a terminal node then
        return heuristic
    if maximizingPlayer:
        # max stuff
    elif maximizingPlayer==False :
        value=10000000
        guess="a"
        for letter in alpha:
            bullseye, wincon, progress = guessLetter(guess, word, progress)
            temp,_=miniMax(letter,depth-1,True)
            if temp<value:
                value=temp
                guess=letter
        return value,guess

win=False
missNum=0
guess=""
misses=[]
progress=[]
dictionary=readDictionary()
word=randomWord(dictionary)

for n in range (len(word)):
    progress.append("_")

while missNum<6:
    print(genBoard(missNum))
    print(toString(progress))
    print("Last Guess: " + guess)
    print("Misses: " + missesToString(misses))
    print("\n+++++\n")
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
