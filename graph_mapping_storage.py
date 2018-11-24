from graph import Graph


def to_graph_vertex(word, is_offensive):
    if is_offensive:
        return word + '|1'
    return word + '|0'


def from_graph_vertex(vertex):
    split_tok = vertex.split('|')
    if split_tok[1] == '1':
        return split_tok[0], True
    return split_tok[0], False


class GraphMappingStorage:
    def __init__(self, graph=None):
        if graph is None:
            graph = Graph()
        self.graph = graph

    def has_vertex(self, vertex):
        return vertex in self.graph.vertices()

    def add_non_offensive_mapping(self, offensive_word, non_offensive_replacements):
        offensive_word_vertex = to_graph_vertex(offensive_word, True)
        non_offensive_replacement_vertices = [to_graph_vertex(word, False) for word in non_offensive_replacements]

        self.graph.add_vertex(offensive_word_vertex)

        for non_offensive_vertex in non_offensive_replacement_vertices:
            if not self.has_vertex(non_offensive_vertex):
                self.graph.add_vertex(non_offensive_vertex)
            self.graph.add_edge((offensive_word_vertex, non_offensive_vertex))

    def get_non_offensive_alternatives(self, offensive_word):
        offensive_word_vertex = to_graph_vertex(offensive_word, True)
        if not self.has_vertex(offensive_word_vertex):
            return None
        offensive_word_neighbors = self.graph.get_neighbors(offensive_word_vertex)
        neighbors_distance_two = []
        for offensive_word_neighbor_vertex in offensive_word_neighbors:
            neighbors_distance_two.extend(self.graph.get_neighbors(offensive_word_neighbor_vertex))
        all_neighbors = offensive_word_neighbors + neighbors_distance_two
        nonoffensive_vertices = [from_graph_vertex(vertex) for vertex in all_neighbors]
        return list(set([v[0] for v in nonoffensive_vertices if v[1] is False]))
