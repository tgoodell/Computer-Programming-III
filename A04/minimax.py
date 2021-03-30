# Hangee
# Branching Factor 26
# First, try all 26. Benchmark. Get a time. Then figure out what will save you time.

# Hangman
# 2^BLANK_COUNT Branching Factor
# Go through all single space, then double spaces, then tripple spaces, etc. for guesses.

# * Pick a Dict
# * Make a class

# w={3:set("the","top"),...}
# m={1:dict((0,"t"):set("the","top"),...)}

# thing
# m[5][(0,"t")].add("thing")
# m[5][(0,"h")].add("thing")
# m[5][(0,"i")].add("thing")
# m[5][(0,"n")].add("thing")
# m[5][(0,"g")].add("thing")

class HangGame:
    # No heurtistic, just length of matches
    def __init__(self,n):
        self.n=n
        self.guesses={} #{"e":[2,3],"f":[]}
        self.guess=""
        # self.matches=w[n]
    def hangeePlay(self,guess):
        copy=self.clone()
        copy.guess=guess
        # self.guess=guess
        return copy
    def hangmanPlay(self,bitPattern):
        copy=self.clone()
        copy.guesses[guess]=arrayFrom(bitPattern)
        return copy
    def numOfMatchesAndEval(self):
        return intersectionOfSets
    def howManyBlanks(self):
        return numberOfBlanks
    def arrayFrom(self,bitPattern):
        return array
    def status(self):
        return deadAliveOngoing
    def clone(self):

game=HangGame(10)
num=miniMax(game,10,False)

# minMax: keep track of best move and


def miniMax(game,depth,maximizingPlayer):
    if depth==0 # or node is a terminal node then
        return heuristic
    if maximizingPlayer:
        # max stuff
    elif maximizingPlayer==False :
        value=10000000
        guess="a"
        for letter in alpha:
            temp,_=miniMax(game.hangeePlay(letter),depth-1,True)
            if temp<value:
                value=temp
                guess=letter
        return value,guess