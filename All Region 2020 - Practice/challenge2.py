# This challenge will have your team create a program that converts a phrase entered by the user into 1337 Speak.

print("This program converts a provided phrase to l337 speak. You may proceed.")
phrase=input("Enter phrase: ")
nphrase=""

for letter in phrase:
    if letter=="O" or letter=="o":
        nphrase+="0"
    elif letter=="L" or letter=="l":
        nphrase+="1"
    elif letter=="Z" or letter=="z":
        nphrase+="2"
    elif letter=="E" or letter=="e":
        nphrase+="3"
    elif letter=="A" or letter=="a":
        nphrase+="4"
    elif letter=="S" or letter=="s":
        nphrase+="5"
    elif letter=="T" or letter=="t":
        nphrase+="7"
    elif letter=="G" or letter=="g":
        nphrase+="9"
    else:
        nphrase+=letter

print("---")
print("Entered Phrase: " + phrase)
print("1337 Phrase:    " + nphrase)
