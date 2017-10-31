import numpy as np
# XXX: This class is designed to allow you to test your AI. Don't modify it.

class Random:
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

    def move(self,game_engine):
        """
        Parameters:
        -----------
        - `game_engine`: the game engine in a given state (see tictactoe.py for class specs)

        Return:
        -------
        - (x, y): the position the agent draws a symbol.

        Returns a random valid move
        """
        lst = np.argwhere(game_engine.M == 0)
        return tuple(lst[np.random.randint(lst.shape[0])])
                
                        
        

