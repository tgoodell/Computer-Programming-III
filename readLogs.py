n=0

with open("logs.txt","r") as f:
    lines=f.read()
    for line in lines.split("\n"):
        if "$" in line:
            print(line)
            n+=1

print(n)