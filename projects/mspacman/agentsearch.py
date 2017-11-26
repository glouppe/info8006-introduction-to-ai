from pacman import Directions
from game import Agent
# XXX: You should complete this class for Step 1


class Agentsearch(Agent):
    def __init__(self, index=0, time_eater=40):
        """
        Arguments:
        ----------
        - `index`: index of your agent. Leave it to 0, it has been put
                   only for game engine compliancy
        - `time_eater`: Amount of time pac man remains in `eater`
                        state when eating a big food dot
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
