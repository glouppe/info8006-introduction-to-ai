"""H-Minimax agent, with the plain evaluation.

    uv run python run.py --agentfile hminimax.py --pdepth 4 --slowmo on

Pacman assumes a ghost that plays against it, and evaluates a cut-off state by
how close it is to a dot. The cutoff depth comes from `--pdepth`.

Demo of lecture 3. The search itself is in `search.py`.
"""

from search import SearchAgent, cutoff_simple, evals_simple


class PacmanAgent(SearchAgent):
    """A Pacman agent based on h-minimax."""

    evaluation = staticmethod(evals_simple)
    cutoff = staticmethod(cutoff_simple)
