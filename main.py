import math
import multiprocessing
import time

import generator
from charikar import charikar_lp_algorithm
from goldberg import goldberg_algorithm
from peeling_algorithms import greedy_peeling_algorithm, iterative_greedy_peeling
from os import listdir

import matplotlib.pyplot as plt

input_tests_directory = "tests/input/"


def generate_sparse(test_number, number_of_vertices, number_of_edges):
    out_f = open(input_tests_directory + "sparse" + str(test_number) + ".txt", "w")
    n, m, edge_list = generator.generate_sparse_graph(number_of_vertices, number_of_edges)
    out_f.write(str(n) + " " + str(m) + "\n")
    for edge in edge_list:
        u, v = edge
        out_f.write(str(u) + " " + str(v) + "\n")
    out_f.close()


def generate_dense(test_number, number_of_vertices, number_of_edges):
    out_f = open(input_tests_directory + "dense" + str(test_number) + ".txt", "w")
    n, m, edge_list = generator.generate_dense_graph(number_of_vertices, number_of_edges)
    out_f.write(str(n) + " " + str(m) + "\n")
    for edge in edge_list:
        u, v = edge
        out_f.write(str(u) + " " + str(v) + "\n")
    out_f.close()


def generate_worst_case(test_number, number_of_vertices, number_of_edges):
    out_f = open(input_tests_directory + "worst-case" + str(test_number) + ".txt", "w")
    n, m, edge_list = generator.generate_worst_case(number_of_vertices, number_of_edges)
    out_f.write(str(n) + " " + str(m) + "\n")
    for edge in edge_list:
        u, v = edge
        out_f.write(str(u) + " " + str(v) + "\n")
    out_f.close()


def run_goldberg_process(test_file, n, adjacency, goldberg_algorithm_output):
    ans = goldberg_algorithm(n, adjacency)
    goldberg_algorithm_output[test_file] = ans


