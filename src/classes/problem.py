import src.utils.db_util as db
from bidict import bidict as bidirectional_dict

MAX_NODES_IN_MEMORY = 5

# TODO:
#  Have MAX_NODES_IN_MEMORY as an attribute
#  Have a list of active nodes in memory
#  Everytime a node is added to this list, prune (based on highest f value (?))

class Problem:
    """
    The class Problem contains the information about the problem to be solved,
    as well as methods to access any graph data (e.g. neighbors of a node, heuristic value) that may not be
    available in
    memory.
    """
    def __init__(self, initial_state: str, goal_state: str, graph_name_in_database):
        """
        Initialize a problem object
        :param initial_state: The initial state to start the pathfinding from.
        :param goal_state: The state that is to be reached.
        :param graph_name_in_database: The name of the graph in the SQLite database.
        """

        self.initial_state = initial_state
        self.goal_state = goal_state
        self.graph_name_in_database = graph_name_in_database

        # create a node ordering, based on the given
        # adjacency list in the database
        self.index_of_node_state = bidirectional_dict()
        node_states = db.get_node_list(graph_name_in_database)

        i = 0
        for node_state in node_states:
            self.index_of_node_state[node_state] = i
            i += 1

    def get_weight(self, node1_state: str, node2_state: str) -> int:
        """
        Returns the weight of the edge connecting two nodes.
        """
        node1_adjacency_list = self.get_adjacency_list(node1_state)

        return node1_adjacency_list[self.index_of_node_state[node2_state]]

    def get_heuristic(self, node_state: str) -> int:
        """
        Returns the heuristic value of the node.
        """

        return db.get_heuristic(node_state, self.graph_name_in_database)

    def get_adjacency_list(self, node_state: str) -> list[int]:
        """
        Return the adjacency list (row in adjacency matrix) corresponding to the given node.
        """

        return db.get_adjacency_list(node_state, self.graph_name_in_database)

