"""Depth-first search agent.

Demo of lecture 2, originally written by Victor Mangeleer. Tidied without
changing what the algorithm does, so that the expanded-node counts shown in
class are unchanged.
"""

from pacman_module.game import Agent
from pacman_module.pacman import Directions


def key(state):
    """Return a hashable key identifying a game state."""
    return (state.getFood(), state.getPacmanPosition())


class PacmanAgent(Agent):
    """A Pacman agent based on depth-first search."""

    def __init__(self, args):
        self.moves = []

    def get_action(self, state):
        """Return a legal move for `state`, as defined in `game.Directions`."""
        if not self.moves:
            self.moves = self.dfs(state)

        return self.moves.pop(0) if self.moves else Directions.STOP

    def dfs(self, state):
        """Return the moves solving the layout, or an empty list on failure.

        The fringe is a LIFO stack, so the deepest node is expanded first.
        """
        path = []
        fringe = [(state, path)]
        closed = set()

        while fringe:
            current, path = fringe.pop()

            if current.isWin():
                return path

            current_key = key(current)

            if current_key not in closed:
                closed.add(current_key)

                for next_state, action in current.generatePacmanSuccessors():
                    fringe.append((next_state, path + [action]))

        return []
