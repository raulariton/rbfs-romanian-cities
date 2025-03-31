from bidict import bidict

from src.classes.problem import Problem
from src.classes.node import Node
from src.classes.edge import Edge
from src.classes.problem_state import ProblemState

# constants
FAILURE = None
INFINITY = float('inf')

# global problem state object
problem_state = ProblemState()

def recursive_best_first_search(problem: Problem) -> Node:
    initial_node = Node(
        state=problem.initial_state,
        problem=problem,
        predecessor=None,
        f_limit=INFINITY)

    initial_node.f_value = initial_node.get_heuristic()

    return rbfs(problem,
                initial_node)

def rbfs(problem: Problem, node: Node) -> (Node, int):
    # base case: is the given node the goal state?
    if node.state == problem.goal_state:

        problem_state.current_path.append(node)
        problem_state.node_added_in_memory(node)
        problem_state.set_node_goal()
        yield problem_state

        return (node, 0)

    # add the node to the current path
    problem_state.current_path.append(node)

    problem_state.set_node_expanded(node)
    yield problem_state
    problem_state.node_added_in_memory(node)
    yield problem_state

    while True:

        print(f"Current path: {problem_state.current_path}")

        if node.state == "Sibiu":
            pass

        (best_successor, alternative) = yield from get_successors(node, problem)

        if best_successor.f_value > node.f_limit:

            problem_state.set_node_failure_pt_1(node)
            yield problem_state
            problem_state.set_displayed_message(f"We set the f-value of \"{node.state}\" to the f-value of "
                                                f"\"{best_successor.state}\".")
            yield problem_state
            problem_state.set_node_failure_pt_2(node)
            yield problem_state

            problem_state.current_path.pop()

            return (FAILURE, best_successor.f_value)

        best_successor.f_limit = min(node.f_limit, alternative.f_value)

        # recursive call
        (result, best_successor.f_value) = yield from rbfs(problem, best_successor)

        if result != FAILURE:
            # not sure about this yield
            # TODO: delete if not needed
            # yield node
            return (result, node.f_limit)


def get_successors(node: Node, problem: Problem) -> (Node, Node):
    """
    Set the best successor and the alternative (second-best) successor of the given node.

    - The best successor is defined as the successor node with the lowest f-value.
    - The alternative successor is the successor node with the second-lowest f-value.

    If the successors are already set, update them to reflect updated f-values.
    This usually happens when the f-value of the node has been updated as a result of backtracking.

    If the successors are not already set, they are obtained using the adjacency list of the node.
    For every successor, it is checked if it is the best or the alternative successor.

    """
    excepted_nodes_and_index = bidict()

    # if the best successor is already set
    # except it from being searched initialized and having its f-value computed again
    # this usually happens when the f-value of the node has been updated as a result of backtracking
    if node.best_successor is not None:
        excepted_nodes_and_index[node.best_successor] = problem.index_by_node_state[node.best_successor.state]
    if node.alternative_successor is not None:
        excepted_nodes_and_index[node.alternative_successor] = problem.index_by_node_state[
            node.alternative_successor.state]

    adjacency_list = problem.get_adjacency_list(node.state)

    for i in range(len(adjacency_list)):
        if adjacency_list[i] != 0:
            if i in excepted_nodes_and_index.values():
                successor = excepted_nodes_and_index.inverse[i]
            else:
                # create a new successor node and compute its f-value
                successor = Node(state=problem.index_by_node_state.inverse[i], problem=problem,
                                   predecessor=node)
                successor.f_value = max(successor.get_cost() + successor.get_heuristic(),
                                        node.f_value)

            # update best and alternative successors
            if node.best_successor is None or successor.f_value < node.best_successor.f_value:
                node.alternative_successor = node.best_successor
                node.best_successor = successor
            elif (node.alternative_successor is None
                    or successor.f_value < node.alternative_successor.f_value) and successor != node.best_successor:
                node.alternative_successor = successor

            # update problem state
            problem_state.set_node_successor(successor, node)
            yield problem_state

    # ensure best_successor != alternative_successor
    if node.best_successor == node.alternative_successor:
        node.alternative_successor = None

    # update problem state
    if node.best_successor is not None:
        problem_state.set_node_best_successor(node.best_successor)
        yield problem_state
        # problem_state.node_added_in_memory(node.best_successor)
        yield problem_state
    if node.alternative_successor is not None:
        problem_state.set_node_alternative_successor(node.alternative_successor)
        yield problem_state
        problem_state.node_added_in_memory(node.alternative_successor)
        yield problem_state

    return (node.best_successor, node.alternative_successor)