# Defining Classes used to setup graph structure

# ------------------------------
# Imports
# ------------------------------ 
from typing import List, Tuple, Set
from copy import copy

# ------------------------------ 
# Declaring Types
# ------------------------------ 
Vector = List[int]
Vector2D = List[List[int]]


# ------------------------------ 
# Declaring Classes
# ------------------------------ 

# Union_Find Data Structure for maintaining Components
class Union_Find:
    # Constructor
    # Complexity: Θ(n)
    def __init__(self, n: int) -> None:
        self.n: int = n
        self.length: int = n
        self.union_find: Vector = list(range(n))
        self.size: Vector = [1] * n 

    # Complexity: Θ(⍺(n))
    def find(self, i: int) -> int:
        if self.union_find[i] != i:
            self.union_find[i] = self.find(self.union_find[i])
        
        return self.union_find[i] 

    # Complexity: Θ(⍺(n))
    def union(self, a: int, b: int) -> None:
        ra: int = self.find(a)
        rb: int = self.find(b)

        if self.size[ra] > self.size[rb]:
            ra, rb = rb, ra

        self.union_find[ra] = rb
        self.size[ra] = self.size[ra] + self.size[rb]

    # Complexity: Θ(1)
    def add(self) -> None:
        self.union_find.append(self.length)
        self.size.append(1)
        self.length += 1


# Sprouts Graph setting up entire board
class Sprouts_Graph:
    # Constructor
    # Complexity: Θ(n)
    def __init__(self, n: int) -> None:
        self.n: int = n
        self.union_find: Union_Find = Union_Find(n)
        self.degrees: Vector = [0] * n
        self.faces: Vector2D = [[0]] * n
        self.face_num: int = 1

    # Complexity: Θ(1) 
    def euler_formula(self, v: int, e: int, f: int) -> bool:
        return v - e + f == 2

    # Complexity: Θ(n * ⍺(n))
    def dots_in_component(self, dot: int, union_find: Union_Find) -> Vector:
        dots: Vector = []
        dot_comp: int = union_find.find(dot)

        for i in range(len(union_find.union_find)):
            if union_find.find(i) == dot_comp:
                dots.append(i)

        return dots

    # Complexity: Θ(n * ⍺(n))
    def check_euler_comp(self, dot: int, union_find: Union_Find, degrees: Vector, faces: Vector2D) -> bool:
        dots: Vector = self.dots_in_component(dot, union_find)
        unique_faces: Set[int] = set()

        for d in dots:
            for face in faces[d]:
                unique_faces.add(face)

        v: int = len(dots)
        e: int = int(sum([degrees[d] for d in dots]) / 2)
        f: int = len(unique_faces)

        return self.euler_formula(v, e, f)

    # Complexity: Θ(f_n^2) -> Θ(1) | f_n -> max == 3 
    def compare_faces(self, dotA: int, dotB: int, faces: Vector2D) -> Vector:
        sim_faces: Vector = []

        for faceA in faces[dotA]:
            if faceA in faces[dotB]:
                sim_faces.append(faceA)

        return sim_faces

    # Complexity: Θ(n * f_n) -> Θ(n) 
    def dots_in_face(self, face_num: int, faces: Vector2D) -> Vector:
        dots: Vector = []

        for i in range(len(faces)):
            if face_num in faces[i]:
                dots.append(i)

        return dots

    # Complexity: Θ()
    def connect_components(self, dotA: int, dotB: int, sim_face: int, faces: Vector2D) -> Tuple[bool, Vector2D]:
        # TODO: Connect components together in way that is unique to connecting components together
        pass

    # Complexity: Θ()
    def connect_within_components(self, dotA: int, dotB: int, sim_faces: Vector, faces: Vector2D) -> Tuple[bool, Vector2D]:
        # TODO: Connect components together in way that is unique to connecting within components
        pass

    # Complexity: Θ() 
    def connect(self, dotA: int, dotB: int, is_check: bool = False) -> bool:
        is_valid: bool
        degrees: Vector = copy(self.degrees)
        union_find: Union_Find = copy(self.union_find)
        faces: Vector2D = copy(self.faces)
        face_num: int = self.face_num

        # Check if Degrees
        degrees[dotA] += 1
        degrees[dotB] += 1
        if degrees[dotA] > 3 or degrees[dotB] > 3:
            return False

        # Check if contains same faces
        sim_faces: Vector = self.compare_faces(dotA, dotB, faces)
        if len(sim_faces) == 0:
            return False

        # Connect with unique properties of w/ and w/o components
        if self.union_find.find(dotA) != self.union_find.find(dotB):
            is_valid, faces = self.connect_components(dotA, dotB, sim_faces[0], faces)
        else:
            is_valid, faces = self.connect_within_components(dotA, dotB, sim_faces, faces)
            face_num += 1

        # TODO: Connect graphs in ways components/within_components both occur
        union_find.union(dotA, dotB)

        # After Connection, check if connection failed or euler formula fails
        if not is_valid or not self.check_euler_comp(dotA, union_find, degrees, faces):
            return False

        # Temp Data Structures replace old ones with success
        if not is_check:
            self.degrees = degrees
            self.union_find = union_find
            self.faces = faces
            self.face_num = face_num

        return True
