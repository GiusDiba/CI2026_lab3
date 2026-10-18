from ciac_models import *

for idx in range(CHILDREN_AMT):
    PLAYGROUND[idx] = Child(idx, choices([True, False], k = CHARACTERISTICS_AMT))

sol = Solution.from_idstring(PLAYGROUND)

print(sol)
print(sol.disentagle())
print(sol.fitness)

for c in PLAYGROUND:
    print(PLAYGROUND[c])

sol2 = sol.mutate()

print(sol2)
print(sol2.disentagle())
print(sol2.fitness)
