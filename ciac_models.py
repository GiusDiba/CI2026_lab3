from __future__ import annotations
from collections.abc import Sequence
from random import seed, sample, choices, shuffle, randint

CHILDREN_AMT = 500
CHARACTERISTICS_AMT = 10
MAX_DIFFERENCES = CHARACTERISTICS_AMT * CHILDREN_AMT
MU = 10
LBDA = 3 * MU
MAX_AGE = 2
TAU = 4

PLAYGROUND = {}
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
        #print(f"\ncurrent: {cur_child} adjacent: {adj1},{adj2}")
        fit += PLAYGROUND[cur_child].difference(PLAYGROUND[adj1])
        fit += PLAYGROUND[cur_child].difference(PLAYGROUND[adj2])

        prev_child = cur_child
        cur_child = adj2

        while cur_child != adj1:
            adj, = self.circle[cur_child] - {prev_child}
            #print(f"evaluating {cur_child} and {adj}")
            fit += PLAYGROUND[cur_child].difference(PLAYGROUND[adj])

            prev_child = cur_child
            cur_child = adj

        return fit / MAX_DIFFERENCES
        pass

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

    def __init__(self):
        self.size = MU
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

    # Tournament selection
    def parentTournamentSelection(population: list[Solution]) -> list[Solution]:
        mating_pool = []
        tournament_pool = []
        for _ in range(LBDA):
            tournament_pool = choices(population, k = TAU)
            mating_pool.append(max(tournament_pool))

        return mating_pool

        pass


    def getOffspringByCloseMutation(parents: list[Solution]) -> set[Solution]:
        offspring = set()
        for sol in parents:
            offspring.add(sol.mutateSwapNext())
        
        return offspring

        pass

    def getOffspringByBigMutation(parents: list[Solution]) -> set[Solution]:
        offspring = set()
        for sol in parents:
            offspring.add(sol.mutateSwapRandom())
        
        return offspring

        pass

    def offspringSelectionByFitness(offspring: set[Solution], amount: int) -> list[Solution]:
        #offspring.sort(key = fitness)
        selected = sorted(offspring, reverse = True)

        return selected[:amount]

        pass

    def offspringSelectionBySimilarity(offspring: set[Solution], amount: int) -> list[Solution]:
        # WIP

        pass

    def survivorSelectionByAging(survivors: list[Solution]) -> list[Solution]:
        population = [sol for sol in survivors if sol.age != MAX_AGE]
        return population

        pass

    def advanceGeneration(self, parentSelectionMethod, offspringGenerationMethod, offspringSelectionMethod, survivorSelectionMethod, eliteNotAging: bool = False, verbose: bool = False, offspring_amt: int = MU):
        mating_pool = parentSelectionMethod(self.solutions)
        offspring = offspringGenerationMethod(mating_pool)
        offspring = offspringSelectionMethod(offspring, offspring_amt)

        best_fitness = max(self.solutions).fitness
        for sol in self.solutions:
            if eliteNotAging and sol.fitness == best_fitness:
                continue
            else:
                sol.age += 1

        self.solutions += offspring
        self.solutions = survivorSelectionMethod(self.solutions)

        self.generation += 1
        self.best_solution = max(self.solutions)

        if verbose:
            print(f"generation {self.generation}, best solution {self.best_solution.stringify()}")

        pass

    def calculateTakeoverTime(self, parentSelectionMethod, survivorSelectionMethod, eliteNotAging: bool = False, verbose: bool = False):
        #backup_sol = self.solutions.copy()
        #backup_best = self.best_solution.copy()

        #self.advanceGeneration()

        pass