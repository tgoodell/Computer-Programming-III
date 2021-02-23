import syllapy
import binascii

secret = 1567694910997135653525145058312346590392317309

def getFlag():
    x =  secret.to_bytes((secret.bit_length() + 7) // 8, 'big').decode()
    return x

def wasHaiku(haiku):
    if haiku:
        x = getFlag()
        print("haikuPy blesses you with this: ")
        print(x)
        return False
    else:
        print("haikuPy no like ur 'haiku' :(")
        return True

def countSyllables(line):
    words = line.split(" ")
    syllables = 0
    for word in words:
        syllables += syllapy.count(word)
    
    return syllables

def getHaiku():
    oneLine = input("Drop haikuPy a line: ")
    x = countSyllables(oneLine)

    twoLine = input("Drop haikuPy anotha line: ")
    y = countSyllables(twoLine)

    threeLine = input("Drop haikuPy ANOTHA line: ")
    z = countSyllables(threeLine)

    return x == 5 and y == 7 and z == 5


print("hi this is haikuPy, haikuPy no likely commas, periods, or any other punctuate. haikuPy just like word. if haikuPy likey, haiku py will give prize :> \n")
print("p.s. haikuPy isnt the best at counting syllables...but haikuPy tries!!!")

# while True:
#     haiku = getHaiku()
#     wasHaiku(haiku)

print(getFlag())