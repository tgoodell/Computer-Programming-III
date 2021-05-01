import sympy

num=int(input("Give me a positive integer: "))
top=int(input("Give me the number to go backwards with: "))
stop=int(input("Give me the number to stop with: "))

if num==1:
    print(1,1)
elif num%2==0:
    print(2,num/2)
elif sympy.isprime(num):
    print(num,1)
else:
    if top%2==0:
        top-=1
    if top==num:
        n=top-2
    else:
        n=1*top
    while n>stop and n>1:
        if num%n==0:
            break
        n-=2
    if num%n==0:
        print(n,num//n)
    else:
        print(-1,-1)

quit()