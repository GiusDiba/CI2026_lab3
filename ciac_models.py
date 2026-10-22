from __future__ import annotations
from collections.abc import Sequence
from random import seed, sample, choices, shuffle, randint, choice
from math import floor

CHILDREN_AMT = 500
CHARACTERISTICS_AMT = 10
MAX_DIFFERENCES = CHARACTERISTICS_AMT * CHILDREN_AMT

PLAYGROUND = {}
ALL_CHILDREN = set(range(CHILDREN_AMT))
seed(42)

class Child:
    _id: int
    characteristics: tuple[bool]

    def __init__(self, _id: int, characteristics: Sequence[bool]):
        self._id = _id
        self.characteristics = characteristics
        pass

    def __str__(self) -> str:
        return f"{self._id}: {self.characteristics}"
        pass
    
    def difference(self, other_child: Child) -> int:
        return sum(s != o for s, o in zip(self.characteristics, other_child.characteristics))
        pass

# solution as a dictionary of adjacences: each key is a child id and each value is a set containing adjacent children.
class Solution:
    circle: dict
    fitness: int
    id_string: list[int]
    age: int

    def __init__(self, id_string: Sequence[int]):
        self.circle = {}
        self.id_string = id_string.copy()

        for idx in range(CHILDREN_AMT):
            cur_child = PLAYGROUND[id_string[idx]]._id
            left_child = PLAYGROUND[id_string[idx - 1]]._id # if idx == 0, then it takes the last element (children[-1])
            right_child = PLAYGROUND[id_string[(idx + 1) % CHILDREN_AMT]]._id # this way it takes the first element if idx == CHILDREN_AMT - 1 (this idea came from ChatGPT)
            
            self.circle[cur_child] = {left_child, right_child}
        
        self.fitness = self.calculateFitness()
        self.age = 0
        self._hash = hash(frozenset((k, frozenset(v)) for k, v in self.circle.items())) # Helped by Claude to allow Solutions to be added in a set

        pass

    def __str__(self) -> str:
        return "\n".join(f"{child}: {adj}" for child, adj in self.circle.items())
        pass

    def __eq__(self, other: Solution) -> bool:
        for idx in range(CHILDREN_AMT):
            if self.circle[idx] != other.circle[idx]:
                return False
        return True

        pass

    # Helped by Calude to allow Solutions to be added in a set
    def __hash__(self) -> int:
        return self._hash

    def __lt__(self, other: Solution) -> bool:
        return self.fitness < other.fitness

    def __gt__(self, other: Solution) -> bool:
        return self.fitness > other.fitness

    # Two solutions are similar if they have many adjacences in common
    def similarity(self, other: Solution) -> int:
        adj_count = 0
        for key, item in self.circle:
            adj_count += len(other[key] - item)
        return adj_count

        pass

    def disentagle(self) -> list[int]:
        disentagled = [None] * CHILDREN_AMT
        cur_child = 0

        disentagled[cur_child] = cur_child
        adj1, adj2 = self.circle[cur_child]
        disentagled[cur_child - 1] = adj1
        disentagled[cur_child + 1] = adj2
        
        prev_child = cur_child
        cur_child = adj2

        idx = 2

        counter = 3
        while (counter < CHILDREN_AMT):
            adj, = self.circle[cur_child] - {prev_child}
            disentagled[idx] = adj

            idx += 1
            prev_child = cur_child
            cur_child = adj
            counter += 1

        return disentagled
        pass

    def calculateFitness(self) -> int:
        fit = 0
        cur_child = 0
        first_child = 0

        adj1, adj2 = self.circle[cur_child]
        fit += PLAYGROUND[cur_child].difference(PLAYGROUND[adj1])
        fit += PLAYGROUND[cur_child].difference(PLAYGROUND[adj2])

        prev_child = cur_child
        cur_child = adj2

        while cur_child != adj1:
            adj, = self.circle[cur_child] - {prev_child}
            fit += PLAYGROUND[cur_child].difference(PLAYGROUND[adj])

            prev_child = cur_child
            cur_child = adj

        return fit / MAX_DIFFERENCES
        pass

    # --- Mutations ---

    def mutateSwapRandom(self) -> Solution:
        new_idstring = self.id_string.copy()
        idx1, idx2 = sample(range(CHILDREN_AMT), 2)

        new_idstring[idx1], new_idstring[idx2] = new_idstring[idx2], new_idstring[idx1]

        return Solution(new_idstring)
        pass

    def mutateSwapNext(self) -> Solution:
        new_idstring = self.id_string.copy()
        idx1 = randint(0, CHILDREN_AMT - 1)
        idx2 = (idx1 + 1) % CHILDREN_AMT

        new_idstring[idx1], new_idstring[idx2] = new_idstring[idx2], new_idstring[idx1]
        return Solution(new_idstring)
        pass

    def inversionMutation(self) -> Solution:
        new_idstring = self.id_string.copy()
        idx1, idx2 = sample(range(CHILDREN_AMT), 2)
        start = min(idx1, idx2)
        end = max(idx1, idx2)

        to_rev = new_idstring[start:end]
        to_rev.reverse()
        new_idstring = new_idstring[:start] + to_rev + new_idstring[end:]

        return Solution(new_idstring)
        pass

    # --- Recombinations ---

    # Given two idstrings, i take one child at random from the first parent and one of its adjacent ones. Then, i repeat the process with the new
    # child, but considering the adjacences of the other parent.
    # This way, half of the offspring's adjacences come from the first parent, and the other half from the other one.
    # This recombinations can also introduce a random mutation in case all adjacent children have already been added
    def binaryRecombination(self, other: Solution) -> Solution: # "explorative"
        inserted = set()

        new_idstring = []
        count = 1
        adj = randint(0, CHILDREN_AMT - 1)
        new_idstring.append(adj)
        inserted.add(adj)
        while count < CHILDREN_AMT:
            if count % 2 == 0:
                parent = self.circle
                fallback_parent = other.circle
            else:
                parent = other.circle
                fallback_parent = self.circle

            pool = parent[adj] - inserted
            if not pool:
                pool = fallback_parent[adj] - inserted
                if not pool:
                    pool = ALL_CHILDREN - inserted

            
            adj = choice(tuple(pool))
            new_idstring.append(adj)
            inserted.add(adj)
            count += 1

        return Solution(new_idstring)

        pass

    def innerOverCrossover(self, other: Solution) -> Solution: # "exploitative"
        p1_gene_idx = randint(0, CHILDREN_AMT - 1)
        p1_gene = self.id_string[p1_gene_idx]
        p2_gene = choice(tuple(other.circle[p1_gene]))
        p2_gene_idx = self.id_string.index(p2_gene)

        start_idx = min(p1_gene_idx, p2_gene_idx)
        end_idx = max(p1_gene_idx, p2_gene_idx)

        new_idstring = self.id_string.copy()

        first_part = new_idstring[:start_idx + 1]
        to_rev = new_idstring[start_idx + 1 : end_idx + 1 ]
        to_rev.reverse()

        if end_idx + 1 >= CHILDREN_AMT:
            last_part = []
        else:
            last_part = new_idstring[end_idx + 1:]

        new_idstring = first_part + to_rev + last_part
        
        return Solution(new_idstring)

        pass



    def stringify(self) -> str:
        st = ""
        if CHILDREN_AMT > 20:
            st = "too long..."
        else:
            for _id in self.id_string:
                st += f"{_id}"
        return st + f" | fitness {self.fitness}"

        pass

