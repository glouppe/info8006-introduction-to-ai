# import numpy as np
# from tictactoe import *
# XXX: Do no use anything else that Numpy and/or the standard Python library.


class Agent:
    def __init__(self, player, k, timeout=60):
        """
        Arguments:
        ----------
        - `player`: the symbol of the player played by the agent
                    (either 1 or 2).
        - `k`: the size of an alignment.
        """
        self.player = player
        self.k = k
        self.timeout = timeout

    def move(self, game_engine):
        """
        Parameters:
        -----------
        - `game_engine`: the game engine in a given state
                         (see tictactoe.py)

        Return:
        -------
        - (x, y): the position the agent draws a symbol.

        Note:
        -----
        In case the returned value violates the game constraints (the position
        is out of range or already contains a symbol), the agent will miss its
        turn.
        """
        # XXX your code goes here
        x = 0
        y = 0
        return x, y

    # XXX you are free to add other methods, if necessary to implement `move`.
