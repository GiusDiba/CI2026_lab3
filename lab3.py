from icecream import ic
from collections.abc import Sequence
from random import seed, randint, choices

CHILDREN_AMT = 10
CHARACTERISTICS_AMT = 5
REFERENCE_CHILD = 0
PLAYGROUND = []
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
    
    def difference(self, other_child) -> int:
        return sum(s != o for s, o in zip(self.characteristics, other_child.characteristics))
        pass

# solution as a dictionary of adjacences: each key is a child id and each value is a set containing adjacent children.
class Solution:
    circle: dict

    def __init__(self, children: Sequence[int]):
        self.circle = {}

        # This is to keep an orientation and avoid having solutions that are the same, but just reversed
        ref_child = children.index((PLAYGROUND[REFERENCE_CHILD] + 1) % CHILDREN_AMT) # see comments below
        if 


        for idx in range(CHILDREN_AMT):
            cur_child = children[idx]._id
            left_child = children[idx - 1]._id # if idx == 0, then it takes the last element (children[-1])
            right_child = children[(idx + 1) % CHILDREN_AMT]._id # this way it takes the first element if idx == CHILDREN_AMT - 1 (this idea came from ChatGPT)
            
            self.circle[cur_child] = {left_child, right_child}

    pass


for idx in range(CHILDREN_AMT):
    PLAYGROUND.append(Child(idx, choices([True, False], k = CHARACTERISTICS_AMT)))

sol = Solution(PLAYGROUND)

ic(sol.circle)