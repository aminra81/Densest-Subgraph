from algorithms.goldberg import goldberg_algorithm
import math

import llist


def constructGraph(number_of_vertices, adjacency_graph, is_deleted, current_number_of_vertices):
    current_adjacency_graph = [[] for _ in range(current_number_of_vertices + 1)]
    index = dict()
    count = 0
    for current_vertex in range(1, number_of_vertices + 1):
        if not is_deleted[current_vertex]:
            count += 1
            index[current_vertex] = count
    for current_vertex in range(number_of_vertices + 1):
        if not is_deleted[current_vertex]:
            for neighbor in adjacency_graph[current_vertex]:
                if not is_deleted[neighbor]:
                    current_adjacency_graph[index[current_vertex]].append(index[neighbor])
    return current_adjacency_graph


def hybrid(number_of_vertices, adjacency_graph):
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
    limit = math.sqrt(number_of_vertices)
    checked = False
    been = dict()
    max_ans = 0.0
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
        if i <= limit and not checked:
            checked = True
            limit_adjacency_graph = constructGraph(number_of_vertices, adjacency_graph, is_deleted, i)
            answer = goldberg_algorithm(i, limit_adjacency_graph)

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
        '''if edges / set_len > 35.0:
            is_there = []
            for t in range(1, number_of_vertices + 1):
                if not is_deleted[t]:
                    is_there.append(t)'''
        max_ans = max(max_ans, edges / set_len)
    return max_ans
