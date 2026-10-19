from ciac_models import *
from random import shuffle

# Playground initialization
for idx in range(CHILDREN_AMT):
    PLAYGROUND[idx] = Child(idx, choices([True, False], k = CHARACTERISTICS_AMT))

# Initial random population
population = Population()

best_solution = population.best_solution
for _ in range(100):
    population.advanceGeneration(Population.parentTournamentSelection, Population.getOffspringByMutation, Population.survivorSelectionByAging)
    if population.best_solution > best_solution:
        best_solution = population.best_solution

print(f"--- END ---\nBest solution: \n{best_solution.stringify()}")