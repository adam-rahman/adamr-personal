# Possible solution to Assignment 4 COMP 211 
# Problems 1 and 2
# Danny Krizanc Nov 2016


#Problem 1

class FullBinaryTree(object):

    '''Implements a full binary tree; each node should have exactly two children,
       left and right, and one parent. For interal nodes left and right are
       are other internal nodes. For leaves, the are both None. All nodes
       have a parent that is an internal node except the root whose parent
       is None. Tree must contain at least one node.'''

    def __init__(self,left=None,right=None,parent=None):

        '''Constructor creates a single node tree as default. Sets
           parent relation if left and right are given.'''

        self.left = left
        self.right = right
        self.parent = parent
        if self.left:
            self.left.set_parent(self)
        if self.right:
            self.right.set_parent(self)

    def set_parent(self,tree):

        self.parent = tree

    def get_parent(self):

        return self.parent

    def is_leaf(self):

        '''Returns true iff node is a leaf'''

        return not self.left and not self.right

    def is_root(self):

        '''Returns true iff node is the root'''

        return not self.parent

    def size(self):

        '''Returns the size of the tree'''

        if self.is_leaf():
            return 1
        else:
            return 1 + self.left.size() + self.right.size()

    def height(self):

        '''Returns the height of the tree'''

        if self.is_leaf():
            return 0
        else:
            return 1 + max((self.left.height(),self.right.height()))

    def lca(self,tree):

        '''Returns the least common answer of self and tree'''

        my_anc = self.list_of_ancestors()
        tree_anc = tree.list_of_ancestors()
        i=0
        while  i<len(my_anc) and i<len(tree_anc) and my_anc[i] == tree_anc[i]:
            i = i+1
        if my_anc[i-1] == tree_anc[i-1]:
            return my_anc[i-1]
        else:
            return None


    def contains(self,tree):

        '''Returns true iff self contains tree as a subtree'''

        if self == tree:
            return True
        elif self.is_leaf():
            return False
        else:
            return self.left.contains(tree) or self.right.contains(tree)

    def list_of_ancestors(self):
        '''Returns list of ancestors including self'''

        if self.is_root():
            return [self]
        else:
            return self.parent.list_of_ancestors() + [self]

    def list_of_leaves(self):

        '''Returns a list of all of the leaves of tree'''

        if self.is_leaf():
            return [self]
        else:
            return self.left.list_of_leaves()+self.right.list_of_leaves()
    
# Problem 2

class PhyloTree(FullBinaryTree):

    '''Implements a phylogenetic tree. Leaves contain name of species; all
       nodes contain a time variable representing a measure of the time into
       the past. The leaves have time=0.0. Subclass of FullBinaryTree'''

    def __init__(self,name,time=0.0,left=None,right=None,parent=None):

        '''Constructor for phylogenetic tree; note must contain a name'''

        self.name = name
        self.time = time
        FullBinaryTree.__init__(self,left,right,parent)

    def __str__(self):

        '''To string method for printing in Newick format (leaves only)'''

        if self.is_leaf():
            return self.name
        else:
            return '('+str(self.left)+','+str(self.right)+')'

    def get_time(self):

        '''Returns the time associated with a node'''

        return self.time

    def get_species(self,name):

        '''Returns node associated with name in tree'''

        leaves = self.list_of_leaves()
        for leaf in leaves:
            if leaf.name == name:
                return leaf
        return None




    
