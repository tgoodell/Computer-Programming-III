import time
import bintrees

class Node():
    def __init__(self, value, left=None, right=None):
        self.value=value
        self.left=left
        self.right=right
        self.height=1

    def __str__(self):
        # Challenge: take in tree and figure out how to print it
        output=""
        if self.left:
            output+="[%s]"%self.left
        output+="%s:%s"%(self.value,self.height)
        if self.right:
            output+="(%s)"%self.right

        return output

class TreeDriver():
    def leftRotate(self, node):
        node2=node.right
        tempNode=node2.left

        node2.left=node
        node.right=tempNode

        node.height=1+max(self.getHeight(node.left),self.getHeight(node.right))
        node2.height=1+max(self.getHeight(node2.left),self.getHeight(node2.right))

        return node2

    def rightRotate(self,node):
        node2=node.left
        tempNode=node2.right

        node2.right=node
        node.left=tempNode

        node.height=1+max(self.getHeight(node.left),self.getHeight(node.right))
        node2.height=1+max(self.getHeight(node2.left),self.getHeight(node2.right))

        return node2

    def getHeight(self,node):
        if not node:
            return 0
        else:
            return node.height

    def getBF(self, parent):
        if not parent:
            return 0
        else:
            return self.getHeight(parent.left) - self.getHeight(parent.right)
        
    def doInsertCases(self,node,value):
        bf=self.getBF(node)
        
        if bf>1 and value>node.left.value:
            node.left=self.leftRotate(node.left)
            return self.rightRotate(node)
        elif bf<-1 and value<node.right.value:
            node.right=self.rightRotate(node.right)
            return self.leftRotate(node)
        elif bf>1 and value<node.left.value:
            return self.rightRotate(node)
        elif bf<-1 and value>node.right.value:
            return self.leftRotate(node)
        else:
            return node

    def doDeleteCases(self,node):
        bf=self.getBF(node)
  
        if bf>1 and self.getBF(node.left)>=0:
            return self.rightRotate(node)
        elif bf<-1 and self.getBF(node.right)<=0:
            return self.leftRotate(node)
        elif bf>1 and self.getBF(node.left)<0:
            node.left = self.leftRotate(node.left)
            return self.rightRotate(node)
        elif bf<-1 and self.getBF(node.right)>0:
            node.right=self.rightRotate(node.right)
            return self.leftRotate(node)
        else:
            return node
        
    def getLowestChild(self,node):
        if not node or not node.left:
            return node
        else:
            return self.getLowestChild(node.left)

    def getTree(self,node):
        if not node:
            return

        raw=str(node)
        raw=raw[2:-2].replace("[",",").replace("]",",").replace("(",",").replace(")",",")
        raw=raw.split(",")
        output={}
        heights=[]
        for line in raw:
            if line=="":
                pass
            else:
                value,height=line.split(":")
                if height in heights:
                    output[height].append(value)
                else:
                    output[height]=[value]
                    heights.append(height)

        heights.sort(reverse=True)
        strOutput=""
        for height in heights:
            strOutput+=str(output[height]).replace("]","").replace("[","").replace("'","")+"\n"

        return strOutput
    
    def add(self, parent, value):
        if not parent:
            return Node(value)
        elif value<parent.value:
            parent.left=self.add(parent.left,value)
        else:
            parent.right=self.add(parent.right,value)

        if self.getHeight(parent.left)>self.getHeight(parent.right):
            parent.height=self.getHeight(parent.left)+1
        elif self.getHeight(parent.left)<self.getHeight(parent.right):
            parent.height=self.getHeight(parent.right)+1

        return self.doInsertCases(parent,value)

    def delete(self, node, key):
        if not node:
            return node
        elif key<node.value:
            node.left=self.delete(node.left, key)
        elif key>node.value:
            node.right=self.delete(node.right, key)
        else:
            if not node.left:
                temp=node.right
                node=None
                return temp
  
            elif node.right is None:
                temp=node.left
                node=None
                return temp
  
            tempNode=self.getLowestChild(node.right)
            node.value=tempNode.value
            node.right=self.delete(node.right,tempNode.value)

        if not node:
            return node

        node.height=1+max(self.getHeight(node.left),self.getHeight(node.right))
  
        return self.doDeleteCases(node)

class Tree:
    def __init__(self):
        self.root=None
        self.tree=TreeDriver()

    def __str__(self):
        return self.tree.getTree(self.root)

    def __add__(self,value):
        self.root=self.tree.add(self.root,value)

    def __sub__(self,value):
        self.root=self.tree.delete(self.root,value)

    def getHeight(self):
        return self.tree.getHeight(self.root)


def addOrderedItems():
    n=0
    fopen = open("heightAVL5.csv", "w")
    initialTime=time.time()
    while time.time()<initialTime+300:
        tree=Tree()
        for k in range(0,2**n):
            tree+k
        startTime=time.time()
        for k in range(0,2**n):
            tree-k
        n+=1
        timestamp=str(time.time()-startTime)
        output=str(2**n) + "," + str(timestamp) + "\n"
        fopen.write(output)
        print(2**n)
        
def addOrderedItemsToBintrees():
    n=0
    fopen = open("heightAVL6.csv", "w")
    initialTime=time.time()
    while time.time()<initialTime+300:
        tree=bintrees.FastAVLTree()
        for k in range(0,2**n):
            tree.insert(k,k)
        startTime=time.time()
        for k in range(0,2**n):
            tree.remove(k)
        n+=1
        timestamp=str(time.time()-startTime)
        output=str(2**n) + "," + timestamp + "\n"
        fopen.write(output)
        print(2**n)

addOrderedItems()
addOrderedItemsToBintrees()


