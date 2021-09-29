- AVL Tree

- Treap
    - Randomized binary search tree 
      
- Remember depth (cache height for each node)
- Scapegoat Tree
- Assuming you just move nodes around, you have to handle whether you are rotating at root, handling a LL or RR or LR case.
- Quite heavy duty to move nodes around: at least six different cases. 
- Write a node, then a tree that keeps track of roots and calls Node methods. 
- Delete, add, contains (binary search) methods. 
- Nodes that keep track of height as a cached value. 
- 