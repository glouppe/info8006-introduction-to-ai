"""H-Minimax agent, with an evaluation that keeps out of trouble.

    uv run python run.py --agentfile hminimax_ADV.py --pdepth 4 --slowmo on

Pacman assumes a ghost that plays against it. Compared with `hminimax.py`, the
evaluation also rewards being far from the ghost, and the search stops early
on a dot that can be eaten safely and once the ghost is far away.

Demo of lecture 3. The search itself is in `search.py`.
"""

from search import SearchAgent, cutoff_advanced, evals_advanced


class PacmanAgent(SearchAgent):
    """A Pacman agent based on h-minimax, with a better evaluation."""

    evaluation = staticmethod(evals_advanced)
    cutoff = staticmethod(cutoff_advanced)
