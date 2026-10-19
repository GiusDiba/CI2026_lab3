from ciac_models import *
from random import shuffle

# Playground initialization
for idx in range(CHILDREN_AMT):
    PLAYGROUND[idx] = Child(idx, choices([True, False], k = CHARACTERISTICS_AMT))

# Initial random population
population = Population()

best_solution = population.best_solution


MAX_NO_IMPROVEMENT = 50
no_improvement_counter = 0

while no_improvement_counter < MAX_NO_IMPROVEMENT:
    population.advanceGeneration(Population.parentTournamentSelection, Population.getOffspringByMutation, Population.survivorSelectionByAging, eliteNotAging = True, verbose = True)
    if population.best_solution > best_solution:
        best_solution = population.best_solution
        no_improvement_counter = 0
    else:
        no_improvement_counter += 1

print(f"--- END ---\nBest solution: \n{best_solution.stringify()}")