import filecmp
import os
import zlib

from phylo_tree import FullBinaryTree
from collections import Counter
from heapq import heapify,heappush,heappop
from pickle import dump,load,HIGHEST_PROTOCOL

from string import ascii_lowercase,ascii_uppercase
from random import choice
from math import log

from texttable import Texttable
from platform import platform

def sym_prob_dict(str):
    '''Returns a dictionary in the form {symbol:probability} 
       representing the probabilities of each symbol occuring
       in the given string'''
    return {sym:Counter(str)[sym]/float(len(str)) for sym in Counter(str)}


def huffman_code(sp_dict):
    '''
    Parameter:A dictionary in the form {symbol:probability}
    Returns a dictionary in the form {symbol:code} where 
    code is a prefix code generated via the Huffman Algorithm
    '''
    symbols = sp_dict.keys()
    if not symbols: 
        return {}
    elif len(symbols) == 1: 
        return {symbols[0]:'1'}
    elif len(symbols) == 2: 
        return {symbols[0]:'1', symbols[1]:'0'}
    trees = [HuffmanTree(sym,(sp_dict[sym])) for sym in symbols]
    heapify(trees)
    while len(trees) > 1:
        l_tree = heappop(trees)
        l_tree.code = '0'
        r_tree = heappop(trees)
        r_tree.code = '1'
        new_tree = HuffmanTree(None,l_tree.prob + r_tree.prob,
            left = l_tree, right = r_tree)
        heappush(trees,new_tree)
    fin_tree = heappop(trees)
    return {sym:fin_tree.get_symbol(sym).get_codeword() for sym in symbols}


def encode(string,codebook):
    '''
    Parameters:A string and dictionary in the form {symbol:code}
    Returns a string formed by the prefix code for each character
    in the given string
    '''
    return ''.join(codebook[sym] for sym in string)


def decode(cipher,codebook):
    '''
    Parameters:A cipher and a dictionary in the form {symbol:code}
    Returns a decoded string formed by searching for codes within 
    the cipher and concatenating the corresponding symbol
    '''
    decodebook = {code:sym for sym,code in codebook.items()}
    codeword = ''
    deciphered = ''
    # Checks cipher to see if code is present
    for i in xrange(len(cipher)):
        codeword += cipher[i]
        if codeword in decodebook:
            deciphered += decodebook[codeword]
            codeword = ''
    return deciphered


def binary2char(string):
    '''Returns character encoded version of a binary string.
       Note: padded to be divisible by 8 with pad length as first char.'''
    pad = 8 - len(string)%8
    string = string+pad*'0'
    out = str(pad)+''.join([chr(int(string[i:i+8],2))
                            for i in range(0,len(string),8)])
    return out


def char2binary(string):
    '''Returns binary string represented by a character string.
       Assumes first char represents number of pad bits.'''
    pad = int(string[0])
    out = ''.join([(10-len(bin(ord(char))))*'0' + bin(ord(char))[2:] for
                    char in string[1:]])
    return out[:-1*pad]


def compress(infile,outfile):
    '''Encodes the contents of a given file and writes the 
       encoding to a specifed file'''
    f_in = open(infile,'r')
    f_out = open(outfile,'wb')
    contents = f_in.read() 
    # Construct a Huffman codebook from the 
    # {symbol:probability} dictionary of the file's contents
    codebook = huffman_code(sym_prob_dict(contents))
    # Serialize codebook dictionary into file
    dump(codebook,f_out,HIGHEST_PROTOCOL)
    # Encode each character in file, write to new file
    f_out.write(binary2char(encode(contents,codebook)))
    # Close files
    f_in.close()
    f_out.close()


def decompress(infile,outfile):
    '''Decodes the contents of a given file and writes the 
       decoding to a specified file'''
    f_in = open(infile,'rb')
    f_out = open(outfile,'wb')
    # Deserialize stored dictionary of prefix codes
    codebook = load(f_in)
    # Read in contents from file
    contents = f_in.read()
    # Decodes contents, writes to file
    f_out.write(decode((char2binary(contents)),codebook))
    # Close files
    f_in.close()
    f_out.close()


def entropy(str):
    '''Calculates the entropy of a given string'''
    probs = Counter(str)
    len_s = float(len(str))
    tmp = sum(count/len_s*log(count/len_s,2) for count in probs.values())
    return -float(tmp) + 0


def make_rand_file(n):
    '''Creates a file consisting of n symbols chosen uniformly at random
    from the standard Roman uppercase and lowercase alphabet'''
    alphabet = ascii_uppercase + ascii_lowercase
    rand_file = open('random.txt','wb')
    rand_file.write(''.join(choice(alphabet) for i in range(n)))
    rand_file.close()


def make_all_As(n):
    '''Creates a file consisting of n A's'''
    a_file = open('allAs.txt','wb')
    a_file.write('A'*n)
    a_file.close()


def make_all_ABs(n):
    '''Creates a file consisting of n characters, either A or B'''
    ab_file = open('allABs.txt','wb')
    ab_file.write(''.join(choice('AB') for i in xrange(n)))
    ab_file.close()


def make_empty_file():
    '''Least deserving of a docstring, but indeed, makes an empty file'''
    open('empty.txt','r').close()


def make_table_row(file):
    '''Given a file name w/o extension,returns table row as a list'''
    orig = file+'.txt'
    comp = file+'-comp.txt'
    decomp = file+'-decomp.txt'
    file_in = open(file+'.txt','rb')
    o_str = file_in.read()
    o_str = open(file+'.txt','r').read()
    # Creates a zlib-compressed file
    z_out = open('zip-'+orig,'wb')
    z_out.write(zlib.compress(o_str))
    z_out.close()
    # Calculates entropy of file contents
    file_entropy = entropy(o_str)
    file_in.close()
    # Fills in row with File Name, Size, 
    # Compressed Size, Zip Size, Entropy
    row = []
    compress(orig,comp)
    decompress(comp,decomp)
    row.extend((orig,         
        os.path.getsize(orig),
        os.path.getsize(comp),
        os.path.getsize('zip-'+orig),
        file_entropy))
    return row


def file_cmp(f1,f2):
    '''Given two files, verifies their contents are identical'''
    return open(f1,'r').read() == open(f2,'r').read()
    open(f1,'r').close()
    open(f2,'r').close()


def rigorous_cmp(f1,f2):
    '''Given two files, verifies contents are identical 
    using both filecmp.cmp and my_file_cmp'''
    return filecmp.cmp(f1,f2) and file_cmp(f1,f2)


def test_lossless_compression():
    '''Tests if decompressed file is identical to original, thus
    indicating lossless compression'''
    for file in ['sample','fasta','random','allAs','allABs','empty']:
        assert rigorous_cmp(file+'.txt',file+'-decomp.txt')
    return "Lossless compression verified."


def draw_table():
    '''Fills in each row of a table using texttable'''
    # Create ASCII table
    tbl = Texttable()
    tbl.set_deco(Texttable.HEADER)
    tbl.set_cols_dtype(['t','i','i','i','f'])
    # Create a list of rows to fill in the ASCII table
    row_lst = [["File Name","Size","Compressed Size",
        "Zip Size","Entropy"]]
    for file in ['sample','fasta','random','allAs','allABs','empty']:
        row_lst.extend([make_table_row(file)])
    tbl.add_rows(row_lst)
    return tbl.draw() + '\n'


def main():
    '''Main function for final assignment'''
    print("Executing main() on",platform()+':\n')
    make_rand_file(20000)
    make_all_As(20000)
    make_all_ABs(20000)
    make_empty_file()
    print(draw_table())
    print(test_lossless_compression())

main()