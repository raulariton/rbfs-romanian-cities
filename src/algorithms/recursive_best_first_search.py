from src.classes import problem as prb
from src.classes.node import Node

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
        print(f"{node.state} ")
        return (node, 0)

    # Expand the node and get its successors
    successors = expand(node, problem)

    # If there are no successors, return FAILURE
    if (len(successors) == 0):
        return (FAILURE, INFINITY)

    while True:

        # sort the successors by their f_values
        successors.sort(key=lambda x: x.f_value)

        best_successor = successors[0]

        if best_successor.f_value > node.f_limit:
            return (FAILURE, best_successor.f_value)

        # second best
        alternative = successors[1]

        best_successor.f_limit = min(node.f_limit, alternative.f_value)

        # recursive call
        (result, best_successor.f_value) = rbfs(problem, best_successor)

        if result != FAILURE:
            print(f"{node.state} ")
            return (result, node.f_limit)


def expand(node: Node, problem: prb.Problem) -> list[Node]:
    """
    Get the successors of (i.e. nodes with a direct edge to) the given node.

    :return A list of ``Node`` objects.
    If ``Node`` has a number of successors greater than
    """

    successors: list[Node] = []

    adjacency_list = problem.get_adjacency_list(node.state)

    for i in range(len(adjacency_list)):
        if adjacency_list[i] != 0:
            successor = Node(state=problem.index_of_node_state.inverse[i], problem=problem, predecessor=node)
            problem.insert_node_in_memory(successor)
            successor.f_value = max(successor.get_cost() + successor.get_heuristic(),
                                    node.f_value)
            successors.append(successor)

    return successors
