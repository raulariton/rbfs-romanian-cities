from algorithms.recursive_best_first_search import recursive_best_first_search
from classes.problem import Problem

if __name__ == '__main__':
    problem = Problem("A", "G")
    problem.build_test_graph()
    recursive_best_first_search(problem)