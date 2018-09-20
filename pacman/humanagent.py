import argparse
from PacmanGym.gym_pacman.envs.game import Agent
from PacmanGym.gym_pacman.envs.pacman import Directions


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
        self.pressedKey = None

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
        """
        Translate the last pressed key to a move among the legal ones

        Parameters:
        -----------
        - `legal`: a list of legal moves in the current game state


        Return:
        -------
        - A legal move as defined in game.Directions.
        """

        move = Directions.STOP
        if self.pressedKey == self.WEST_KEY and Directions.WEST in legal:
            move = Directions.WEST
        elif self.pressedKey == self.EAST_KEY and Directions.EAST in legal:
            move = Directions.EAST
        elif self.pressedKey == self.NORTH_KEY and Directions.NORTH in legal:
            move = Directions.NORTH
        elif self.pressedKey == self.SOUTH_KEY and Directions.SOUTH in legal:
            move = Directions.SOUTH
        elif self.pressedKey == self.lastMove and self.lastMove in legal:
            move = self.lastMove
        self.lastMove = move
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
