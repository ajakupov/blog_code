from heapq import heappush, heappop, heapify
from collections import defaultdict

class Dictionary:
    def __init__(self, symbol, huffman_code) :
        self.symbol = symbol
        self.huffman_code = huffman_code
    def getSymbol(self):
        return self.symbol
    def getHuffman(self):
        return self.huffman_code

dictionary = []

def encode(symb2freq):
    """Huffman encode the given dict mapping symbols to weights"""
    heap = [[wt, [sym, ""]] for sym, wt in symb2freq.items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

def decode(encoded_sequence):
    temp = []
    seq = ""
    output = ""
    for i in dictionary:
        temp.append(i.getHuffman())
    for digit in encoded_sequence:
        seq += digit
        if temp.count(seq) == 0:
            continue
        else:
            output += dictionary[temp.index(seq)].getSymbol();
            seq=""
    print output

txt = raw_input("Please, enter your sequence")
symb2freq = defaultdict(int)
for ch in txt:
    symb2freq[ch] += 1
# in Python 3.1+:
# symb2freq = collections.Counter(txt)
huff = encode(symb2freq)
encoded_sequence = "";
print "Symbol\tWeight\tHuffman Code"
for p in huff:
    item = Dictionary(p[0], p[1])
    dictionary.append(item)
    print "%s\t%s\t%s" % (p[0], symb2freq[p[0]], p[1])
encoded_sequence = ""
for letter in txt:
    temp = []
    for i in dictionary:
        temp.append(i.getSymbol())
    ind = temp.index(letter)
    encoded_sequence += dictionary[ind].getHuffman()
print "the encoded sequence is"
print encoded_sequence
print "the decode sequence is"
decode (encoded_sequence)
