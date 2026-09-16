"""Greedy search agent.

The fringe is ordered by ${h(n)}$ alone, the Manhattan distance to the
furthest dot: no path cost.

Demo of lecture 2. The search itself is in `search.py`.
"""

from pacman_module.util import manhattanDistance
from search import SearchAgent, furthest_dot


class PacmanAgent(SearchAgent):
    """A Pacman agent based on greedy search."""

    @staticmethod
    def heuristic(state):
        """Return the Manhattan distance from Pacman to the furthest dot."""
        return furthest_dot(state, manhattanDistance)

    def cost(self, next_state, current, previous, path):
        """No path cost: greedy search orders the fringe by h(n) alone."""
        return 0
