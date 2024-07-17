import cvxpy as cp


def charikar_lp_algorithm(number_of_vertices, adjacency):
    m = 0
    edges = []
    adjacency_graph = [[] for _ in range(number_of_vertices)]
    for i in range(1, number_of_vertices + 1):
        for v in adjacency[i]:
            adjacency_graph[i - 1].append(v - 1)
            if v < i:
                m = m + 1
                edges.append((v - 1, i - 1))

    x = cp.Variable(m)
    y = cp.Variable(number_of_vertices)
    constraints = []
    edges_number = {}
    i = 0
    for edge in edges:
        edges_number[i] = edge
        u, v = edge
        constraints.append(x[i] <= y[u])
        constraints.append(x[i] <= y[v])
        i += 1
    constraints.append(sum(y) == 1)
    constraints.append(0 <= x)
    constraints.append(0 <= y)
    objective = cp.Maximize(sum(x))
    problem = cp.Problem(objective, constraints)
    problem.solve()
    answer = []
    answer_value = -1
    answer_bound = 0
    current_answer = []
    nodes_with_value = []
    for i in range(number_of_vertices):
        nodes_with_value.append((i, y[i].value))
    nodes_with_value = sorted(
        nodes_with_value,
        key=lambda z: z[1],
        reverse=True
    )
    # print(nodes_with_value)
    for node in nodes_with_value:
        current_answer.append(node[0])
        edges_weight = 0
        for u in current_answer:
            for v in adjacency_graph[u]:
                if v in current_answer:
                    edges_weight += 1
        edges_weight /= 2
        if (edges_weight / len(current_answer)) > answer_value:
            answer_bound = node[0]
            answer_value = (edges_weight / len(current_answer))
    for node in nodes_with_value:
        if node[0] != answer_bound:
            answer.append(node[0])
        else:
            answer.append(node[0])
            break

    edges_weight = 0
    for u in answer:
        for v in adjacency_graph[u]:
            if v in answer:
                edges_weight += 1
    edges_weight /= 2
    return edges_weight / len(answer)
