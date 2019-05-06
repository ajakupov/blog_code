import sys
 
K = 4
def encode(s):
    """Read in K=4 bits at a time and write out those plus parity bits"""
    while len(s) >= K:
        nybble = s[0:K]
        sys.stdout.write(hamming(nybble))
        s = s[K:]
 
def hamming(bits):
    """Return given 4 bits plus parity bits for bits (1,2,3), (2,3,4) and (1,3,4)"""
    t1 = parity(bits, [0,1,2])
    t2 = parity(bits, [1,2,3])
    t3 = parity(bits, [0,1,3])
    return bits + t1 + t2 + t3 
 
def parity(s, indicies):
    """Compute the parity bit for the given string s and indicies"""
    sub = ""
    for i in indicies:
        sub += s[i]
    return str(str.count(sub, "1") % 2) 


sequence = raw_input("Enter your encoded msg")
print "The decode sequence is: "
encode(sequence)
###################################################################################
# Main
 
if __name__ == "__main__":
    input_string = sys.stdin.read().strip()
    encode(input_string)
