from random import randint
from random import sample
    
class Chromosome:

    def __init__(self, sequence, cost):
        self.sequence = sequence
        self.cost = cost
        
    def getSequence(self):
        return self.sequence
    
    def getCost(self):
        return self.cost
    
    def setSequence(self, sequence):
        self.sequence = sequence

    def setCost(self, cost):
        self.cost = cost
                
    def getDcolumns(self):
        return self.dColumns     

def initialize (number_cities, population_size):
    generation = []
    for i in range(population_size):
        sequence = sample(xrange(1,number_cities+1), number_cities)
        generation.append(Chromosome(sequence, 0))
    return generation

def calculate_fitness(generation, cost_matrix):
    for chromosome in generation:
        cost = 0
        for i in range(len(chromosome.getSequence())-1):
            cost += cost_matrix[chromosome.getSequence()[i]-1][chromosome.getSequence()[i+1]-1]
        cost+= cost_matrix[chromosome.getSequence()[len(chromosome.getSequence())-1]-1][chromosome.getSequence()[0]-1]
        chromosome.setCost(cost)

def selection(generation):
    return sorted(generation, key = getKey)[0]

def crossover(parent1, parent2):
    point = randint(0, len(parent1.getSequence()))
    child = Chromosome(parent1.getSequence(), 0)
    #initializing child sequence
    #for x in range(0,len(child.getSequence())):
     #   child.getSequence()[x] = None
    
    # Two random integer indices of the parent1:
    start_pos = randint(0, len(parent1.getSequence()))
    end_pos = randint(0, len(parent1.getSequence()))


    # takes the sub-route from parent one and sticks it in itself:
    # if the start position is before the end:
    if start_pos < end_pos:
        # do it in the start-->end order
        for x in range(start_pos,end_pos):
            child.getSequence()[x] = parent1.getSequence()[x] # set the values to each other
    # if the start position is after the end:
    elif start_pos > end_pos:
        # do it in the end-->start order
        for i in range(end_pos,start_pos):
            child.getSequence()[i] = parent1.getSequence()[i] # set the values to each other

    # Cycles through the parent2. And fills in the child
    # cycles through length of parent2:
    for i in range(len(parent2.getSequence())):
        # if parent2 has a city that the child doesn't have yet:
        if not parent2.getSequence()[i] in child.getSequence():
            # it puts it in the first 'None' spot and breaks out of the loop.
            for x in range(len(child.getSequence()) - 1):
                if child.getSequence()[x] == None:
                    child.getSequence()[x] = parent2.getSequence()[i]
                    break
        # repeated until all the cities are in the child route
        
    return child

def generate_next(generation, cost_matrix):
    temp = []
    result = []
    size = len(generation)
    while (len(temp)!=size):
        parent1 = generation[randint(0, size-1)]
        parent2 = generation[randint(0, size-1)]
        temp.append(crossover(parent1, parent2))
    result = temp + generation
    calculate_fitness(result, cost_matrix)
    result = sorted(result, key = getKey)
    result = result[:size]
    return result

def mutate (generation):
    for chromosome in generation:
        point1 = randint(0, len(chromosome.getSequence())-1)
        point2 = randint(0, len(chromosome.getSequence())-1)
        chromosome.getSequence()[point1], chromosome.getSequence()[point2] = chromosome.getSequence()[point2], chromosome.getSequence()[point1]
        
def printGeneration (generation):
    for chromosome in generation:
        print "{0}\tcost: {1}".format(chromosome.getSequence(), chromosome.getCost())
        
def getKey(chromosome):
    return chromosome.getCost()


cities = open('cities.txt', 'r')
cost_matrix = []

for row in cities:
    cost_matrix.append([ int(x) for x in row.split(',')])

number_cities = len(cost_matrix)
generation_size = 3
generation = initialize(number_cities, generation_size)
calculate_fitness(generation, cost_matrix)
next_generation = generation
print "Initial generation, Best sequence: {0}\tScore: {1}".format(selection(next_generation).getSequence(), selection(next_generation).getCost())
for i in range (1000):
    next_generation = generate_next(next_generation, cost_matrix)
    mutate(next_generation)
    calculate_fitness(next_generation, cost_matrix)
    print "Best sequence: {0}\tScore: {1}".format(selection(next_generation).getSequence(), selection(next_generation).getCost())
