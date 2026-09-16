"""Expectimax agent, for the modeling assumptions of lecture 3.

    uv run python run.py --agentfile expectimax.py --pdepth 4 \\
        --ghostagent rightrandy --p 0

Ghost nodes take the average of their children instead of the minimum: this
Pacman assumes a ghost that moves at random, not one that plays against it.
Against `--ghostagent rightrandy --p 0` the assumption holds, against
`--ghostagent cheeky` it does not, which is what the section demonstrates.
Everything else is `hminimax_ADV.py`.

Demo of lecture 3. The search itself is in `search.py`.
"""

from search import SearchAgent, cutoff_advanced, evals_advanced


class PacmanAgent(SearchAgent):
    """A Pacman agent based on expectimax."""

    evaluation = staticmethod(evals_advanced)
    cutoff = staticmethod(cutoff_advanced)

    @staticmethod
    def ghost_value(values):
        """Back up a ghost node: it is assumed to move uniformly at random."""
        return sum(values) / len(values)
