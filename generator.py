import random
import math


def generate_sparse_graph(n, m):
    edges = random.sample(range(0, math.comb(n, 2)), m)
    edge_list = []
    for edge_code in edges:
        u = int((1 + math.sqrt(1 + 8 * edge_code)) / 2)
        v = edge_code - math.comb(u, 2)

        u = u + 1
        v = v + 1

        edge_list.append((u, v))
    return n, m, edge_list


def generate_dense_graph(n, m):
    edges = [i for i in range(0, math.comb(n, 2))]
    random.shuffle(edges)
    edge_list = []
    for i in range(math.comb(n, 2) - m, math.comb(n, 2)):
        edge_code = edges[i]
        u = int((1 + math.sqrt(1 + 8 * edge_code)) / 2)
        v = edge_code - math.comb(u, 2)

        u = u + 1
        v = v + 1

        edge_list.append((u, v))
    return n, m, edge_list


def generate_worst_case(t, p):
    n = t + 1 + 2 * p
    m = t + p
    edge_list = []
    for i in range(1, t + 1):
        edge_list.append((1, 1 + i))

    for i in range(1, p + 1):
        edge_list.append((2 * i - 1 + (t + 1), 2 * i + (t + 1)))
    return n, m, edge_list
