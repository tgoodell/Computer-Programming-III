s="""0 1 7
0 2 9
0 3 14
1 2 10
3 2 2
1 4 15
3 4 11
2 5 9
5 4 6"""

adjList={}
for line in s.split("\n"):
    a,b,c=[int(x) for x in line.split()]
    a,b=sorted((a,b))
    weight=[a,b,c]
    adjList[a]=adjList.get(a,[])+[(b,weight)]
    adjList[b]=adjList.get(b,[])+[(a,weight)]
print(adjList)
m=adjList[0][1][1]
m[0]=234234
print(adjList)