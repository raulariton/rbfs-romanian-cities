from classes import problem, node
from classes.node import Node

# NOTE: Only 5 nodes are allowed to be in the graph at all times. Any additional nodes will be loaded from
#  something like a database

FAILURE = None
INFINITY = float('inf')

def recursive_best_first_search(problem: problem.Problem) -> Node:
    initial_node = Node(state=problem.initial_state, f_limit=INFINITY)
    initial_node.f_value = initial_node.get_heuristic(problem)
    return rbfs(problem,
                initial_node)

def rbfs(problem: problem.Problem, node: Node) -> (Node, int):
    # Base case: is the given node the goal state?
    if node.state == problem.goal_state:
        print(f"{node.state} ")
        return (node, 0)

    # Expand the node and get its successors
    successors = expand(node, problem)

    # If there are no successors, return FAILURE
    if (len(successors) == 0):
        return (FAILURE, INFINITY)

    while True:

        # sort the successors by their f values
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


# helper method
def expand(node: Node, problem: problem.Problem) -> list[Node]:

    # clear all nodes except node in graph
    # why? for the get_weight method to work properly
    node_states_to_remove = [state for state in problem.graph.nodes if state != node.state]

    for node_state in node_states_to_remove:
        problem.graph.remove_node(node_state)

    successors: list[Node] = []

    adjacency_list = problem.get_adjacent_nodes(node.state)

    for i in range(len(adjacency_list)):
        if adjacency_list[i] != 0:
            successor = Node(state = problem.node_states[i], predecessor = node)
            problem.graph.add_node(successor.state, node=successor)
            problem.graph.add_edge(node.state, successor.state, weight=adjacency_list[i])
            successor.f_value = max(successor.get_cost(problem) + successor.get_heuristic(problem),
                                    node.f_value)
            successors.append(successor)


    return successors

    # successors: list[tuple[Node, Union[int, None]]] = []
    #
    # for successor in problem.get_successors(node):
    #     # compute F value for each successor
    #     # and append to list as a tuple
    #     f_value = max(successor.get_cost(problem) + successor.heuristic,
    #                       node.f_limit)
    #     successors.append((successor, f_value))
    #
    # # sort the list in ascending order (using the second element in each tuple)
    # successors.sort(key = lambda get_f_value: successors[1])
    #
    # return successors
