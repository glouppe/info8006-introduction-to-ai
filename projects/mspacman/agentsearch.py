from pacman import Directions
from game import Agent
# XXX: You should complete this class for Step 1


class Agentsearch(Agent):
    def __init__(self, index=0, time_eater=40, g_pattern=-1):
        """
        Arguments:
        ----------
        - `index`: index of your agent. Leave it to 0, it has been put
                   only for game engine compliancy
        - `time_eater`: Amount of time pac man remains in `eater`
                        state when eating a big food dot
        - `g_pattern`: Ghosts' pattern in-game. See agentghost.py.
                       Not useful in this class, value does not matter
        """
        pass

    def getAction(self, state):
        """
        Parameters:
        -----------
        - `state`: the current game state as defined pacman.GameState.
                   (you are free to use the full GameState interface.)

        Return:
        -------
        - A legal move as defined game.Directions.
        """
        return Directions.STOP
