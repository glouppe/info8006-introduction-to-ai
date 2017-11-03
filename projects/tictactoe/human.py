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

    def move(self, game_engine):
        """
        Parameters:
        -----------
        - `game_engine`: the game engine in a given state
                         (see tictactoe.py)

        Return:
        -------
        - (x, y): the position the agent draws a symbol.

        """

        while True:
            game_engine.render()
            print (
                    "Enter your line, a space, and your column coordinates :")
            try:
                a = raw_input()
                (x, y) = tuple(a.split(" "))
                if game_engine.checkAction((self.player, int(x), int(y))):
                    return int(x), int(y)
                else:
                    print (
                        "Your coordinates are not valid.")
            except Exception as e:
                print (
                    "Something went wrong : " + e)
