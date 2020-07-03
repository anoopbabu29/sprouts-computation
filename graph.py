''' Modules '''
from typing import List, Tuple, Set
import matplotlib.pyplot as plt
import networkx as nx

Vector = List[int]
Vector2D = List[List[int]]
Vector3D = List[List[List[int]]]
Vectored2DSet = List[List[Set[int]]]


def common_faces(faces_a: Set[int], faces_b: Set[int]) -> Vector:
    ''' Finds face is common => Θ(n^2) | max len = 3 => Θ(1)'''
    faces = []

    for face_a in faces_a:
        if face_a in faces_b:
            faces.append(face_a)

    return faces


def find_trace_ind(trace: Vector, dot: int) -> Vector:
    ''' Finds index of dots within the trace => O() '''
    return [i for i, curr_dot in enumerate(trace) if curr_dot == dot]


def find_trace(trace_set: Vectored2DSet, face_ind: int, dot: int) -> int:
    ''' Finds trace associated with specified dot in specified face => O(n) '''
    for trace_ind, set_of_trace in enumerate(trace_set[face_ind]):
        if dot in set_of_trace:
            return trace_ind

    return -1


def to_graph(traces: Vector3D) -> nx.Graph:
    ''' Converts trace graph to the network graph type'''
    graph = nx.Graph()

    for traces_per_face in traces:
        for trace in traces_per_face:
            for i, dot in enumerate(trace):
                graph.add_edge(dot, trace[(i+1) % len(trace)])

    return graph


def visualize_graph(traces: Vector3D, is_save: bool = False) -> None:
    ''' Shows networkx graph of Sprouts '''
    nx.draw_planar(to_graph(traces), with_labels=True)

    if is_save:
        plt.savefig('sprouts.png')
    # clearing the current plot
    plt.clf()


