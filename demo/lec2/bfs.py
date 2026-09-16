"""Breadth-first search agent.

The fringe is ordered by the length of the path, which on this demo expands
the shallowest node first, as breadth-first search does. It is therefore
written here as the uniform-cost search it really is, with the number of
actions as cost.

Demo of lecture 2. The search itself is in `search.py`.
"""

from search import SearchAgent


class PacmanAgent(SearchAgent):
    """A Pacman agent based on breadth-first search."""

    def cost(self, next_state, current, previous, path):
        """Return the number of actions of `path`, i.e. the depth of the node."""
        return len(path)
