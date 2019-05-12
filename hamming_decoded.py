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
    return bits + str(t1) + str(t2) + str(t3) 
 
def parity(s, indicies):
    """Compute the parity bit for the given string s and indicies"""
    sub = ""
    for i in indicies:
        sub += s[i]
    return str.count(sub, "1") % 2 

sequence = raw_input("Enter your encoded msg")
encode(sequence)
print

syndrome_dict = {'000': -1, '001': 6, '010': 5,
                 '011': 3, '100': 4, '101': 0, '110': 2, '111': 1}

def get_syndrome(bits):
    number_of_blocks = len(bits)/7
    entire_msg =""
    for i in range (0, number_of_blocks):
        end  = (i+1)*7 - 1
        r3 = int(bits[end])
        r2 = int(bits[end-1])
        r1 = int(bits[end-2])
        s1 = r1^parity(bits, [7*i,7*i + 1,7*i + 2])
        s2 = r2^parity(bits, [7*i+1,7*i + 2,7*i + 3])
        s3 = r3^parity(bits, [7*i,7*i + 1,7*i + 3])
        ss = str(s1)+str(s2)+str(s3)

        print ("Syndrome is:")
        print (ss)
        correct_msg = list(bits)
        index = -1
        if syndrome_dict[ss] != -1:
            index = 7*i + syndrome_dict[ss]
        else:
            index = -1
        print ("Error index")
        print (index)
        print (bits[index])
        if correct_msg[index] == '0':
            correct_msg[index]= '1'
        elif correct_msg[index] == '1':
            correct_msg[index] = '0'
        correct_msg = correct_msg[:4]
        correct_msg = "".join(correct_msg)
        entire_msg += correct_msg
    print ("The correct msg")
    print entire_msg
sequence2 = raw_input("Enter your msg")
get_syndrome(sequence2)
raw_input("Press Enter to exit")
