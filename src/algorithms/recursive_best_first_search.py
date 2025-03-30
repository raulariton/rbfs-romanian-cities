from src.classes import problem as prb
from src.classes.node import Node
from src.classes.edge import Edge

FAILURE = None
INFINITY = float('inf')

def recursive_best_first_search(problem: prb.Problem) -> Node:
    initial_node = Node(state=problem.initial_state,
                        problem=problem,
                        predecessor=None,
                        f_limit=INFINITY)

    # add node to list of nodes in memory
    problem.insert_node_in_memory(initial_node)

    initial_node.f_value = initial_node.get_heuristic()

    return rbfs(problem,
                initial_node)

def rbfs(problem: prb.Problem, node: Node) -> (Node, int):
    # base case: is the given node the goal state?
    if node.state == problem.goal_state:
        yield f"We have reached the goal state \"{node.state}\"."
        yield node
        return (node, 0)

    yield f"Now expanding node \"{node.state}\"."
    # yield the current node
    yield node
    # this should highlight only the path between current node and predecessor node
    # and clear any other highlighted paths

    while True:

        # get the best successor of the current node
        # (the functions sets the best_successor attribute of the node)
        yield from get_best_successor(node, problem)

        # shortcut (for readability)
        best_successor = node.best_successor

        yield f"The best successor is \"{best_successor.state}\"."

        if best_successor.f_value > node.f_limit:
            yield f"The best successor's f-value is greater than the current node's f-limit."
            yield f"This means that we have to backtrack to the parent node (\"{node.predecessor.state}\")."
            yield FAILURE
            return (FAILURE, best_successor.f_value)

        # second best
        alternative = node.alternative_successor

        best_successor.f_limit = min(node.f_limit, alternative.f_value)

        # recursive call
        (result, best_successor.f_value) = yield from rbfs(problem, best_successor)

        if result != FAILURE:
            # not sure about this yield
            # yield node
            return (result, node.f_limit)


def get_best_successor(node: Node, problem: prb.Problem) -> None:
    """
    Search for the best successor and the alternative (second-best) successor of given node and set the
    corresponding attributes.

    The best successor is the one with the lowest f-value.

    The alternative successor is the one with the second-lowest f-value.
    """

    # if the successor attributes are already set, update them to reflect updated f-values
    if node.best_successor is not None and node.alternative_successor is not None:
        if node.best_successor.f_value > node.alternative_successor.f_value:
            node.best_successor, node.alternative_successor = node.alternative_successor, node.best_successor
        return


    adjacency_list = problem.get_adjacency_list(node.state)

    for i in range(len(adjacency_list)):
        if adjacency_list[i] != 0:
            successor = Node(state=problem.index_by_node_state.inverse[i], problem=problem,
                               predecessor=node)
            successor.f_value = max(successor.get_cost() + successor.get_heuristic(),
                                    node.f_value)

            # only keep track (in memory) of the best successor and the alternative successor
            if node.best_successor is None or successor.f_value < node.best_successor.f_value:
                node.alternative_successor = node.best_successor
                node.best_successor = successor
            elif (node.alternative_successor is None
                    or successor.f_value < node.alternative_successor.f_value) and successor != node.best_successor:
                node.alternative_successor = successor

            yield Edge(node, successor)

    # ensure best_successor != alternative_successor
    if node.best_successor == node.alternative_successor:
        node.alternative_successor = None