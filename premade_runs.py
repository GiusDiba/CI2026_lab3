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

# Stage1: EXPLORATION - perform big mutations on the current population, with elite aging (population will decrease)
# Stage2: EXPLOITATION - perform some multi-sibling recombination, without elite aging (population will increase)
# Repeat stages 1 and 2 some times
# Stage3: EXPLOITATION - perform small mutations with elite aging
def bigmut_multirec(population: Population,  max_mut: int, max_rec: int, max_iterations:int, stage_3_iterations: int, verbose: bool = False):
    best_solution = max(population.solutions)
    print(f"Starting best: {best_solution.stringify()}")

    iter_counter = 0
    while iter_counter < max_iterations:
        prev_iter_best = best_solution
        inner_counter = 0
        print(f"---\tSTAGE 1\t---")
        while inner_counter < max_mut:
            population.advanceGeneration(
                Population.parentTournamentSelection,
                Population.getOffspringByBigMutation,
                Population.offspringSelectionByFitness,
                Population.survivorSelectionByAging,
                eliteNotAging= False,
                verbose = verbose
            )
            if population.best_solution > best_solution:
                best_solution = population.best_solution
                inner_counter = 0
            else:
                inner_counter += 1
        
        inner_counter = 0
        print(f"---\tSTAGE 2\t---")
        while inner_counter < max_rec:
            population.advanceGeneration(
                Population.parentTournamentSelection,
                Population.getMultipleChildrenByBinaryRecombination,
                Population.offspringSelectionByFitness,
                Population.survivorSelectionByAging,
                eliteNotAging= False,
                verbose= verbose
            )
            if population.best_solution > best_solution:
                best_solution = population.best_solution
                inner_counter = 0
            else:
                inner_counter += 1
        
        if best_solution > prev_iter_best:
            iter_counter = 0
        else:
            iter_counter += 1

    iter_counter = 0
    print(f"---\tSTAGE 3\t---")
    while iter_counter < stage_3_iterations:
        population.advanceGeneration(
                Population.parentTournamentSelection,
                Population.getOffspringByCloseMutation,
                Population.offspringSelectionByFitness,
                Population.survivorSelectionByAging,
                eliteNotAging= False,
                verbose= verbose
            )
        if population.best_solution > best_solution:
            best_solution = population.best_solution
            iter_counter = 0
        else:
            iter_counter += 1

    print(f"---\tEND\t---\nBest solution: \n{best_solution.stringify()} | generation {population.generation}")

    pass
