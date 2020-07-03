
''' Modules '''
from typing import List, Set, Dict
from copy import deepcopy

Vector = List[int]
Vector2D = List[List[int]]


# Complexity: Θ(1)
def euler_formula(num_vertices: int,
                  num_edges: int,
                  num_faces: int) -> bool:
    ''' Expresses Euler's Formula and checks graph '''
    return num_vertices - num_edges + num_faces == 2


class UnionFind:
    ''' Union_Find Data Structure for maintaining Components '''

    # Constructor
    # Complexity: Θ(n)
    def __init__(self, n: int) -> None:
        self.initial_dots: int = n
        self.length: int = n
        self.union_find: Vector = list(range(n))
        self.size: Vector = [1] * n

    # Complexity: Θ(⍺(n))
    def find(self, i: int) -> int:
        ''' Method to find the blob the dot is connected to (w/ compression)'''
        if self.union_find[i] != i:
            self.union_find[i] = self.find(self.union_find[i])

        return self.union_find[i]

    # Complexity: Θ(⍺(n))
    def union(self, dot_a: int, dot_b: int) -> None:
        ''' Connects two points and makes them one blob '''
        r_a: int = self.find(dot_a)
        r_b: int = self.find(dot_b)

        if self.size[r_a] > self.size[r_b]:
            r_a, r_b = r_b, r_a

        self.union_find[r_a] = r_b
        self.size[r_a] = self.size[r_a] + self.size[r_b]

    # Complexity: Θ(1)
    def add(self) -> None:
        ''' Adds a point to the union-find '''
        self.union_find.append(self.length)
        self.size.append(1)
        self.length += 1


# Complexity: Θ(n * ⍺(n))
def dots_in_component(dot: int, union_find: UnionFind) -> Vector:
    ''' Find all dots in a single component '''
    dots: Vector = []
    dot_comp: int = union_find.find(dot)

    for i in range(union_find.length):
        if union_find.find(i) == dot_comp:
            dots.append(i)

    return dots


# Complexity: Θ(n * ⍺(n))
def check_euler_comp(dot_a: int,
                     union_find: UnionFind,
                     graph: Vector2D,
                     faces: Vector2D) -> bool:
    ''' Check if component in dot follows euler's formula '''
    dots: Vector = dots_in_component(dot_a, union_find)
    unique_faces: Set[int] = set()

    for dot in dots:
        for face in faces[dot]:
            unique_faces.add(face)

    num_vertices: int = len(dots)
    num_edges: int = int(sum([len(graph[d]) for d in dots]) / 2)
    num_faces: int = len(unique_faces)

    return euler_formula(num_vertices, num_edges, num_faces)


# Complexity: Θ(f_n^2) -> Θ(1) | f_n -> max == 3
def compare_faces(dot_a: int, dot_b: int, faces: Vector2D) -> Vector:
    ''' Check which faces dot_a and dot_b have in common'''
    sim_faces: Vector = []

    for face_a in faces[dot_a]:
        if face_a in faces[dot_b]:
            sim_faces.append(face_a)

    return sim_faces


# Complexity: Θ(n * f_n) -> Θ(n)
def dots_in_face(face_num: int, faces: Vector2D) -> Vector:
    ''' Find all dots that are in a particular face'''
    dots: Vector = []

    for i, face in enumerate(faces):
        if face_num in face:
            dots.append(i)

    return dots


class SproutsGraph:
    ''' Sprouts Graph setting up entire board '''

    # Constructor
    # Complexity: Θ(n)
    def __init__(self, n: int) -> None:
        self.initial_dots: int = n
        self.union_find: UnionFind = UnionFind(n)
        self.graph: Vector2D = [[]] * n
        self.faces: Vector2D = [[0]] * n
        self.face_num: int = 1

    # Complexity: Θ()
    def connect_within_components(self,
                                  dot_a: int,
                                  dot_b: int,
                                  union_find: UnionFind,
                                  graph: Vector2D,
                                  sim_faces: Vector,
                                  faces: Vector2D) -> Vector2D:
        ''' Connect two dots within the same component '''
        # TODO: Connect components together in way that is unique
        # to connecting within components
        components: Dict[int, Set[int]] = {}
        dots: Vector

        for face in sim_faces:
            dots = dots_in_face(face, faces)

            # Pair Dots by Components
            # Complexity: O(n * a(n))
            for dot in dots:
                comp_id: int = union_find.find(dot)
                if comp_id in components:
                    components[comp_id].add(dot)
                else:
                    components[comp_id] = {dot}
            # TODO: Check if Connecting Component is a Cycle
            conn_comp: int = union_find.find(dot_a)


            # TODO: Check number of different ways it can be connected

            # TODO: Reassign the faces bordering each dot based on way that
            # it is chosen to be connected
            # including adding the new face
            # (if cycle, then choose which dots get entrapped)

            # Reset for next iteration
            components = {}

        return faces

    # Complexity: Θ()
    def connect(self, dot_a: int, dot_b: int, is_check: bool = False) -> bool:
        ''' Connect dot_a and dot_b to eachother '''
        graph: Vector2D = deepcopy(self.graph)
        union_find: UnionFind = deepcopy(self.union_find)
        faces: Vector2D = deepcopy(self.faces)
        face_num: int = self.face_num

        # Check if contains same faces
        sim_faces: Vector = compare_faces(dot_a, dot_b, faces)
        if sim_faces == []:
            return False

        # Connect with unique properties of w/ components
        if self.union_find.find(dot_a) == self.union_find.find(dot_b):
            faces = self.connect_within_components(dot_a, dot_b, union_find,
                                                   graph, sim_faces, faces)
            face_num += 1
        else:
            faces.append(sim_faces)

        # Connect Graph
        graph.append([dot_a, dot_b])
        graph[dot_a].append(len(graph) - 1)
        graph[dot_b].append(len(graph) - 1)

        # Check Degrees
        if len(graph[dot_a]) > 3 or len(graph[dot_b]) > 3:
            return False

        # Connect union_find
        union_find.add()
        new_dot: int = union_find.union_find[union_find.length - 1]
        union_find.union(dot_a, new_dot)
        union_find.union(dot_b, new_dot)

        # After Connection, check if connection failed or euler formula fails
        if not check_euler_comp(dot_a, union_find, graph, faces):
            return False

        # Temp Data Structures replace old ones with success
        if not is_check:
            self.graph = graph
            self.union_find = union_find
            self.faces = faces
            self.face_num = face_num

        return True
