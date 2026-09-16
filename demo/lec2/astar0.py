"""A* agent, with the Euclidean distance as heuristic.

The fringe is ordered by ${f(n) = g(n) + h(n)}$.

Demo of lecture 2. The search itself is in `search.py`.
"""

from search import SearchAgent, euclidian, furthest_dot


class PacmanAgent(SearchAgent):
    """A Pacman agent based on A* with the Euclidean distance."""

    @staticmethod
    def heuristic(state):
        """Return the Euclidean distance from Pacman to the furthest dot."""
        return furthest_dot(state, euclidian)
