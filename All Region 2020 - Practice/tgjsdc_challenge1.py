'''
Arkansas School for Mathematics Sciences and the Arts
Tristan Goodell
David Clark
Joshua Stallings
'''

print("This program asks the user to input some information and then outputs it back in a neat format.")

userInput1 = input("School Name: ")
userInput2 = input("Team Member 1: ")
userInput3 = input("Team Member 2: ")
userInput4 = input("Team Member 3: ")
userInput5 = input("Sponsor: ").strip() + " - Sponsor"

members = [userInput2, userInput3, userInput4]
finalMembers = []
longest = 0

for x in members:
    if len(x) > longest:
        longest = len(x)
        
for x in members:
    temp = x.strip().replace(" ", "_")
    while len(temp) < longest:
        temp += "_"
    finalMembers.append(temp)

finalString = ""

for x in range(0, longest):
    finalString += f"{finalMembers[0][x]} {finalMembers[1][x]} {finalMembers[2][x]}\n"

print(userInput1)
print(finalString[:-2])
print(userInput5)




      
