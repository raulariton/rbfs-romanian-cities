class Node:
    """This class represents a node in the RBFS tree."""

    # TODO: Some fields are not necessary and can be simply obtained with a method call
    #  look into which ones can be removed without affecting the program's running time
    #  i.e. without having to compute the same thing multiple times
    def __init__(self, state: str, predecessor = None, f_limit: float = 0):
        """Creates a Node object."""
        self.state = state
        self.f_limit = f_limit
        self.f_value = None
        self.predecessor: Node = predecessor
        self.cost_from_initial = None
        self.heuristic = None

    def get_cost(self, problem) -> int:
        """
        Computes the cost of getting to this node, by iterating through the predecessors
        until getting to the initial state (the starting node).
        """
        iterator: Node = self
        self.cost_from_initial: int = 0

        while iterator.predecessor is not None:
            self.cost_from_initial = self.cost_from_initial + problem.get_weight(iterator.state, iterator.predecessor.state)
            iterator = iterator.predecessor

        return self.cost_from_initial

    def get_heuristic(self, problem) -> int:
        """
        Computes the heuristic of the node.
        In the Romanian cities problem, this value is equivalent to a straight line from the node
        to the goal state (the end city).
        """

        # calculates the dimension of the straight line
        self.heuristic = problem.get_heuristic(self.state)

        return self.heuristic