class SproutsGraph:
    ''' Sprouts Graph setting up entire board '''
    def __init__(self, n: int) -> None:
        ''' Constructor => Θ(n) '''
        self.initial_dots: int = n
        self.num_dots: int = n
        self.num_faces: int = 1
        self.num_connected: Vector = [0] * n
        self.faces: List[Set[int]] = [set([0])] * n
        self.traces: Vector3D = [[[dot] for dot in range(n)]]
        self.trace_set: Vectored2DSet = [[set([dot]) for dot in range(n)]]

    def add_new_dot(self, dot_a: int, dot_b: int) -> None:
        ''' Adds the new dot to the above data structures => O()'''
        self.num_dots += 1

        self.num_connected[dot_a] += 1
        self.num_connected[dot_b] += 1
        self.num_connected.append(2)

        self.faces.append(self.faces[dot_a] | self.faces[dot_b])

    def has_dot_overflown(self, dot_a: int, dot_b: int) -> bool:
        ''' Condition making sure that after connecting,
            dot doesn't have more than 3 edges => O(1) '''
        return (self.num_connected[dot_a] > 2 or
                self.num_connected[dot_b] > 2 or
                (dot_a == dot_b and self.num_connected[dot_a] > 1))

    def connect_traces(self,
                       face: int,
                       trace_inds: Tuple[int, int],
                       dots: Tuple[int, int],
                       is_enumerate: bool = False) -> bool:
        ''' Connects dots from different traces => Θ() '''
        prompt_ind: str = 'Pick index {} from trace {}'
        pos_a: int = 0
        pos_b: int = 1

        trace_a: Vector = self.traces[face][trace_inds[pos_a]]
        trace_b: Vector = self.traces[face][trace_inds[pos_b]]

        dot_a_inds: Vector = find_trace_ind(trace_a, dots[pos_a])
        dot_b_inds: Vector = find_trace_ind(trace_b, dots[pos_b])

        if is_enumerate:
            # TODO: Complete this
            return False

        dot_ind_a: int = dot_a_inds[
            int(input(prompt_ind.format(dot_a_inds, trace_a)))]

        dot_ind_b: int = dot_b_inds[
            int(input(prompt_ind.format(dot_b_inds, trace_b)))]

        trace_b = ([dots[pos_a], self.num_dots] +
                   trace_b[dot_ind_b:len(trace_b)] + trace_b[0:dot_ind_b] +
                   [dots[pos_b], self.num_dots, dots[pos_a]])

        trace_a = (trace_a[0:dot_ind_a] +
                   trace_b +
                   trace_a[dot_ind_a+1:len(trace_a)])

        self.traces[face].pop(trace_inds[pos_b])

        self.trace_set[face][trace_inds[pos_a]] = (
            self.trace_set[face][trace_inds[pos_a]]
            .union(self.trace_set[face][trace_inds[pos_b]]))

        self.trace_set[face][trace_inds[pos_a]].add(self.num_dots)
        self.trace_set[face].pop(trace_inds[pos_b])

        self.add_new_dot(dots[pos_a], dots[pos_b])

        return True

    def connect_dots_in_trace(self,
                              face: int,
                              trace_ind: int,
                              dots: Tuple[int, int],
                              is_enumerate: bool = False) -> bool:
        ''' Connects dots in the same trace => Θ() '''
        trace: Vector = self.traces[face][trace_ind]

        dot_a_inds: Vector = find_trace_ind(trace, dots[0])
        dot_b_inds: Vector = find_trace_ind(trace, dots[1])

        if is_enumerate:
            # TODO: Structure in such a way, easy to see all possibilities
            return False

        dot_ind_a: int = dot_a_inds[
            int(input('Pick index {} from trace {}'
                      .format(dot_a_inds, trace)))]

        dot_ind_b: int = dot_b_inds[
            int(input('Pick index {} from trace {}'
                      .format(dot_b_inds, trace)))]

        if dot_ind_a > dot_ind_b:
            dot_ind_a, dot_ind_b = dot_ind_b, dot_ind_a
            dots = (dots[1], dots[0])

        new_trace: Vector = trace[dot_ind_a:dot_ind_b+1] + [self.num_dots]

        trace = (trace[0:dot_ind_a+1] +
                 [self.num_dots] +
                 trace[dot_ind_b:len(trace)])

        self.traces.append([new_trace])

        self.trace_set[face][trace_ind] = set(trace)
        self.trace_set.append([set(new_trace)])

        other_traces: Vector2D = (self.traces[face][0:trace_ind] +
                                  self.traces[face][trace_ind+1:])
        moved_traces: Vector = [int(char) for char in
                                input('Pick which traces of ' +
                                      f'{other_traces}' +
                                      'will be moved to inside new face')]

        self.traces[-1] += [trace for i, trace in enumerate(other_traces)
                            if moved_traces == 1]

        for i in range(len(self.traces[face]) - 1, -1, -1):
            if moved_traces[i] == 0:
                self.traces[face][trace_ind].pop(i)

        self.faces[dots[0]].add(self.num_faces)
        self.faces[dots[1]].add(self.num_faces)

        self.num_faces += 1

        self.add_new_dot(dots[0], dots[1])

        return True

    def connect(self, dot_a: int, dot_b: int,
                is_enumerate: bool = False) -> bool:
        ''' Connects two dots in the graph if possible => Θ() '''
        if self.has_dot_overflown(dot_a, dot_b):
            return False

        poss_faces: Vector = list(self.faces[dot_a]
                                  .intersection(self.faces[dot_b]))

        if poss_faces == []:
            return False

        if is_enumerate:
            # TODO: Structure in such a way, easy to see all possibilities
            return False

        face_ind: int = int(input(f'Pick face via index {poss_faces}'))

        trace_ind_a: int = find_trace(self.trace_set, face_ind, dot_a)
        trace_ind_b: int = find_trace(self.trace_set, face_ind, dot_a)

        if trace_ind_a == trace_ind_b:
            return self.connect_dots_in_trace(face_ind, trace_ind_a,
                                              (dot_a, dot_b))

        return self.connect_traces(face_ind, (trace_ind_a, trace_ind_b),
                                   (dot_a, dot_b))


def main():
    ''' Main function '''


if __name__ == '__main__':
    main()
