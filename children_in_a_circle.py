from ciac_models import *
from random import shuffle

# Playground initialization
for idx in range(CHILDREN_AMT):
    PLAYGROUND[idx] = Child(idx, choices([True, False], k = CHARACTERISTICS_AMT))

# Initial random population
population = Population()

best_solution = population.best_solution

# --- Takeover Time evaluation ---
print (f"TAKEOVER TIME: {population.calculateTakeoverTime(
    Population.parentTournamentSelection,
    Population.offspringSelectionByFitness,
    Population.survivorSelectionByAging,
    eliteNotAging= False,
    verbose= False
)}")

# --- Running the algorithm ---
MAX_NO_IMPROVEMENT = max(CHILDREN_AMT // CHARACTERISTICS_AMT, 50)
MAX_EXPLORE_STAGE = 3
explore_counter = 0

while explore_counter < MAX_EXPLORE_STAGE:
    no_improvement_counter = 0

    print("--- EXPLORING ---")
    while no_improvement_counter < MAX_NO_IMPROVEMENT / 2:
        population.advanceGeneration(
            Population.parentTournamentSelection,
            Population.getOffspringByBigMutation,
            Population.offspringSelectionByFitness,
            Population.survivorSelectionByAging,
            eliteNotAging = True,
            verbose = False)

        if population.best_solution > best_solution:
            best_solution = population.best_solution
            no_improvement_counter = 0
        else:
            no_improvement_counter += 1
    explore_counter += 1

    no_improvement_counter = 0
    print("--- EXPLOITING ---")
    while no_improvement_counter < MAX_NO_IMPROVEMENT:
        population.advanceGeneration(
            Population.parentTournamentSelection,
            Population.getOffspringByCloseMutation, 
            Population.offspringSelectionByFitness,
            Population.survivorSelectionByAging,
            eliteNotAging = True,
            verbose = False)

        if population.best_solution > best_solution:
            best_solution = population.best_solution
            no_improvement_counter = 0
        else:
            no_improvement_counter += 1

print(f"--- END ---\nBest solution: \n{best_solution.stringify()} | generation {population.generation}")