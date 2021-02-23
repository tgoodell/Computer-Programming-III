import random
import math

# The limit for the extended ASCII Character set
MAX_LIMIT = math.pow(2,32)

randString = ''

GCD=random.randint(1,MAX_LIMIT)

for n in range(1000000):
    randInt = random.randint(0, MAX_LIMIT)
    randString+=str(randInt*GCD)+","

randString=randString[:-1]

print(randString)

with open('input.txt', 'w') as f:
    print(randString,file=f)