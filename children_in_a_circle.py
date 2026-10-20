from premade_runs import *
# Playground initialization
for idx in range(CHILDREN_AMT):
    PLAYGROUND[idx] = Child(idx, choices([True, False], k = CHARACTERISTICS_AMT))

# Initial random population
population = Population()
REF_SOLUTIONS = population.solutions.copy()

recombinationOnly(population, verbose= True, eliteNotAging= False)