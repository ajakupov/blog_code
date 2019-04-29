#Init class to store the collection of letters
import math

class Letter:
    def __init__(self, letter, quantity, msgSize) :
        self.letter = letter
        self.quantity = float(quantity)
        self.msgSize = float(msgSize)
    def getLetter(self):
        return self.letter
    def getQuantity(self):
        return self.quantity
    def getMsgSize(self):
        return self.msgSize
    def getProbabilty(self):
        return float(self.quantity/self.msgSize)

a =[]
temp = []
x = raw_input("Please, enter your sequence:")
length = len(x)
for i in x:
    if temp.count(i) == 0:
        tempObj = Letter(i, x.count(i), length)
        a.append(tempObj)
        temp.append(i)
print temp
for item in a:
    print item.getLetter()
    print item.getProbabilty()
