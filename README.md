# CI2026_lab3

## _Children in a Circle_ approached using evolutionary computation

### *N* children each having *C* boolean characteristics. The difference between two children is the number of characteristics in which they differ. We want to maximize the difference between adjacent children.

---

## Solution

To avoid having duplicate solutions, I've decided to represent the circle as a dictionary of adjacences. For example, if 10 children are arranged as follows:

```python
7804926531
```

the solution will look like this:

```py
7: {8, 1}
8: {0, 7}
0: {8, 4}
4: {0, 9}
9: {2, 4}
2: {9, 6}
6: {2, 5}
5: {3, 6}
3: {1, 5}
1: {3, 7}
```

## Fitness

I've decided to evaluate fitness as the sum of all differencese between adjacent children, divided by the highest theoretical cumulative difference count (if every adjacent children would be completely different from the ones nearby, this count is CHILDREN_AMOUNT * CHARACTERISTICS_AMOUNT).

```python
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

        return fit / (CHARACTERISTICS_AMT * CHILDREN_AMT)
        pass
```

This way, it ranges between 0 and 1, allowing to better judge how good a solution is for different amounts of children and characteristics.

## Genetic Operators

I've implemented mutation operators that perform copy, random sawpping, swapping with an adjacent child and inversion mutation.

I've also implemented recombination operators that give either one or two children by combining adjacences from two parents, and an inner-over crossover operator.

## Offspring Selection

Offspring selection is completely deterministic: the `MU` individuals with the highest fitness are chosen.

## Survivor Selection

Survivors are selected according to their age. I've included an option to allow for the highest-fitness member to not age.

## Runs

I've tried different combinations and strategies, resumed in the table below. Alle the implementations are in `premade_runs.py`

- Amount of children: 500
- Amount of characteristics: 10

| Run                                         | Fitness | Generations | Time     |
| ------------------------------------------- | ------- | ----------- | -------- |
| `mutationOnly(population, True, True)`      | 0.7352  | 1194        | 2m 22s   |
| `recombinationOnly(population, False, False)`| 0.5976  | 436         | 1m 11.7s |
|`bigmut_multirec(population, 1, 10, 10, 10, True)`| 0.8136    | 3755        | 12m 28.0s         |
|`naive_hypermodern(population, 200, False)`|0.7976|3952|7m 17.9s|
|`multistage_hypermodern_fm(population, 10, 50, 10, 1, True)`|0.7696|1694|3m 24.4s|
|`multistage_hypermodern_fr(population, 20, 50, 12, 1, True)`|0.7208 |921|1m 20.0s|
|`mult_hypr_fr_ex(population, 5, MU, 20, 50, 12, 1)`|0.7744|6049|--|
|`hypr_mut_rec(population, 0.12, 100)`|0.8052|4166|--|
|`mixed_advancing(population, 0.1, 100)`|0.83|3869|--|