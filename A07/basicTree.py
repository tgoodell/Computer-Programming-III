class Tree:
    def __init__(self):
        self.root=None

    def __add__(self, value):
        if self.root:
            self.root+value
        else:
            self.root=TreeNode(value)
        return self

    def __str__(self):
        return str(self.root)

class TreeNode:
    def __init__(self,value,left=None,right=None):
        self.value=value
        self.left=left
        self.right=right
        self.height=0

    def __getitem__(self, index):
        return self.getList()[index]

    def __len__(self):
        x=1
        if self.left:
            x+=len(self.left)
        if self.right:
            x+=len(self.right)
        return x

    def __add__(self, value):
        if value<self.value:
            # recursively add
            if self.left:
                self.left+value
            else:
                self.left=TreeNode(value)
            # update height
            h=max(self.left.height+1,self.right.height+1)
            if h>self.height:
                self.height=h
            # balance if unbalanced
            if abs(self.left.height-(self.right.height if self.right else -1))>1:
                pass
            # update height
        elif value>self.value:
            if self.right:
                self.right + value
            else:
                self.right = TreeNode(value)
            if self.right.height+1>self.height:
                self.height=self.left.height+1
        # else:
        #     replace

        return self

    def leftRotate(self):
        pass

    def rightRotate(self):
        pass

    def getList(self):
        output=[]
        if self.left:
            output+=self.left.getList()
        output+=self.value
        if self.right:
            output+=self.right.getList()
        return output

    def __str__(self):
        # Challenge: take in tree and figure out how to print it
        output=""
        if self.left:
            output+="[%d]"%self.left
        output+="%d:%d"%(self.value,self.height)
        if self.right:
            output+="(s%)"%self.right
        return output

t=Tree()
t+=5
t+=7
print(t)