class Population:
    size: int
    solutions: list[Solution]
    generation: int
    best_solution: Solution

    MU = 10
    LBDA = 3 * MU
    MAX_AGE = 2

    def __init__(self, MU: int = 20, LBDA: int = 60, MAX_AGE: int = 2, TAU: int = None ):
        self.size = MU
        self.MU = MU
        self.LBDA = LBDA
        self.MAX_AGE = MAX_AGE
        if TAU:
            self.TAU = TAU
        else:
            self.TAU = max(CHILDREN_AMT // 100, 4)
        self.solutions = []
        self.generation = 0
        id_string = list(range(CHILDREN_AMT))
        
        for _ in range(self.size):
            shuffle(id_string)
            self.solutions.append(Solution(id_string))

        self.best_solution = max(self.solutions)

        pass

    def __str__(self) -> str:
        return "\n".join(f"specimen {idx} | fitness {self.solutions[idx].fitness}: {self.solutions[idx].id_string}" for idx in range(self.size))

        pass

    # --- Parent selection methods ---

    # Tournament selection
    def parentTournamentSelection(population: list[Solution], LBDA, TAU) -> list[Solution]:
        mating_pool = []
        tournament_pool = []
        for _ in range(LBDA):
            tournament_pool = choices(population, k = TAU)
            mating_pool.append(max(tournament_pool))

        return mating_pool

        pass

    # --- Genetic operators ---

    def getOffspringByCloseMutation(parents: list[Solution], LBDA = None) -> set[Solution]:
        offspring = set()
        for sol in parents:
            offspring.add(sol.mutateSwapNext())
        
        return offspring

        pass

    def getOffspringByBigMutation(parents: list[Solution], LBDA = None) -> set[Solution]:
        offspring = set()
        for sol in parents:
            offspring.add(sol.mutateSwapRandom())
        
        return offspring

        pass

    def getOffspringByCopy(parents: list[Solution], LBDA = None) -> set[Solution]:
        offspring = set()
        for sol in parents:
            offspring.add(Solution(sol.id_string))
        return offspring
        
        pass

    def getOffspringByInversion(parents: list[Solution], LBDA = None) -> set[Solution]:
        offspring = set()
        for sol in parents:
            offspring.add(sol.inversionMutation())

        return offspring

        pass
    
    # If the mating pool is uneven, the remaining parent "mates with himself" (close mutation)
    def getSingleChildrenByBinaryRecombination(parents: list[Solution], LBDA) -> set[Solution]:
        offspring = set()

        if len(parents) % 2 != 0:
            lone_parent = parents.pop()
            offspring.add(lone_parent.mutateSwapNext())
        
        for idx in range(len(parents) - 1):
            next_idx = idx + 1
            offspring.add(parents[idx].binaryRecombination(parents[next_idx]))
            idx = next_idx

        return offspring

        pass

    def getMultipleChildrenByBinaryRecombination(parents: list[Solution], LBDA, siblings_amt: int = 2):
        offspring = set()

        if len(parents) % 2 != 0:
            lone_parent = parents.pop()
            offspring.add(lone_parent.mutateSwapNext())
        
        for idx in range(len(parents) - 1):
            next_idx = idx + 1
            #print(f"Mating {idx} and {next_idx}")
            for _ in range(siblings_amt):
                offspring.add(parents[idx].binaryRecombination(parents[next_idx]))
            idx = next_idx

        return offspring

        pass

    def getChildrenByInnerOverCrossover(parents: list[Solution], LBDA):
        offspring = set()

        if LBDA % 2 != 0:
            lone_parent = parents.pop()
            offspring.add(lone_parent.mutateSwapNext())
        
        for idx in range(len(parents) - 1):
            next_idx = idx + 1
            offspring.add(parents[idx].innerOverCrossover(parents[next_idx]))
            idx = next_idx

        return offspring

        pass

    # --- Offspring selection methods ---

    def offspringSelectionByFitness(offspring: set[Solution], amount: int) -> list[Solution]:
        selected = sorted(offspring, reverse = True)

        return selected[:amount]

        pass

    def offspringSelectionBySimilarity(offspring: set[Solution], amount: int) -> list[Solution]:
        # WIP

        pass

    # --- Survivor selection methods ---

    def survivorSelectionByAging(survivors: list[Solution], MAX_AGE) -> list[Solution]:
        population = [sol for sol in survivors if sol.age < MAX_AGE]
        return population

        pass

    ### ### ###
    mutation_operators = [
        getOffspringByBigMutation,
        getOffspringByCloseMutation,
        getOffspringByInversion 
    ]

    recombination_operators = [
        getSingleChildrenByBinaryRecombination,
        getMultipleChildrenByBinaryRecombination,
        getChildrenByInnerOverCrossover
    ]
    
    def advanceGeneration(self, parentSelectionMethod, geneticOperator, offspringSelectionMethod, survivorSelectionMethod, eliteNotAging: bool = False, verbose: bool = False, offspring_amt: int = MU):
        mating_pool = parentSelectionMethod(self.solutions, self.LBDA, self.TAU)
        offspring = geneticOperator(mating_pool, self.LBDA)
        offspring = offspringSelectionMethod(offspring, self.MU)

        best_fitness = max(self.solutions).fitness
        for sol in self.solutions:
            if eliteNotAging and sol.fitness == best_fitness:
                continue
            else:
                sol.age += 1

        self.solutions += offspring
        self.solutions = survivorSelectionMethod(self.solutions, self.MAX_AGE)

        self.generation += 1
        self.best_solution = max(self.solutions)

        if verbose:
            print(f"generation {self.generation}, best solution {self.best_solution.stringify()}, solution amt {len(self.solutions)}")

        pass

    # Some specimen mutate, other recombine
    def mixedAdvance(self, parentSelectionMethod, mutationWeights, recombinationWeights, offspringSelectionMethod, survivorSelectionMethod, fractionMutating: float = 0.5, eliteNotAging: bool = False, verbose: bool = False):
        parents = parentSelectionMethod(self.solutions, self.LBDA, self.TAU)
        shuffle(parents)
        amt = floor(len(parents) * fractionMutating)

        mutation_pool = parents[:amt]
        mating_pool = parents[amt:]

        mut_idx = choices(range(len(self.mutation_operators)), weights = mutationWeights)[0]
        mat_idx = choices(range(len(self.recombination_operators)), weights = recombinationWeights)[0]

        mut_offspring = self.mutation_operators[mut_idx](mutation_pool, self.LBDA)
        mat_offspring = self.recombination_operators[mat_idx](mutation_pool, self.LBDA)

        offspring = mut_offspring.union(mat_offspring)
        offspring = offspringSelectionMethod(offspring, self.MU)

        best_fitness = max(self.solutions).fitness
        for sol in self.solutions:
            if eliteNotAging and sol.fitness == best_fitness:
                continue
            else:
                sol.age += 1

        self.solutions += offspring
        self.solutions = survivorSelectionMethod(self.solutions, self.MAX_AGE)

        self.generation += 1
        self.best_solution = max(self.solutions)

        if verbose:
            print(f"generation {self.generation}, best solution {self.best_solution.stringify()}, solution amt {len(self.solutions)}")

        pass

    def calculateTakeoverTime(self, parentSelectionMethod, offspringSelectionMethod, survivorSelectionMethod, eliteNotAging: bool = False, verbose: bool = False) -> int:
        backup_sol = self.solutions
        backup_best = self.best_solution
        best_count = 0

        while best_count < len(self.solutions):
            self.advanceGeneration(parentSelectionMethod, Population.getOffspringByCopy, offspringSelectionMethod, survivorSelectionMethod, eliteNotAging, verbose)
            best_count = 0
            for sol in self.solutions:
                if sol.fitness == backup_best.fitness:
                    best_count += 1
                
        takeover_time = self.generation

        self.solutions = backup_sol
        self.best_solution = backup_best

        self.generation = 0
        return takeover_time
        pass

    def randomMassExtinction(self, new_population: int = MU):
        self.solutions = sample(self.solutions, k = new_population)
        self.generation += 1

        pass