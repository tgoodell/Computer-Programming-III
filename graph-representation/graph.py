s="""0 1 7
0 2 9
0 3 14
1 2 10
3 2 2
1 4 15
2 4 11
3 5 9
5 4 6"""

adjList={}
for line in s.split("\n"):
    a,b,c=[int(x) for x in line.split()]
    a,b=sorted((a,b))
    weight=[a,b,c]
    adjList[a]=adjList.get(a,[])+[(b,weight)]
    adjList[b]=adjList.get(b,[])+[(a,weight)]
# print(adjList)
# Dikstra Pseudo Algorthm

bestSoFar={0:0}
queue=[0]
while queue:
    node=queue.pop(0) # get the smallest
    for node2,(edgeCost,) in adjList[node]:
        c=edgeCost+bestSoFar[node]
        if node2 not in bestSoFar or bestSoFar[node2]>c:
            bestSoFar[node2]=c
            queue+=node2,
print(bestSoFar)