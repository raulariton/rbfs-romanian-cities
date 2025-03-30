import gc
import sys
from enum import Enum
from typing import Tuple, Dict, List
from src.classes.node import Node

class Color(Enum):
    DARK_GREEN = '#194D33'
    GREEN = '#5E9325'
    ORANGE = '#C95603'
    GRAY = '#70716F'
    BLUE = '#03A9F4'
MAX_NODES_IN_MEMORY = 5

class ProblemState:
    def __init__(self):

        self.highlighted: Dict[Tuple[str] | Tuple[str, str], Color] = dict()

        self.displayed_message = None
        self.in_memory_nodes: List[List[Node, str | None]] = []

        self.current_path: List[Node] = []

    def set_node_expanded(self, node):

        # delete any previous expanded (green) highlights
        self.highlighted = {k: v for k, v in self.highlighted.items() if v != Color.DARK_GREEN}

        # delete any successor (orange) highlights
        self.highlighted = {k: v for k, v in self.highlighted.items() if v != Color.ORANGE}

        # delete any failure (gray) highlights
        self.highlighted = {k: v for k, v in self.highlighted.items() if v != Color.GRAY}

        self.highlighted[(node.state,)] = Color.DARK_GREEN

        # recursively highlight the path from the initial node to the expanded node
        # in green
        iterator = node
        while iterator.predecessor is not None:
            self.highlighted[(iterator.state,)] = Color.DARK_GREEN
            self.highlighted[(iterator.predecessor.state, iterator.state)] = Color.DARK_GREEN
            self.highlighted[(iterator.predecessor.state,)] = Color.DARK_GREEN
            iterator = iterator.predecessor

        self.set_displayed_message(f"Now expanding node \"{node.state}\".")

    def set_node_successor(self, successor, node):
        self.highlighted[(successor.state,)] = Color.ORANGE

        # highlight edge between current node and successor
        self.highlighted[(node.state, successor.state)] = Color.ORANGE

        self.set_displayed_message(f"\"{successor.state}\" is a successor.")

    def set_node_failure_pt_1(self, node):
        # highlight the node in gray
        self.highlighted[(node.state,)] = Color.GRAY

        self.set_displayed_message("The best successor's f-value is greater than the current node's f-limit.")

    def set_node_failure_pt_2(self, node):
        # delete best successor (green) highlights (node and edge)
        self.highlighted = {k: v for k, v in self.highlighted.items() if v != Color.GREEN}

        # delete gray highlights
        self.highlighted = {k: v for k, v in self.highlighted.items() if v != Color.GRAY}

        # delete currently highlighted path (dark green)
        self.highlighted = {k: v for k, v in self.highlighted.items() if v != Color.DARK_GREEN}

        # recursively highlight the path from the initial node to the expanded node
        # in green
        iterator = node.predecessor
        while iterator is not None and iterator.predecessor is not None:
            self.highlighted[(iterator.state,)] = Color.DARK_GREEN
            self.highlighted[(iterator.predecessor.state, iterator.state)] = Color.DARK_GREEN
            self.highlighted[(iterator.predecessor.state,)] = Color.DARK_GREEN
            iterator = iterator.predecessor

        self.set_displayed_message(f"Now expanding node \"{node.predecessor.state}\".")

    def set_node_no_successors(self, node):
        # delete any previous no-successors (gray) highlights
        # NOTE: this may not be necessary ?
        self.highlighted = {k: v for k, v in self.highlighted.items() if v != Color.GRAY}

        self.highlighted[(node.state,)] = Color.GRAY

    def set_node_best_successor(self, best_successor):

        # delete any previous successor (orange) node and edge highlights
        self.highlighted = {k: v for k, v in self.highlighted.items() if v != Color.ORANGE}

        # recursively highlight the path from the initial node to the expanded node
        # in green
        iterator = best_successor.predecessor.predecessor
        while iterator is not None and iterator.predecessor is not None:
            self.highlighted[(iterator.state,)] = Color.DARK_GREEN
            self.highlighted[(iterator.predecessor.state, iterator.state)] = Color.DARK_GREEN
            self.highlighted[(iterator.predecessor.state,)] = Color.DARK_GREEN
            iterator = iterator.predecessor

        self.highlighted[(best_successor.state,)] = Color.GREEN
        self.highlighted[(best_successor.predecessor.state, best_successor.state)] = Color.GREEN

        self.set_displayed_message(f"\"{best_successor.state}\" is the best successor, "
                                   f"with the lowest f-value.")

    def set_node_alternative_successor(self, alternative_successor):

        # delete any previous successor (orange) node and edge highlights
        self.highlighted = {k: v for k, v in self.highlighted.items() if v != Color.ORANGE}

        self.highlighted[(alternative_successor.state,)] = Color.BLUE

        self.set_displayed_message(f"\"{alternative_successor.state}\" is the second-best successor.")

    def set_displayed_message(self, message: str):
        self.displayed_message = message

    def node_added_in_memory(self, node):
        if node in [lst[0] for lst in self.in_memory_nodes]:
            return

        # add additional message if a node object
        # with the same name exists
        message = None
        for lst in self.in_memory_nodes:
            if lst[0].state == node.state:
                # add additional message to node
                # with the same state in memory
                lst[1] = f"\n(successor of \"{lst[0].predecessor}\")"

                # add additional message to the new node
                # that will be added to memory
                message = f"\n(successor of \"{node.predecessor}\")"


        if len(self.in_memory_nodes) == MAX_NODES_IN_MEMORY:
            # prune

            # sort the nodes in memory by their f_values
            self.in_memory_nodes.sort(key=lambda tup: tup[0].f_value, reverse=True)

            # prune (remove) the node with the highest f_value (last node in list),
            # as long as it is not a part of the final path

            for i in range(len(self.in_memory_nodes)):
                # if the node is not highlighted green
                # (i.e. if is not part of the possible optimal/final path)
                if not self.is_part_of_path(self.in_memory_nodes[i][0]):
                    # it can be pruned (removed from list and thus memory)
                    # to allow for `node` to be inserted

                    # debug print
                    print(f"Pruning node \"{self.in_memory_nodes[i][0].state}\" "
                          f"(with {sys.getrefcount(self.in_memory_nodes[i][0])} references).")

                    # remove from list
                    self.in_memory_nodes.pop(i)
                    break

        self.in_memory_nodes.append([node, message])

    def is_part_of_path(self, node):
        """
        Check if the node is part of the possible optimal/final path.

        """
        return ((node.state,) in self.highlighted
                and ((self.highlighted[(node.state,)] == Color.DARK_GREEN)
                        or (self.highlighted[(node.state,)] == Color.GREEN)))

    # # iterate backwards over optimal path and if iterator == node_to_be_checked, return True (part of optimal path)
    # iterator = node
    # while iterator.predecessor is not None:
    #     if iterator == node_to_be_checked:
    #         return True
    #     iterator = iterator.predecessor
