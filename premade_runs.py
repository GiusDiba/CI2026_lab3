from ciac_models import *

def takeoverTimeEvaluation(population: Population):
        # --- Takeover Time evaluation ---
    print (f"TAKEOVER TIME: {population.calculateTakeoverTime(
        Population.parentTournamentSelection,
        Population.offspringSelectionByFitness,
        Population.survivorSelectionByAging,
        eliteNotAging= False,
        verbose= False
    )}")

def mutationOnly(population: Population, verbose: bool = False, eliteNotAging: bool = True):
    best_solution = max(population.solutions)

    print(f"Starting best: {best_solution.stringify()}")

    # --- Running the algorithm - Mutation only ---
    print("---\tMutation only\t---")
    MAX_NO_IMPROVEMENT = max(CHILDREN_AMT // CHARACTERISTICS_AMT, 50)
    MAX_EXPLORE_STAGE = 3
    explore_counter = 0

    while explore_counter < MAX_EXPLORE_STAGE:
        no_improvement_counter = 0

        print("---\tEXPLORING\t---")
        while no_improvement_counter < MAX_NO_IMPROVEMENT / 2:
            population.advanceGeneration(
                Population.parentTournamentSelection,
                Population.getOffspringByBigMutation,
                Population.offspringSelectionByFitness,
                Population.survivorSelectionByAging,
                eliteNotAging = eliteNotAging,
                verbose = verbose)

            if population.best_solution > best_solution:
                best_solution = population.best_solution
                no_improvement_counter = 0
            else:
                no_improvement_counter += 1
        explore_counter += 1

        no_improvement_counter = 0
        print("---\tEXPLOITING\t---")
        while no_improvement_counter < MAX_NO_IMPROVEMENT:
            population.advanceGeneration(
                Population.parentTournamentSelection,
                Population.getOffspringByCloseMutation, 
                Population.offspringSelectionByFitness,
                Population.survivorSelectionByAging,
                eliteNotAging = eliteNotAging,
                verbose = verbose)

            if population.best_solution > best_solution:
                best_solution = population.best_solution
                no_improvement_counter = 0
            else:
                no_improvement_counter += 1

    print(f"---\tEND\t---\nBest solution: \n{best_solution.stringify()} | generation {population.generation}")

def recombinationOnly(population: Population, verbose: bool = False, eliteNotAging: bool = True):
    # --- Running the algorithm - recombination only ---
    best_solution = max(population.solutions)
    print(f"Starting best: {best_solution.stringify()}")

    print("---\tRecombination only\t---")
    MAX_NO_IMPROVEMENT = max(CHILDREN_AMT // CHARACTERISTICS_AMT, 50)
    MAX_EXPLORE_STAGE = 3
    explore_counter = 0

    while explore_counter < MAX_EXPLORE_STAGE:
        no_improvement_counter = 0

        print("---\tEXPLORING\t---")
        while no_improvement_counter < MAX_NO_IMPROVEMENT / 2:
            population.advanceGeneration(
                Population.parentTournamentSelection,
                Population.getSingleChildrenByBinaryRecombination,
                Population.offspringSelectionByFitness,
                Population.survivorSelectionByAging,
                eliteNotAging = eliteNotAging,
                verbose = verbose,
                )

            if population.best_solution > best_solution:
                best_solution = population.best_solution
                no_improvement_counter = 0
            else:
                no_improvement_counter += 1
        explore_counter += 1

        no_improvement_counter = 0
        print("---\tEXPLOITING\t---")
        while no_improvement_counter < MAX_NO_IMPROVEMENT:
            population.advanceGeneration(
                Population.parentTournamentSelection,
                Population.getSingleChildrenByBinaryRecombination, 
                Population.offspringSelectionByFitness,
                Population.survivorSelectionByAging,
                eliteNotAging = eliteNotAging,
                verbose = verbose)

            if population.best_solution > best_solution:
                best_solution = population.best_solution
                no_improvement_counter = 0
            else:
                no_improvement_counter += 1

    print(f"---\tEND\t---\nBest solution: \n{best_solution.stringify()} | generation {population.generation}")

# Stage1: EXPLORATION - perform big mutations on the current population, without elite aging
# Stage2: EXPLOITATION - perform some multi-sibling recombination, with elite aging
# WIP