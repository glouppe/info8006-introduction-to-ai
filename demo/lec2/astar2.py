"""A* agent, with the exact maze distance as heuristic.

The fringe is ordered by ${f(n) = g(n) + h(n)}$. The distances come from
`maze.py`, which floods the maze from a position and caches the resulting map,
so that the heuristic is the true remaining cost.

Demo of lecture 2. The search itself is in `search.py`.
"""

from maze import maze_retrieve
from search import SearchAgent, furthest_dot

# Flooded maps, keyed by the position they were computed from
maze_map = {}


class PacmanAgent(SearchAgent):
    """A Pacman agent based on A* with the exact maze distance."""

    @staticmethod
    def heuristic(state):
        """Return the exact maze distance from Pacman to the furthest dot."""
        return furthest_dot(
            state,
            lambda pacman, dot: maze_retrieve(state, pacman, dot, maze_map))
