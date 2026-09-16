"""Uniform-cost search agent.

The fringe is ordered by ${g(n)}$ alone: no heuristic, the step cost of
`search.py`.

Demo of lecture 2. The search itself is in `search.py`.
"""

from search import SearchAgent


class PacmanAgent(SearchAgent):
    """A Pacman agent based on uniform-cost search."""
