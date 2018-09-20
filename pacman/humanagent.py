import argparse
from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.graphicsUtils import keys_waiting, keys_pressed


class PacmanAgent(Agent):
    """
    An agent controlled by the keyboard.
    """
    # NOTE: Arrow keys also work.
    WEST_KEY = 'j'
    EAST_KEY = 'l'
    NORTH_KEY = 'i'
    SOUTH_KEY = 'k'

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace. Built from both main command-line parser
                  and command-line parser built by `arg_parser`
        """
        self.lastMove = Directions.STOP
        self.keys = []

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move. Called on-game.
        !!! Constrained computational time (see `args.timeout` parameter)

        Parameters:
        -----------
        - `state`: the current game state. See class pacman.GameState.

        Return:
        -------
        - A legal move as defined in game.Directions.
        """

        keys = keys_waiting() + keys_pressed()
        if keys != []:
            self.keys = keys

        legal = state.getLegalActions(0)
        move = self._get_move(legal)

        if move == Directions.STOP:
            # Try to move in the same direction as before
            if self.lastMove in legal:
                move = self.lastMove

        if move not in legal:
            move = random.choice(legal)

        self.lastMove = move
        return move

    def _get_move(self, legal):
        move = Directions.STOP
        if ((self.WEST_KEY in self.keys or 'Left' in self.keys)
           and Directions.WEST in legal):
            move = Directions.WEST
        if ((self.EAST_KEY in self.keys or 'Right' in self.keys)
           and Directions.EAST in legal):
            move = Directions.EAST
        if ((self.NORTH_KEY in self.keys or 'Up' in self.keys)
           and Directions.NORTH in legal):
            move = Directions.NORTH
        if ((self.SOUTH_KEY in self.keys or 'Down' in self.keys)
           and Directions.SOUTH in legal):
            move = Directions.SOUTH
        return move

    def register_initial_state(self, state):
        """
        Procedure called before the game
        with the initial game state `state`.
        !!! Not called in the online setting (See instructions).

        Parameters:
        -----------
        - `state`: the current game state. See class pacman.GameState.

        """
        return

    @staticmethod
    def arg_parser(parser):
        """
        Return a command line parser based on the arguments needed both
        from this agent and the command line. See python module `argparse`.
        """
        return parser

    def _on_press(self, key, mod):
        try:
            self.pressedKey = chr(key)
        except Exception:
            pass

    def _on_release(self, key, mod):
        try:
            self.pressedKey = self.lastMove
        except Exception:
            pass
