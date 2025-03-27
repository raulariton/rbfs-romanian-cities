from src.algorithms.recursive_best_first_search import recursive_best_first_search
from src.classes.problem import Problem
import src.utils.db_util as db_util
import json

if __name__ == '__main__':

    try:
        problem = Problem("A", "G", "test_graph")
        recursive_best_first_search(problem)
    except Exception as e:
        print(f"Error occurred: {e}")
        print(e.with_traceback())
