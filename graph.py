# Defining Classes used to setup graph structure

# Imports
from typing import List, Tuple

# Declaring Types
Vector = List[int]
Graph = List[List[int]]

# Declaring Classes
class Union_Find:
    def __init__(self, n: int) -> None:
        self.n: int = n
        self.length: int = n
        self.union_find: Vector = list(range(n))
        self.size: Vector = [1] * n 

    def find(self, i: int) -> int:
        if self.union_find[i] != i:
            self.union_find[i] = self.find(self.union_find[i])
        
        return self.union_find[i] 

    def union(self, a: int, b: int) -> None:
        ra: int = self.find(a)
        rb: int = self.find(b)

        if self.size[ra] > self.size[rb]:
            ra, rb = rb, ra

        self.union_find[ra] = rb
        self.size[ra] = self.size[ra] + self.size[rb]

    def add(self) -> None:
        self.union_find.append(self.length)
        self.size.append(1)
        self.length += 1


class Sprouts_Graph:
    def __init__(self, n: int) -> None:
        self.n: int = n
        self.union = Union_Find(n)

