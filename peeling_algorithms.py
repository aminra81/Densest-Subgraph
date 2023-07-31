import heapq

import llist


def greedy_peeling_algorithm(number_of_vertices, adjacency_graph):
    answer = []
    is_deleted = [0 for _ in range(number_of_vertices + 1)]
    list_of_degrees = [llist.dllist() for _ in range(1, number_of_vertices + 1)]
    degrees = [0 for _ in range(number_of_vertices + 1)]
    nodes = []
    for vertex in range(1, number_of_vertices + 1):
        degrees[vertex] = len(adjacency_graph[vertex])
        list_of_degrees[degrees[vertex]].append(vertex)
        new_node = list_of_degrees[degrees[vertex]].last
        nodes.append(new_node)
    min_deg = 0
    i = number_of_vertices
    been = dict()
    while i > 1:
        for deg in range(min_deg, number_of_vertices):
            if len(list_of_degrees[deg]) > 0:
                current_vertex = list_of_degrees[deg].popleft()
                is_deleted[current_vertex] = 1
                been[current_vertex] = 1
                answer.append(current_vertex)
                for neighbor in adjacency_graph[current_vertex]:
                    if is_deleted[neighbor]:
                        continue
                    neighbor_node = nodes[neighbor - 1]
                    list_of_degrees[degrees[neighbor_node.value]].remove(neighbor_node)
                    degrees[neighbor_node.value] = degrees[neighbor_node.value] - 1
                    list_of_degrees[degrees[neighbor_node.value]].append(neighbor_node.value)
                    nodes[neighbor_node.value - 1] = list_of_degrees[degrees[neighbor_node.value]].last
                min_deg = deg - 1
                break
        i = i - 1
    max_ans = 0.0
    is_in_set = [0 for _ in range(number_of_vertices + 1)]
    for i in range(number_of_vertices + 1):
        if is_deleted[i] == 0:
            is_in_set[i] = 1

    edges = 0
    for i in range(len(answer) - 1, -1, -1):
        current_vertex = answer[i]
        is_in_set[current_vertex] = 1
        for neighbor in adjacency_graph[current_vertex]:
            if is_in_set[neighbor]:
                edges = edges + 1
        set_len = len(answer) - i + 1
        if edges / set_len > 35.0:
            is_there = []
            for t in range(1, number_of_vertices + 1):
                if not is_deleted[t]:
                    is_there.append(t)
        max_ans = max(max_ans, edges / set_len)
    return max_ans


def iterative_greedy_peeling(number_of_vertices, adjacency_graph, T):
    load = [0 for i in range(number_of_vertices + 1)]
    deg = [0 for i in range(number_of_vertices + 1)]
    deleted_vertex = [[0 for j in range(number_of_vertices + 1)] for i in range(T + 1)]
    for i in range(1, T + 1):
        is_deleted = [0 for i in range(number_of_vertices + 1)]
        pq = []
        for j in range(1, number_of_vertices + 1):
            deg[j] = len(adjacency_graph[j])
            pq.append((load[j] + deg[j], j))
        heapq.heapify(pq)
        j = 0
        while pq:
            min_l, vertex = heapq.heappop(pq)
            if is_deleted[vertex]:
                continue
            j = j + 1
            is_deleted[vertex] = 1
            deleted_vertex[i][j] = vertex
            load[vertex] = load[vertex] + deg[vertex]
            for adj_vertex in adjacency_graph[vertex]:
                if not is_deleted[adj_vertex]:
                    deg[adj_vertex] = deg[adj_vertex] - 1
                    heapq.heappush(pq, (load[adj_vertex] + deg[adj_vertex], adj_vertex))
    max_ans = 0
    for i in range(1, T + 1):
        is_in_set = [0 for _ in range(number_of_vertices + 1)]
        edges = 0
        for j in range(number_of_vertices, 0, -1):
            current_vertex = deleted_vertex[i][j]
            is_in_set[current_vertex] = 1
            for neighbor in adjacency_graph[current_vertex]:
                if is_in_set[neighbor]:
                    edges = edges + 1
            set_len = number_of_vertices - j + 1
            max_ans = max(max_ans, edges / set_len)
    return max_ans
