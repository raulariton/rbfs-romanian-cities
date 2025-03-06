from decimal import Decimal
from classes import problem

FAILURE = None

def recursive_best_first_search(problem: problem.Problem):
    rbfs(problem, node = Node(state = problem.initial_state, f_limit = Decimal('inf')))

def rbfs(problem: problem.Problem, node, f_limit: int):

    if node == problem.goal_state:
        # base case, return the goal node
        return node

    successors = expand(node, problem)

    if (len(successors) == 0):
        # if node has no successors
        return (FAILURE, Decimal('inf'))

    for (successor, F_value) in successors:
        # g = cost attribute
        # h = heuristic
        F_value = max(successor.cost + successor.heuristic,
                      node.F_value)

    while True:
        best_successor = successors[0][0]
        best_successor_f_value = successor[0][1]

        if best_successor_f_value > f_limit:
            return (FAILURE, best_successor_f_value)

        # second best
        alternative = successors[1]

        # recursive call
        (result, best_successor_f_value) = rbfs(problem, best_successor,
                                                min(f_limit, alternative[1]))

        if result != FAILURE:
            return (result, f_limit)


# helper method
def expand(node, problem: problem.Problem):

    successors = list()

    for successors in problem.get_successors(node):
        # the F values are calculated in the main function
        # thus here they are initialized as None
        successors.insert((successors, None))

    # sort the list ascendingly (using the second element in each tuple)
    successors.sort(key = lambda successor: successor[1])

    return successors

