"""A* agent, with the Manhattan distance as heuristic.

The fringe is ordered by ${f(n) = g(n) + h(n)}$.

Demo of lecture 2. The search itself is in `search.py`.
"""

from pacman_module.util import manhattanDistance
from search import SearchAgent, furthest_dot


class PacmanAgent(SearchAgent):
    """A Pacman agent based on A* with the Manhattan distance."""

    @staticmethod
    def heuristic(state):
        """Return the Manhattan distance from Pacman to the furthest dot."""
        return furthest_dot(state, manhattanDistance)
