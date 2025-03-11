import networkx as nx

MAX_NODES_IN_MEMORY = 5

from classes.node import Node

class Problem:
    def __init__(self, initial_state: str, goal_state: str):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.node_states = None

        # Graph will only store the currently expanded node and its successors
        # If the number of successors is greater than 4,
        # in the expand() method
        self.graph = nx.Graph()

        # Introduce the initial node in the graph
        self.graph.add_node(initial_state, node = Node(initial_state))

    def get_weight(self, node1: str, node2: str) -> int:
        """
        Returns the weight of the edge connecting two nodes.
        """

        return self.get_adjacent_nodes(node1)[self.node_states.index(node2)]

    def get_heuristic(self, node_state: str) -> int:
        """
        Returns the heuristic value of the node.
        """

        # return get_straight_distance(node, self.goal_state)

        match node_state:
            case "A":
                return 12
            case "B":
                return 12
            case "C":
                return 10
            case "D":
                return 7
            case "E":
                return 2
            case "F":
                return 6
            case "G":
                return 0


    def build_test_graph(self):
        self.node_states = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    def get_adjacent_nodes(self, node_state: str) -> list[int]:
        """
        Return the adjacency list (row in adjacency matrix) corresponding to the given node.
        """

        # TODO: The graph will be stored in a database as an adjacency list
        #  and this method will query the database to get the adjacency list of the given node.
        #  the query will query the adjacency matrix based on the problems

        # NOTE: Test graph
        match node_state:
            case "A":
                return [0, 5, 4, 5, 0, 0, 0]
            case "B":
                return [5, 0, 0, 0, 7, 0, 0]
            case "C":
                return [4, 0, 0, 0, 9, 7, 0]
            case "D":
                return [5, 0, 0, 0, 0, 4, 0]
            case "E":
                return [0, 7, 9, 0, 0, 0, 4]
            case "F":
                return [0, 0, 7, 4, 0, 0, 6]
            case "G":
                return [0, 0, 0, 0, 4, 6, 0]