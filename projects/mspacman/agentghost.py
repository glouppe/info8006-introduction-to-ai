from pacman import Directions
from game import Agent
# XXX: You should complete this class for Step 2


class Agentghost(Agent):
    def __init__(self, index=0):
        """
        Arguments:
        ----------
        - `index`: index of your agent. Leave it to 0, it has been put
                   only for game engine compliancy
        """
        pass

    def getAction(self, state):
        """
        Parameters:
        -----------
        - `state`: the game engine in a given state
                         (see pacman.py)

        Return:
        -------
        - A legal move defined in Directions module.
        """
        return Directions.STOP
