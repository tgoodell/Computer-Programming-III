# Eval: count number of words in the word group that remains
# Have the class call itself for each possibility.
# Need to separate by wordGroup

import random
import socket, re
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 50000        # The port used by the server

class HangMan:
    def __init__(self,wordGroup,dictionary,possibleGuesses="ETAINOSHRDLUCMFWYGPBVKQJXZ"):
        self.wordGroup=wordGroup
        self.dictionary=dictionary
        self.possibleGuesses=possibleGuesses

    def getDictionary(self):
        return self.dictionary

    def minimax(self,depth,maximizing):
        bestNode=""
        bestGuess=""
        if len(self.dictionary)==1:
            return self.eval(),self.wordGroup,None
        elif depth==0:
            return self.eval(),self.dictionary[0],None
        elif maximizing:
            value=-10000000
            for letter in self.possibleGuesses[:14]:
                testWords=self.newWordGroups(letter)

                for testGroup in testWords:
                    testWordList=testWords[testGroup]
                    guessGame=HangMan(testGroup,testWordList,self.possibleGuesses.replace(letter,""))
                    evalValueGame,_,_=guessGame.minimax(depth-1,False)
                    if evalValueGame>value:
                        value=evalValueGame
                        bestGuess=letter
                        bestNode=testGroup

            return value,bestNode,bestGuess
        else:
            value=10000000

            for letter in self.possibleGuesses[:14]:
                testWords=self.newWordGroups(letter)

                for testGroup in testWords:
                    testWordList=testWords[testGroup]
                    guessGame=HangMan(testGroup,testWordList,self.possibleGuesses.replace(letter,""))
                    evalValueGame,_,_=guessGame.minimax(depth-1,True)
                    if evalValueGame<value:
                        value=evalValueGame
                        bestGuess=letter
                        bestNode=testGroup

            return value,bestNode,bestGuess

    def eval(self):
        return len(self.dictionary)

    def play(self,bestGuess,bestNode):
        if bestGuess:
            self.possibleGuesses=self.possibleGuesses.replace(bestGuess,"")
            self.wordGroup=bestNode
            if "_" in bestNode:
                self.dictionary=self.newWordGroups(bestGuess)[bestNode]
            else:
                self.dictionary=[]

            return True
        else:
            return False

    def newWordGroups(self,guess):
        newWordGroupList={}

        for word in self.dictionary:
            tempWordGroup=""
            if guess in word:
                bad=False
                for letter,lettern in zip(word,self.wordGroup):
                    if lettern!="_" and letter!=lettern:
                        bad=True
                        break
                    elif letter==lettern or letter==guess:
                        tempWordGroup+=letter
                    else:
                        tempWordGroup+="_"

                if not bad and tempWordGroup not in newWordGroupList:
                    newWordGroupList[tempWordGroup]=[word]
                elif not bad:
                    newWordGroupList[tempWordGroup].append(word)

        return newWordGroupList

def sepMissHit(node, guesses):
    hits = []
    misses = []
    for check in guesses:
        if check in node:
            hits.append(check.lower())
        else:
            misses.append(check.lower())

    return misses, hits

sourceDict = {}
for line in open("Collins Scrabble Words (2019).txt"):
    word = line.strip()
    if len(word) not in sourceDict:
        sourceDict[len(word)] = []
    sourceDict[len(word)].append(word)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    data = s.recv(1024)
    x=""
    wordGroup=""
    bestGuess=""
    if(b"," in data):
        word,guesses,guess=re.findall(b"(\w+) \[(\w*),(\w*)\]".decode("utf-8"),data.decode("utf-8"))[0]
        misses,hits=sepMissHit(word,guesses)
        if len(misses)>8:
            x="Hangee Lost."
        elif "_" not in word:
            x="Hangman Lost."
        else:
            possibles=""
            for letter in "ETAINOSHRDLUCMFWYGPBVKQJXZ":
                if letter not in guesses:
                    possibles+=letter
            game=HangMan(word,sourceDict[len(word)],possibleGuesses=possibles)
            _,wordGroup,bestGuess=game.minimax(4,True)
            if bestGuess==guess:
                x=wordGroup
            else:
                x=word
    else:
        word,guesses=re.findall(b"(\w+) \[(\w*)]".decode("utf-8"),data.decode("utf-8"))[0]
        possibles=""
        for letter in "ZXJQKVBPGYWFMCULDRHSONIATE":
            if letter not in guesses:
                possibles+=letter
        game=HangMan(word,sourceDict[len(word)],possibleGuesses=possibles)
        _,wordGroup,bestGuess=game.minimax(4,False)
        x=bestGuess

    # ~ print(data)
    print(x,wordGroup,bestGuess)
    s.sendall(x.encode())