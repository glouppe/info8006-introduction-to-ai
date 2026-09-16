"""Greedy search agent.

Demo of lecture 2, originally written by Victor Mangeleer. Tidied without
changing what the algorithm does, so that the expanded-node counts shown in
class are unchanged: the fringe is ordered by h(n) alone.
"""

from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import manhattanDistance


def key(state):
    """Return a hashable key identifying a game state."""
    return (state.getFood(), state.getPacmanPosition())


def heuristic(state):
    """Return the Manhattan distance from Pacman to the furthest dot."""
    food_position = state.getFood()
    pacman_position = state.getPacmanPosition()

    distances = [
        manhattanDistance(pacman_position, (i, j))
        for i, column in enumerate(food_position)
        for j in range(len(food_position[0]))
        if column[j] is True
    ]

    return max(distances)


def costfunction(state, initial_state, previous_cost):
    """No path cost: greedy search orders the fringe by h(n) alone."""
    return 0


class PacmanAgent(Agent):
    """A Pacman agent based on greedy search."""

    def __init__(self, args):
        self.moves = []

    def get_action(self, state):
        """Return a legal move for `state`, as defined in `game.Directions`."""
        if not self.moves:
            self.moves = self.greedy(state)

        return self.moves.pop(0) if self.moves else Directions.STOP

    def greedy(self, state):
        """Return the moves solving the layout, or an empty list on failure."""
        path = []
        fringe = [(state, path)]
        closed = set()

        # Priority of each node of the fringe, at the same index
        cost_list = []
        index_min_cost = -1

        while fringe:
            if not cost_list:
                current, path = fringe.pop()
            else:
                # The priority of the node expanded last is no longer needed
                if index_min_cost != -1:
                    cost_list.pop(index_min_cost)

                index_min_cost = cost_list.index(min(cost_list))
                current, path = fringe.pop(index_min_cost)

            if current.isWin():
                return path

            current_key = key(current)

            if current_key not in closed:
                closed.add(current_key)

                for next_state, action in current.generatePacmanSuccessors():
                    if next_state.isWin():
                        return path + [action]

                    if index_min_cost != -1:
                        previous = cost_list[index_min_cost]
                    else:
                        previous = -heuristic(current)

                    cost = costfunction(next_state, current, previous)
                    cost += heuristic(next_state)

                    cost_list.append(cost)
                    fringe.append((next_state, path + [action]))

        return []
