from __future__ import annotations
from icecream import ic
from collections.abc import Sequence
from random import seed, randint, choices, shuffle

CHILDREN_AMT = 10
CHARACTERISTICS_AMT = 5
REFERENCE_CHILD = 0
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

    def __init__(self, children: Sequence[Child]):
        self.circle = {}
        for idx in range(CHILDREN_AMT):
            cur_child = children[idx]._id
            left_child = children[idx - 1]._id # if idx == 0, then it takes the last element (children[-1])
            right_child = children[(idx + 1) % CHILDREN_AMT]._id # this way it takes the first element if idx == CHILDREN_AMT - 1 (this idea came from ChatGPT)
            
            self.circle[cur_child] = {left_child, right_child}
        
        self.fitness = self.calculateFitness()

        pass

    def __str__(self):
        return "\n".join(f"{child}: {adj}" for child, adj in self.circle.items())
        pass

    @classmethod
    def from_idstring(cls, idstring: Sequence[int]):
        childseq = []
        for _id in idstring:
            childseq.append(PLAYGROUND[_id])
        return cls(childseq)

    def __eq__(self, other: Solution) -> bool:
        for idx in range(CHILDREN_AMT):
            if self.circle[idx] != other.circle[idx]:
                return False
        return True

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

        adj1, adj2 = self.circle[cur_child]
        fit += PLAYGROUND[cur_child].difference(PLAYGROUND[adj1])
        fit += PLAYGROUND[cur_child].difference(PLAYGROUND[adj2])

        prev_child = cur_child
        cur_child = adj2

        counter = 3

        while counter < CHILDREN_AMT:
            adj, = self.circle[cur_child] - {prev_child}
            fit += PLAYGROUND[cur_child].difference(PLAYGROUND[adj])

            prev_child = cur_child
            cur_child = adj
            counter += 1

        return fit
        pass



for idx in range(CHILDREN_AMT):
    PLAYGROUND[idx] = Child(idx, choices([True, False], k = CHARACTERISTICS_AMT))

sol = Solution.from_idstring(PLAYGROUND)

print(sol)
print(sol.disentagle())
print(sol.fitness)

for c in PLAYGROUND:
    print(PLAYGROUND[c])
