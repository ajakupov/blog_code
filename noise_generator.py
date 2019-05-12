import math
from random import randint

def noize(sequence):
    number_of_blocks = len(sequence)/7
    temp = list(sequence)
    for i in range (0, number_of_blocks):
        end  = (i+1)*7 - 1
        start = (i+1)*7 -7
        index = randint(start,end)
        print index
        if (temp[index]=='0'):
            temp[index]='1'
        elif (temp[index]=='1'):
            temp[index]='0'
        sequence = "".join(temp)
    print sequence
def swap(digit):
    if digit == '0':
        digit = '1'
    if digit == '1':
        digit = '0'

x  = raw_input("Enter your code: ")
noize(x)
