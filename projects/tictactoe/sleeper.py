# XXX: This class is designed to allow you to test your AI. Don't modify it.
from time import sleep


class Sleeper:
    def __init__(self, player, k):
        """
        Arguments:
        ----------
        - `player`: the symbol of the player played by the agent
                    (either 'X' or 'O').
        - `k`: the size of an alignment.
        """
        self.player = player
        self.k = k

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
        while True:
            sleep(1)