def build_outputs():
    tests = [f for f in listdir(input_tests_directory)]
    answer_result_f = open("tests/answer_results.txt", "w")
    runtime_result_f = open("tests/runtime_results.txt", "w")

    goldberg_algorithm_output = multiprocessing.Manager().dict()

    for test_file in tests:
        print(test_file)
        answer_result_f.write(test_file + " ")
        runtime_result_f.write(test_file + " ")
        with open(input_tests_directory + test_file) as f:
            n, m = [int(x) for x in next(f).split()]
            adjacency_graph = [[] for _ in range(n + 1)]
            for line in f:
                u, v = [int(x) for x in line.split()]
                adjacency_graph[u].append(v)
                adjacency_graph[v].append(u)

            print("goldberg is running...")
            start_time = time.time()
            ans_goldberg = -1.0
            goldberg_runtime = -1.0

            p = multiprocessing.Process(target=run_goldberg_process, name="goldberg",
                                        args=(test_file, n, adjacency_graph, goldberg_algorithm_output))
            p.start()
            p.join(40)
            if p.is_alive():
                p.terminate()
                p.join()
            if goldberg_algorithm_output.get(test_file) is not None:
                ans_goldberg = goldberg_algorithm_output.get(test_file)
                goldberg_runtime = time.time() - start_time

            print("charikar is running...")
            start_time = time.time()
            ans_charikar = -1.0
            charikar_runtime = -1.0
            if n <= 5000 and m <= 5000:
                ans_charikar = charikar_lp_algorithm(n, adjacency_graph)
                charikar_runtime = time.time() - start_time

            print("greedy peeling is running...")
            start_time = time.time()
            ans_greedy_peeling = greedy_peeling_algorithm(n, adjacency_graph)
            greedy_peeling_runtime = time.time() - start_time

            print("iterative greedy peeling is running...")
            start_time = time.time()
            ans_iterative = iterative_greedy_peeling(n, adjacency_graph, min(10000000 // m, 30))
            iterative_runtime = time.time() - start_time

            answer_result_f.write(str(ans_goldberg) if ans_goldberg != -1 else "NaN")
            answer_result_f.write(" ")
            answer_result_f.write(str(ans_charikar) if ans_charikar != -1 else "NaN")
            answer_result_f.write(" ")
            answer_result_f.write(str(ans_greedy_peeling) + " ")
            answer_result_f.write(str(ans_iterative) + " ")
            if ans_goldberg != -1:
                answer_result_f.write(str(ans_greedy_peeling / ans_goldberg) + " ")
                answer_result_f.write(str(ans_iterative / ans_goldberg) + " ")
            else:
                answer_result_f.write(str(ans_greedy_peeling / ans_iterative) + " ")
                answer_result_f.write("NaN ")
            answer_result_f.write("\n")

            runtime_result_f.write(str(goldberg_runtime) if goldberg_runtime != -1 else "NaN")
            runtime_result_f.write(" ")
            runtime_result_f.write(str(charikar_runtime) if charikar_runtime != -1 else "NaN")
            runtime_result_f.write(" ")
            runtime_result_f.write(str(greedy_peeling_runtime) + " ")
            runtime_result_f.write(str(iterative_runtime) + " ")
            runtime_result_f.write("\n")

    answer_result_f.close()
    runtime_result_f.close()


def generate_sample_tests():
    test_num = 1
    with open("tests/sparse_sizes") as data_file:
        for line in data_file:
            n, m = [int(x) for x in line.split()]
            generate_sparse(test_num, n, m)
            test_num = test_num + 1

    test_num = 1
    with open("tests/dense_sizes") as data_file:
        for line in data_file:
            n, m = [int(x) for x in line.split()]
            generate_dense(test_num, n, m)
            test_num = test_num + 1

    test_num = 1
    with open("tests/worst_case_sizes") as data_file:
        for line in data_file:
            t, p = [int(x) for x in line.split()]
            generate_worst_case(test_num, t, p)
            test_num = test_num + 1


def generate_greedy_peeling_curve():
    f = open("tests/answer_results.txt", "r")
    x_nan = []
    y_nan = []
    x = []
    y = []
    x_worst = []
    y_worst = []
    for line in f:
        values = line.split()
        test_name = values[0]
        test_file = open("tests/input/" + test_name)
        n, m = [int(x) for x in next(test_file).split()]
        if "worst" in values[0]:
            x_worst.append(m / math.comb(n, 2))
            y_worst.append(float(values[5]))
        elif values[1] == "NaN":
            x_nan.append(m / math.comb(n, 2))
            y_nan.append(float(values[5]))
        else:
            x.append(m / math.comb(n, 2))
            y.append(float(values[5]))

    plt.scatter(x_worst, y_worst, label='worst case')
    plt.scatter(x_nan, y_nan, label='NaN')
    plt.scatter(x, y, label='other')
    plt.legend(loc='lower right')
    plt.show()

    f.close()


def generate_iterative_peeling_curve():
    x = [i for i in range(1, 51)]
    y_TX = []
    y_amazon = []
    y_sparse = []
    y_worst = []
    with open("tests/input/roadNet-TX.txt", "r") as f:
        print("TX...")
        test = open("tests/answer_results.txt", "r")
        given_info = []
        for line in test:
            if line.split()[0] != "roadNet-TX.txt":
                continue
            given_info = line.split()
        test.close()
        ans_goldberg = -1
        if given_info[1] != "NaN":
            ans_goldberg = float(given_info[1])
        n, m = [int(x) for x in next(f).split()]
        adjacency_graph = [[] for _ in range(n + 1)]
        for line in f:
            u, v = [int(x) for x in line.split()]
            adjacency_graph[u].append(v)
            adjacency_graph[v].append(u)
        for x_value in x:
            print(x_value)
            ans = iterative_greedy_peeling(n, adjacency_graph, x_value)
            y_TX.append(ans)
        if ans_goldberg == -1:
            ans_goldberg = y_TX[len(y_TX) - 1]
        for i in range(0, len(y_TX)):
            y_TX[i] = y_TX[i] / ans_goldberg

    with open("tests/input/com-amazon.ungraph.txt", "r") as f:
        print("amazon...")
        test = open("tests/answer_results.txt", "r")
        given_info = []
        for line in test:
            if line.split()[0] != "com-amazon.ungraph.txt":
                continue
            given_info = line.split()
        test.close()
        ans_goldberg = -1
        if given_info[1] != "NaN":
            ans_goldberg = float(given_info[1])
        n, m = [int(x) for x in next(f).split()]
        adjacency_graph = [[] for _ in range(n + 1)]
        for line in f:
            u, v = [int(x) for x in line.split()]
            adjacency_graph[u].append(v)
            adjacency_graph[v].append(u)
        for x_value in x:
            print(x_value)
            ans = iterative_greedy_peeling(n, adjacency_graph, x_value)
            y_amazon.append(ans)
        if ans_goldberg == -1:
            ans_goldberg = y_amazon[len(y_amazon) - 1]
        for i in range(0, len(y_amazon)):
            y_amazon[i] = y_amazon[i] / ans_goldberg

    with open("tests/input/sparse17.txt", "r") as f:
        print("sparse...")
        test = open("tests/answer_results.txt", "r")
        given_info = []
        for line in test:
            if line.split()[0] != "sparse17.txt":
                continue
            given_info = line.split()
        test.close()
        ans_goldberg = -1
        if given_info[1] != "NaN":
            ans_goldberg = float(given_info[1])
        n, m = [int(x) for x in next(f).split()]
        adjacency_graph = [[] for _ in range(n + 1)]
        for line in f:
            u, v = [int(x) for x in line.split()]
            adjacency_graph[u].append(v)
            adjacency_graph[v].append(u)
        for x_value in x:
            print(x_value)
            ans = iterative_greedy_peeling(n, adjacency_graph, x_value)
            y_sparse.append(ans)
        if ans_goldberg == -1:
            ans_goldberg = y_sparse[len(y_sparse) - 1]
        for i in range(0, len(y_sparse)):
            y_sparse[i] = y_sparse[i] / ans_goldberg

    with open("tests/input/worst-case10.txt", "r") as f:
        print("worst...")
        test = open("tests/answer_results.txt", "r")
        given_info = []
        for line in test:
            if line.split()[0] != "worst-case10.txt":
                continue
            given_info = line.split()
        test.close()
        ans_goldberg = -1
        if given_info[1] != "NaN":
            ans_goldberg = float(given_info[1])
        n, m = [int(x) for x in next(f).split()]
        adjacency_graph = [[] for _ in range(n + 1)]
        for line in f:
            u, v = [int(x) for x in line.split()]
            adjacency_graph[u].append(v)
            adjacency_graph[v].append(u)
        for x_value in x:
            print(x_value)
            ans = iterative_greedy_peeling(n, adjacency_graph, x_value)
            y_worst.append(ans)
        if ans_goldberg == -1:
            ans_goldberg = y_worst[len(y_worst) - 1]
        for i in range(0, len(y_worst)):
            y_worst[i] = y_worst[i] / ans_goldberg

    plt.plot(x, y_TX, label='roadNet-TX')
    plt.plot(x, y_amazon, label='com-amazon.ungraph')
    plt.plot(x, y_sparse, label='sparse17')
    plt.plot(x, y_sparse, label='worst10')
    plt.xticks(x, x)
    plt.legend(loc='lower right')
    plt.show()


if __name__ == '__main__':
    generate_iterative_peeling_curve()
