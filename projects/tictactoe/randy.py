import numpy as np
# XXX: This class is designed to allow you to test your AI. Don't modify it.


class Randy:
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

        Returns a random valid move
        """
        lst = np.argwhere(game_engine.M == 0)
        return tuple(lst[np.random.randint(lst.shape[0])])
