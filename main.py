import math
from os import listdir

import matplotlib.pyplot as plt

from algorithms.algorithm_handler import AlgorithmRunner
from algorithms.peeling_algorithms import iterative_greedy_peeling
from generators.generator_handler import TestGenerator


class ResultsBuilder:
    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_directory = output_directory

    def build_outputs(self, algorithm_runner):
        tests = [f for f in listdir(self.input_directory)]
        with open(f"{self.output_directory}/answer_results.txt", "w") as answer_result_f, \
                open(f"{self.output_directory}/runtime_results.txt", "w") as runtime_result_f:

            for test_file in tests:
                print(f"Processing {test_file}")
                with open(f"{self.input_directory}/{test_file}") as f:
                    n, m = map(int, next(f).split())
                    adjacency_graph = [[] for _ in range(n + 1)]
                    for line in f:
                        u, v = map(int, line.split())
                        adjacency_graph[u].append(v)
                        adjacency_graph[v].append(u)

                    results = algorithm_runner.run_algorithms(test_file, n, m, adjacency_graph)

                    ans_goldberg = results['goldberg']['answer']
                    ans_charikar = results['charikar']['answer']
                    ans_greedy_peeling = results['greedy_peeling']['answer']
                    ans_iterative = results['iterative_greedy']['answer']

                    goldberg_runtime = results['goldberg']['runtime']
                    charikar_runtime = results['charikar']['runtime']
                    greedy_peeling_runtime = results['greedy_peeling']['runtime']
                    iterative_runtime = results['iterative_greedy']['runtime']

                    answer_result_f.write(
                        f"{test_file} {ans_goldberg} {ans_charikar} {ans_greedy_peeling} {ans_iterative} ")
                    if not math.isnan(ans_goldberg):
                        answer_result_f.write(f"{ans_greedy_peeling / ans_goldberg} {ans_iterative / ans_goldberg}\n")
                    else:
                        answer_result_f.write(f"{ans_greedy_peeling / ans_iterative} NaN\n")

                    runtime_result_f.write(
                        f"{test_file} {goldberg_runtime} {charikar_runtime} "
                        f"{greedy_peeling_runtime} {iterative_runtime}\n")


class CurveGenerator:
    def __init__(self, input_directory, output_file):
        self.input_directory = input_directory
        self.output_file = output_file

    def _parse_test_file(self, test_file):
        with open(f"{self.input_directory}/{test_file}") as f:
            n, m = map(int, next(f).split())
            adjacency_graph = [[] for _ in range(n + 1)]
            for line in f:
                u, v = map(int, line.split())
                adjacency_graph[u].append(v)
                adjacency_graph[v].append(u)
        return n, m, adjacency_graph

    def generate_greedy_peeling_curve(self):
        with open(self.output_file, "r") as f:
            x_nan, y_nan, x, y, x_worst, y_worst = [], [], [], [], [], []
            for line in f:
                values = line.split()
                test_name = values[0]
                n, m, _ = self._parse_test_file(test_name)
                density = m / math.comb(n, 2)
                if "worst" in values[0]:
                    x_worst.append(density)
                    y_worst.append(float(values[5]))
                elif values[1] == "NaN":
                    x_nan.append(density)
                    y_nan.append(float(values[5]))
                else:
                    x.append(density)
                    y.append(float(values[5]))

        plt.scatter(x_worst, y_worst, label='worst case')
        plt.scatter(x_nan, y_nan, label='NaN')
        plt.scatter(x, y, label='other')
        plt.legend(loc='lower right')
        plt.show()

    def generate_iterative_peeling_curve(self):
        x = list(range(1, 51))
        curves = {
            'roadNet-TX': [],
            'com-amazon.ungraph': [],
            'sparse17': [],
            'worst-case10': []
        }

        def process_file(test_file, label):
            print(f"Processing {label}...")
            n, m, adjacency_graph = self._parse_test_file(test_file)
            y = []
            for x_value in x:
                print(x_value)
                ans = iterative_greedy_peeling(n, adjacency_graph, x_value)
                y.append(ans)
            return y

        for label, test_file in curves.keys():
            y = process_file(f"{self.input_directory}/{test_file}.txt", label)
            goldberg_answer = float('nan')
            with open(self.output_file, "r") as f:
                for line in f:
                    if line.split()[0] == f"{test_file}.txt":
                        values = line.split()
                        if values[1] != "NaN":
                            goldberg_answer = float(values[1])
                        break
            if math.isnan(goldberg_answer):
                goldberg_answer = y[-1]
            y = [val / goldberg_answer for val in y]
            curves[label] = y

        for label, y_values in curves.items():
            plt.plot(x, y_values, label=label)
        plt.xticks(x, x)
        plt.legend(loc='lower right')
        plt.show()


def main():
    input_tests_directory = "tests/input"
    output_tests_directory = "tests"
    generator = TestGenerator(input_tests_directory)

    generator.generate_from_sizes_file("sparse_sizes", generator.generate_sparse)
    generator.generate_from_sizes_file("dense_sizes", generator.generate_dense)
    generator.generate_from_sizes_file("worst_case_sizes", generator.generate_worst_case)

    runner = AlgorithmRunner()
    builder = ResultsBuilder(input_tests_directory, output_tests_directory)
    builder.build_outputs(runner)
    """curve_gen = CurveGenerator(input_tests_directory, f"{output_tests_directory}/answer_results.txt")
    curve_gen.generate_iterative_peeling_curve()"""


if __name__ == '__main__':
    main()
