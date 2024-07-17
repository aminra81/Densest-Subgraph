import maxflow


def goldberg_algorithm(number_of_vertices, adjacency):
    m = 0
    edges = []
    adjacency_graph = [[] for _ in range(number_of_vertices)]
    for i in range(1, number_of_vertices + 1):
        for v in adjacency[i]:
            adjacency_graph[i - 1].append(v - 1)
            if v < i:
                m = m + 1
                edges.append((v - 1, i - 1))

    lower_bound = 0
    upper_bound = m / 2
    delta = 1 / (number_of_vertices * (number_of_vertices - 1))
    while (upper_bound - lower_bound) >= delta:
        iteration = 0
        mid = (upper_bound + lower_bound) / 2
        cut = goldberg_cut(adjacency_graph, edges, number_of_vertices, m, mid)
        if not cut:
            upper_bound = mid
        else:
            lower_bound = mid
        # print("the cut in iteration ", iteration, " is ", cut)
        # print("the lower-bound is ", lower_bound, " and the upperbound is ", upper_bound)
        iteration += 1
    cut = goldberg_cut(adjacency_graph, edges, number_of_vertices, m, lower_bound)
    answer = cut

    edges_weight = 0
    for u in answer:
        for v in adjacency_graph[u]:
            if v in answer:
                edges_weight += 1
    edges_weight /= 2
    return edges_weight / len(answer)


def goldberg_cut(G, edges, n, m, mid):
    graph = maxflow.Graph[float](n, m)
    nodes = graph.add_nodes(n)
    for edge in edges:
        u, v = edge
        graph.add_edge(nodes[u], nodes[v], 1, 1)  # all edge weights are twice the graph in goldberg's algorithm.
    for i in range(n):
        graph.add_tedge(nodes[i], len(G[i]), 2 * mid)
    cut = []
    flow = graph.maxflow()
    # print(flow)
    for i in nodes:
        if graph.get_segment(nodes[i]) == 0:
            cut.append(nodes[i])
    return cut
