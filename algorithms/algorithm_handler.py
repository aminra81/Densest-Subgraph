import multiprocessing
import time
import math
from algorithms.charikar import charikar_lp_algorithm
from algorithms.goldberg import goldberg_algorithm
from algorithms.peeling_algorithms import greedy_peeling_algorithm, iterative_greedy_peeling


class AlgorithmRunner:
    def __init__(self):
        self.goldberg_algorithm_output = multiprocessing.Manager().dict()

    def run_goldberg_process(self, test_file, n, adjacency):
        ans = goldberg_algorithm(n, adjacency)
        self.goldberg_algorithm_output[test_file] = ans

    def run_algorithms(self, test_file, n, m, adjacency_graph):
        result = {}

        # Goldberg
        start_time = time.time()
        p = multiprocessing.Process(target=self.run_goldberg_process, args=(test_file, n, adjacency_graph))
        p.start()
        p.join(40)
        if p.is_alive():
            p.terminate()
            p.join()
        result['goldberg'] = {
            'answer': self.goldberg_algorithm_output.get(test_file, float('nan')),
            'runtime': time.time() - start_time if not math.isnan(
                self.goldberg_algorithm_output.get(test_file, float('nan'))) else float('nan')
        }

        # Charikar
        start_time = time.time()
        if n <= 5000 and m <= 5000:
            result['charikar'] = {
                'answer': charikar_lp_algorithm(n, adjacency_graph),
                'runtime': time.time() - start_time
            }
        else:
            result['charikar'] = {'answer': float('nan'), 'runtime': float('nan')}

        # Greedy Peeling
        start_time = time.time()
        result['greedy_peeling'] = {
            'answer': greedy_peeling_algorithm(n, adjacency_graph),
            'runtime': time.time() - start_time
        }

        # Iterative Greedy Peeling
        start_time = time.time()
        result['iterative_greedy'] = {
            'answer': iterative_greedy_peeling(n, adjacency_graph, min(10000000 // m, 30)),
            'runtime': time.time() - start_time
        }

        return result
