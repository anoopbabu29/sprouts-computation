''' Modules '''
from typing import List, Tuple, Set
import copy
import matplotlib.pyplot as plt
import networkx as nx

Vector = List[int]
Vector2D = List[List[int]]
Vector3D = List[List[List[int]]]
Vectored2DSet = List[List[Set[int]]]


def common_faces(faces_a: Set[int], faces_b: Set[int]) -> Vector:
    ''' Finds face is common => Θ(n^2) | max(n) = 3'''
    faces = []

    for face_a in faces_a:
        if face_a in faces_b:
            faces.append(face_a)

    return faces


def find_trace_ind(trace: Vector, dot: int) -> Vector:
    ''' Finds index of dots within the trace => O(n) '''
    ind_lis: Vector = [i for i, curr_dot in enumerate(trace)
                       if curr_dot == dot]

    # Raise exception if cannot find the dot within trace
    if ind_lis == []:
        print(f'Error: Unable to find dot {dot} within trace {trace}')
        raise Exception

    return ind_lis


def find_trace(trace_set: Vectored2DSet, face_ind: int, dot: int) -> int:
    ''' Finds trace associated with specified dot in specified face => O(n) '''
    for trace_ind, set_of_trace in enumerate(trace_set[face_ind]):
        if dot in set_of_trace:
            return trace_ind

    return -1


def to_graph(traces: Vector3D) -> nx.Graph:
    ''' Converts trace graph to the network graph type => O(f*t*d)'''
    graph = nx.Graph()

    # Add each edge in graph along each trace
    for traces_per_face in traces:
        for trace in traces_per_face:
            for i, dot in enumerate(trace):
                graph.add_edge(dot, trace[(i+1) % len(trace)])

    return graph


def visualize_graph(traces: Vector3D, is_save: bool = False) -> None:
    ''' Shows networkx graph of Sprouts => ??? '''
    nx.draw_planar(to_graph(traces), with_labels=True)

    if is_save:
        plt.savefig('sprouts.png')

    plt.show()


