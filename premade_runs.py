from ciac_models import *
from random import random

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

# genetic operators are equiprobable and randomly chosen
# elite aging is also chosen at random
def naive_hypermodern(population: Population, max_no_improvement: int, verbose: bool = False):
    best_solution = max(population.solutions)
    print(f"Starting best: {best_solution.stringify()}")

    iter_counter = 0
    genetic_operators = [
        Population.getOffspringByBigMutation,
        Population.getOffspringByCloseMutation,
        #Population.getOffspringByCopy,
        Population.getSingleChildrenByBinaryRecombination,
        Population.getMultipleChildrenByBinaryRecombination]

    while iter_counter < max_no_improvement:
        chosen_operator = choice(genetic_operators)
        population.advanceGeneration(
            Population.parentTournamentSelection,
            chosen_operator,
            Population.offspringSelectionByFitness,
            Population.survivorSelectionByAging,
            eliteNotAging= choice((True, False)),
            verbose= verbose)

        if population.best_solution > best_solution:
            best_solution = population.best_solution
            iter_counter = 0
        else:
            iter_counter += 1
    
    print(f"---\tEND\t---\nBest solution: \n{best_solution.stringify()} | generation {population.generation}")
        
    pass

# If during the last season there has been a majority of non-improvements, the probability of performing a mutation is increased.
# The algorithm sops after max_no_improvement consecutive mutation ages
# (I'm using "season" to refer to an arbitrary number of most recent generations)
def multistage_hypermodern_fm(population: Population, season_length: int, max_no_improvement: int, decrease_step: int = 1, increase_step: int = 1, verbose: bool = False):
    best_solution = max(population.solutions)
    print(f"Starting best: {best_solution.stringify()}")

    mutation_ops = [
        Population.getOffspringByCloseMutation,
        Population.getOffspringByBigMutation
    ]

    recombination_ops = [
        Population.getSingleChildrenByBinaryRecombination,
        Population.getMultipleChildrenByBinaryRecombination
    ]

    no_improvement_counter = 0
    no_improvement_generations = 0

    while no_improvement_generations < max_no_improvement:
        if no_improvement_counter > season_length:
            no_improvement_counter = season_length
        else:
            no_improvement_counter = max(0, no_improvement_counter)

        prob = no_improvement_counter / season_length
        print(f"---\tPROB {prob}\t---")
        if random() < prob:
            print("---\tMUTATING\t---")
            population.advanceGeneration(
                Population.parentTournamentSelection,
                choice(mutation_ops),
                Population.offspringSelectionByFitness,
                Population.survivorSelectionByAging,
                eliteNotAging= True,
                verbose= verbose
            )
            if population.best_solution > best_solution:
                no_improvement_generations = 0
                no_improvement_counter -= decrease_step
                best_solution = population.best_solution
            else:
                no_improvement_generations += 1
                no_improvement_counter += increase_step
        else:
            print("---\tRECOMBINING\t---")
            population.advanceGeneration(
                Population.parentTournamentSelection,
                choice(recombination_ops),
                Population.offspringSelectionByFitness,
                Population.survivorSelectionByAging,
                eliteNotAging= False,
                verbose= verbose
            )
            if population.best_solution > best_solution:
                no_improvement_counter -= decrease_step
                best_solution = population.best_solution
            else:
                no_improvement_counter += increase_step




    print(f"---\tEND\t---\nBest solution: \n{best_solution.stringify()} | generation {population.generation}")
    pass

def multistage_hypermodern_fr(population: Population, season_length: int, max_no_improvement: int, decrease_step: int = 1, increase_step: int = 1, verbose: bool = False) -> Solution:
    best_solution = max(population.solutions)
    print(f"Starting best: {best_solution.stringify()}")

    mutation_ops = [
        Population.getOffspringByCloseMutation,
        Population.getOffspringByBigMutation
    ]

    recombination_ops = [
        Population.getSingleChildrenByBinaryRecombination,
        Population.getMultipleChildrenByBinaryRecombination
    ]

    no_improvement_counter = 0
    no_improvement_generations = 0

    while no_improvement_generations < max_no_improvement:
        if no_improvement_counter > season_length:
            no_improvement_counter = season_length
        else:
            no_improvement_counter = max(0, no_improvement_counter)

        prob = no_improvement_counter / season_length
        print(f"---\tPROB {prob}\t---")
        if random() < prob:
            print("---\tMUTATING\t---")
            population.advanceGeneration(
                Population.parentTournamentSelection,
                choice(recombination_ops),
                Population.offspringSelectionByFitness,
                Population.survivorSelectionByAging,
                eliteNotAging= True,
                verbose= verbose
            )
            if population.best_solution > best_solution:
                no_improvement_generations = 0
                no_improvement_counter -= decrease_step
                best_solution = population.best_solution
            else:
                no_improvement_generations += 1
                no_improvement_counter += increase_step
        else:
            print("---\tRECOMBINING\t---")
            population.advanceGeneration(
                Population.parentTournamentSelection,
                choice(mutation_ops),
                Population.offspringSelectionByFitness,
                Population.survivorSelectionByAging,
                eliteNotAging= False,
                verbose= verbose
            )
            if population.best_solution > best_solution:
                no_improvement_counter -= decrease_step
                best_solution = population.best_solution
            else:
                no_improvement_counter += increase_step




    print(f"---\tEND\t---\nBest solution: \n{best_solution.stringify()} | generation {population.generation}")
    return best_solution
    pass


# multistage_hypermodern_fr provides in the end a big population:
# perform "mass extinction" and then repeat the process
def mult_hypr_fr_ex(population: Population, pop_amt: int, max_for_extinction: int, season_length: int, max_no_improvement: int, decrease_step: int = 1, increase_step: int = 1):
    best_solution = population.best_solution
    no_improvement_counter = 0
    while no_improvement_counter < max_for_extinction:
        found = multistage_hypermodern_fr(population, season_length, max_no_improvement, decrease_step, increase_step, False)
        if found > best_solution:
            best_solution = found
            no_improvement_counter = 0
        else:
            no_improvement_counter += 1

        population.randomMassExtinction()

    print(f"---\tEND (for real)\t---\nBest solution: \n{best_solution.stringify()} | generation {population.generation}")

    pass