from src.algorithms.recursive_best_first_search import recursive_best_first_search
from src.classes.problem import Problem
from src.visualizer import Visualizer

if __name__ == '__main__':

    problem = Problem("Arad", "Bucharest", "romanian_cities_graph")
    visualizer = Visualizer(problem, 'node_canvas.json').start()
