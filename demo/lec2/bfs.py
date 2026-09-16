"""Breadth-first search agent.

Demo of lecture 2, originally written by Victor Mangeleer. Tidied without
changing what the algorithm does, so that the expanded-node counts shown in
class are unchanged.

Note: the fringe is ordered by the length of the path, which on this demo
expands the shallowest node first, as breadth-first search does. It is
therefore written here as the uniform-cost search it really is, with the
number of actions as cost.
"""

from pacman_module.game import Agent
from pacman_module.pacman import Directions


def key(state):
    """Return a hashable key identifying a game state."""
    return (state.getFood(), state.getPacmanPosition())


def heuristic(state):
    """No heuristic: the fringe is ordered by the path length alone."""
    return 0


def costfunction(path):
    """Return the number of actions of `path`, i.e. the depth of the node."""
    return len(path)


class PacmanAgent(Agent):
    """A Pacman agent based on breadth-first search."""

    def __init__(self, args):
        self.moves = []

    def get_action(self, state):
        """Return a legal move for `state`, as defined in `game.Directions`."""
        if not self.moves:
            self.moves = self.bfs(state)

        return self.moves.pop(0) if self.moves else Directions.STOP

    def bfs(self, state):
        """Return the moves solving the layout, or an empty list on failure."""
        path = []
        fringe = [(state, path)]
        closed = set()

        # Depth of each node of the fringe, at the same index
        cost_list = []
        index_min_cost = -1

        while fringe:
            if not cost_list:
                current, path = fringe.pop()
            else:
                # The depth of the node expanded last is no longer needed
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

                    cost = costfunction(path + [action])
                    cost += heuristic(next_state)

                    cost_list.append(cost)
                    fringe.append((next_state, path + [action]))

        return []
