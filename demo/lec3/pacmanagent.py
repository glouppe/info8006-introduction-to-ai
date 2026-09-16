"""Empty agent, to be completed when writing a new one."""

from pacman_module.game import Agent
from pacman_module.pacman import Directions


class PacmanAgent(Agent):
    """A Pacman agent that does nothing."""

    def __init__(self, args):
        self.args = args

    def get_action(self, state):
        """Return a legal move for `state`, as defined in `game.Directions`."""
        return Directions.STOP
