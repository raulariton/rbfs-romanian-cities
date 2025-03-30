from src.classes.problem import Problem

class Node:
    """This class represents a node in the RBFS tree."""

    def __init__(self, state: str, problem: Problem, predecessor = None, f_limit: float = 0):
        """
        Create a Node object
        :param state: The state (name) of the node
        :param predecessor: The predecessor of the node. None if the node is
        the initial node.
        :param f_limit: The f_limit of the node.
        """
        self.state = state
        self.predecessor = predecessor
        self.problem = problem
        self.f_limit = f_limit
        self.best_successor = None
        self.alternative_successor = None

        self.f_value = None

        # to be computed on demand
        self.cost_from_initial = None

        # to be retrieved by database on demand
        self.heuristic = None

    def __str__(self):
        return f"{self.state}"

    def __repr__(self):
        return f"{self.state}"

    def get_cost(self) -> int:
        """
        Compute the cost of getting to this node, by iterating through the predecessors
        until getting to the initial state (the starting node).
        The cost only gets computed once throughout the lifetime of a ``Node`` object.
        """

        # if cost has already been computed, return it
        if self.cost_from_initial is not None:
            return self.cost_from_initial

        iterator = self
        self.cost_from_initial = 0

        # if the node is the initial node, then cost is 0
        while iterator.predecessor is not None:
            self.cost_from_initial = (self.cost_from_initial +
                                      self.problem.get_weight(iterator.state,
                                                                iterator.predecessor.state))
            iterator = iterator.predecessor

        return self.cost_from_initial

    def get_heuristic(self) -> int:
        """
        Retrieve the heuristic of the node from the database.
        The heuristic only gets retrieved once throughout the lifetime of a ``Node`` object.
        """

        if self.heuristic is not None:
            return self.heuristic

        self.heuristic = self.problem.get_heuristic(self.state)

        return self.heuristic