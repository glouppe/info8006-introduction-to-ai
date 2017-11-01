import numpy as np
# XXX: This class is designed to allow you to test your AI. Don't modify it.

class Human:
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

        Note:
        -----
        In case the returned value violates the game constraints (the position
        is out of range or already contains a symbol), the agent will miss its
        turn.
        """
        
        while True:
            game_engine.render()
            print "Enter your coordinates (line then column) separated by a space :"
            try:
                a = raw_input()
                (x,y) = tuple(a.split(" "))
                if game_engine.checkAction((self.player,int(x),int(y))):
                    return int(x),int(y)
                else:
                    print "Your coordinates are not valid, please enter your coordinates (line then column) separated by a space :"
            except:
                print "Something went wrong, please enter your coordinates (line then column) separated by a space :"
                
                        