class SproutsGraph:
    ''' Sprouts Graph setting up entire board '''
    def __init__(self, n: int) -> None:
        ''' Constructor => Θ(n) '''
        self.initial_dots: int = n
        self.num_dots: int = n
        self.num_faces: int = 1
        self.num_connected: Vector = [0] * n
        self.faces: List[Set[int]] = [set([0]) for _ in range(n)]
        self.traces: Vector3D = [[[dot] for dot in range(n)]]
        self.trace_set: Vectored2DSet = [[set([dot]) for dot in range(n)]]

    def add_new_dot(self, dot_a: int, dot_b: int) -> None:
        ''' Adds the new dot to the above data structures => O(n)'''
        self.num_dots += 1

        # Increase number of edges for each dot & new dot
        self.num_connected[dot_a] += 1
        self.num_connected[dot_b] += 1
        self.num_connected.append(2)

    def will_dot_overflow(self, dot_a: int, dot_b: int) -> bool:
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
        prompt_ind: str = 'Pick index {} from trace {}: '
        pos: Tuple[int, int] = (0, 1)  # Note: Used to easily swap dots a & b

        trace_a: Vector = self.traces[face][trace_inds[pos[0]]]
        trace_b: Vector = self.traces[face][trace_inds[pos[1]]]

        # Find index of each dot within the trace
        dot_a_inds: Vector = find_trace_ind(trace_a, dots[pos[0]])
        dot_b_inds: Vector = find_trace_ind(trace_b, dots[pos[1]])

        if is_enumerate:
            # TODO: Complete this
            return False

        dot_ind_a: int = dot_a_inds[
            int(input(prompt_ind.format(dot_a_inds, trace_a)))]

        dot_ind_b: int = dot_b_inds[
            int(input(prompt_ind.format(dot_b_inds, trace_b)))]

        # Format new trace to add to trace_a
        new_trace: Vector = ([dots[pos[0]], self.num_dots] +
                             trace_b[dot_ind_b:len(trace_b)] +
                             trace_b[0:dot_ind_b] +
                             [dots[pos[1]], self.num_dots, dots[pos[0]]])

        if len(trace_b) == 1:
            new_trace.pop(-3)
        if dot_ind_a == 0:
            new_trace.pop(-1)

        # Add new trace to trace_a & make change to traces
        trace_a = (trace_a[0:dot_ind_a] +
                   new_trace +
                   trace_a[dot_ind_a+1:len(trace_a)])

        self.traces[face][trace_inds[pos[0]]] = trace_a
        self.traces[face].pop(trace_inds[pos[1]])

        # Combining both trace sets of trace a & b, adding new dot
        self.trace_set[face][trace_inds[pos[0]]] = (
            self.trace_set[face][trace_inds[pos[0]]]
            .union(self.trace_set[face][trace_inds[pos[1]]]))

        self.trace_set[face][trace_inds[pos[0]]].add(self.num_dots)
        self.trace_set[face].pop(trace_inds[pos[1]])

        # Add new dot
        self.add_new_dot(dots[pos[0]], dots[pos[1]])
        self.faces.append(set([face]))

        return True

    def connect_dots_in_trace(self,
                              face: int,
                              trace_ind: int,
                              dots: Tuple[int, int],
                              is_enumerate: bool = False) -> bool:
        ''' Connects dots in the same trace => Θ() '''
        trace: Vector = self.traces[face][trace_ind]

        # Find index of each dot within the trace
        dot_a_inds: Vector = find_trace_ind(trace, dots[0])
        dot_b_inds: Vector = find_trace_ind(trace, dots[1])

        if is_enumerate:
            # TODO: Structure in such a way, easy to see all possibilities
            return False

        # Assigning which face to be connected
        dot_ind_a: int = dot_a_inds[
            int(input('Pick index {} from trace {}: '
                      .format(dot_a_inds, trace)))]

        dot_ind_b: int = dot_b_inds[
            int(input('Pick index {} from trace {}: '
                      .format(dot_b_inds, trace)))]

        # Order dots by lower # to higher # to enforce order
        if dot_ind_a > dot_ind_b:
            dot_ind_a, dot_ind_b = dot_ind_b, dot_ind_a
            dots = (dots[1], dots[0])

        # Format new trace, and add to traces
        new_trace: Vector = trace[dot_ind_a:dot_ind_b+1] + [self.num_dots]
        orig_trace_set: Set[int] = copy.deepcopy(
            self.trace_set[face][trace_ind])

        trace = (trace[0:dot_ind_a+1] + [self.num_dots] +
                 trace[dot_ind_b:len(trace)])

        if trace[0] == trace[-1]:
            trace.pop(-1)

        self.traces[face][trace_ind] = trace
        self.traces.append([new_trace])

        self.trace_set[face][trace_ind] = set(self.traces[face][trace_ind])
        self.trace_set.append([set(new_trace)])

        # Add new face to connected dots
        self.faces[dots[0]].add(self.num_faces)
        self.faces[dots[1]].add(self.num_faces)
        self.faces.append(set([face, self.num_faces]))
        self.num_faces += 1

        # Add new dot
        self.add_new_dot(dots[0], dots[1])

        for dot in orig_trace_set:
            if dot not in dots and dot != (self.num_dots - 1):
                if dot not in self.trace_set[face][trace_ind]:
                    print(f'Removed {face} from dot {dot}')
                    self.faces[dot].remove(face)
                if dot in self.trace_set[-1][0]:
                    print(f'Added {self.num_faces - 1} to dot {dot}')
                    self.faces[dot].add(self.num_faces - 1)

        # See if other traces within face exist
        other_traces: Vector2D = (self.traces[face][0:trace_ind] +
                                  self.traces[face][trace_ind+1:])

        # If other traces exist, user chooses which traces to move to new face
        if other_traces != []:
            moved_traces: Vector = [int(char) for char in
                                    input('Pick which traces of ' +
                                          f'{other_traces} will be moved ' +
                                          'to inside new face: ')]
            moved_traces.insert(trace_ind, 0)

            for i, trace in enumerate(self.traces[face]):
                if moved_traces[i] == 1:
                    for dot in self.trace_set[face][i]:
                        self.faces[dot].remove(face)
                        self.faces[dot].add(self.num_faces - 1)

            self.traces[-1] += [trace for i, trace
                                in enumerate(self.traces[face])
                                if moved_traces[i] == 1]
            self.trace_set[-1] += [trace_set for i, trace_set
                                   in enumerate(self.trace_set[face])
                                   if moved_traces[i] == 1]

            self.traces[face] = [trace for i, trace
                                 in enumerate(self.traces[face])
                                 if moved_traces[i] == 0]
            self.trace_set[face] = [trace_set for i, trace_set
                                    in enumerate(self.trace_set[face])
                                    if moved_traces[i] == 0]

        return True

    def connect(self, dot_a: int, dot_b: int,
                is_enumerate: bool = False) -> bool:
        ''' Connects two dots in the graph if possible => Θ() '''
        if self.will_dot_overflow(dot_a, dot_b):
            return False

        # Check faces in common if any
        poss_faces: Vector = list(self.faces[dot_a]
                                  .intersection(self.faces[dot_b]))

        if poss_faces == []:
            return False

        if is_enumerate:
            # TODO: Structure in such a way, easy to see all possibilities
            return False

        # Choose common face and
        face_ind: int = poss_faces[
            int(input(f'Pick face via index {poss_faces}: '))]

        trace_ind_a: int = find_trace(self.trace_set, face_ind, dot_a)
        trace_ind_b: int = find_trace(self.trace_set, face_ind, dot_b)

        if trace_ind_a == trace_ind_b:
            return self.connect_dots_in_trace(face_ind, trace_ind_a,
                                              (dot_a, dot_b))

        return self.connect_traces(face_ind, (trace_ind_a, trace_ind_b),
                                   (dot_a, dot_b))

    def can_connect(self) -> bool:
        ''' Check to see if a connetion can be made'''
        for traces_per_face in self.traces:
            num_edges_to_add: int = 0
            for trace in traces_per_face:
                for dot in trace:
                    # Check if a dot can connect to itself
                    if self.num_connected[dot] <= 1:
                        return True

                    # Check if a dot can connect to another
                    if self.num_connected[dot] == 2:
                        num_edges_to_add += 1

                    if num_edges_to_add >= 2:
                        return True

        return False

    def show_state(self) -> None:
        ''' Prints state of graph for debugging purposes '''
        print(f'''
        Initial Dots    = {self.initial_dots}
        # of Dots       = {self.num_dots}
        # of Faces      = {self.num_faces}
        Edges per Dot   = {self.num_connected}
        Faces per Dot   = {self.faces}
        Traces per Face = {self.traces}
        TraceSet per F. = {self.trace_set}

        ''')

    def play(self) -> None:
        ''' Plays the game of sprouts '''
        while self.can_connect():
            try:
                self.show_state()
                visualize_graph(self.traces)
                dot_a: int = int(input('Dot A: '))
                dot_b: int = int(input('Dot B: '))
                print()

                while not self.connect(dot_a, dot_b):
                    print('Those dots cannot connect')
                    visualize_graph(self.traces)
                    dot_a: int = int(input('Dot A: '))
                    dot_b: int = int(input('Dot B: '))

            except Exception as error:
                print(f'Unexpected error: {error}')
                print('Try Again')

            finally:
                print()

        print('Game Finished!')
        self.show_state()
        visualize_graph(self.traces)


def main():
    ''' Main function '''
    sprouts = SproutsGraph(2)
    sprouts.play()


if __name__ == '__main__':
    main()
