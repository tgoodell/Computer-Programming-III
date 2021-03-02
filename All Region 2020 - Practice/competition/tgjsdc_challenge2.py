def gcd(first,second):
    while (first%second)>0:
        remainder=first%second
        first=second
        second=remainder
    return second

print("Weclome!")
print("This program simplifies fractions and converts fractions to mixed numbers.")
print("-"*10 + "\n")

badInput=True
while badInput:
    input=input("Please provide a fraction in the form a/b: ")
    try:
        input=input.split("/")
        a, b=input
        badInput=False
    except:
        print("Bad input. Please use the form a/b.")



a,b=input

a=int(a)
b=int(b)

if b==0:
    print("Undefined.")
elif a//b==a/b:
    print(int(a//b))
elif a>b:
    remainder=a%b
    wholeNum=0
    while a>b:
        a-=b
        wholeNum+=1

    print(str(wholeNum) + " " + str(remainder) + "/" + str(b))
else:
    GCD=gcd(a,b)
    a=a//GCD
    b=b//GCD
    print(str(a) + "/" + str(b))