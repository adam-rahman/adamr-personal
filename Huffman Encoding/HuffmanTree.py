class HuffmanTree(FullBinaryTree):
    '''Implements a Huffman Coding Tree, each node stores a symbol, 
    probability, and code; extends FullBinaryTree '''
    def __init__(self,symbol,prob,code=None,
                 left=None,right=None,parent=None):
        '''Constructor for Huffman Coding Tree'''
        self.symbol = symbol
        self.prob = prob
        FullBinaryTree.__init__(self,left,right,parent)

    def __cmp__(self,other):
        '''Compares two trees according to their problem'''
        return cmp(self.prob,other.prob)

    def get_codeword(self):
        '''Returns the binary string created by concatenating code
           values from root to self, excluding root code value'''
        if self.is_root(): 
            return ""
        return self.parent.get_codeword() + self.code

    def get_symbol(self,symbol):
        '''Returns the leaf node in the tree containing
        the given symbol if such a leaf exists.'''
        if self.is_leaf(): 
            if self.symbol == symbol: 
                return self
            else: 
                return None
        return self.left.get_symbol(symbol) or self.right.get_symbol(symbol)