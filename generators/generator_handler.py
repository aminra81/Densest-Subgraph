from enum import Enum

from generators import generator


class TestType(Enum):
    SPARSE = "sparse"
    DENSE = "dense"
    WORST_CASE = "worst-case"


class TestGenerator:
    def __init__(self, directory):
        self.directory = directory

    def _generate_graph(self, graph_generator, test_number, test_type, num_vertices, num_edges):
        filename = f"{self.directory}/{test_type.value}{test_number}.txt"
        n, m, edge_list = graph_generator(num_vertices, num_edges)
        with open(filename, "w") as out_f:
            out_f.write(f"{n} {m}\n")
            for u, v in edge_list:
                out_f.write(f"{u} {v}\n")

    def generate_sparse(self, test_number, num_vertices, num_edges):
        self._generate_graph(generator.generate_sparse_graph, test_number, TestType.SPARSE, num_vertices, num_edges)

    def generate_dense(self, test_number, num_vertices, num_edges):
        self._generate_graph(generator.generate_dense_graph, test_number, TestType.DENSE, num_vertices, num_edges)

    def generate_worst_case(self, test_number, num_vertices, num_edges):
        self._generate_graph(generator.generate_worst_case, test_number, TestType.WORST_CASE, num_vertices, num_edges)

    def generate_from_sizes_file(self, sizes_file, generate_function):
        test_number = 1
        with open(f"tests/{sizes_file}") as data_file:
            for line in data_file:
                n, m = [int(x) for x in line.split()]
                generate_function(test_number, n, m)
                test_number += 1
