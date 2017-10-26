import numpy as np
# XXX: Do no use anything else that Numpy and/or the standard Python library.

class Agent:
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

	def move(grid):
        """
        Parameters:
        -----------
        - `grid`: a 2D Numpy array of integers, where grid[i,j] is
            - 0 if the cell is empty
            - 1 if the cell contains 'X'
            - 2 if the cell contains 'O'

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
        return x, y

    # XXX you are free to add other methods, if necessary to implement `move`.
