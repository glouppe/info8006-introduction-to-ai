from pacman_module.game import Agent, Directions
from pacman_module.graphicsUtils import keys_waiting, keys_pressed


class PacmanAgent(Agent):
    """Pacman agent controlled by the arrow keys."""

    def __init__(self):
        super().__init__()

        self.last = Directions.STOP
        self.keys = []

    def get_action(self, state):
        """Given a Pacman game state, returns a legal move.

        Arguments:
            state: a game state. See API or class `pacman.GameState`.

        Returns:
            A legal move as defined in `game.Directions`.
        """

        legal = state.getLegalActions()

        for key in keys_waiting() + keys_pressed():
            move = {
                'Up': Directions.NORTH,
                'Down': Directions.SOUTH,
                'Left': Directions.WEST,
                'Right': Directions.EAST,
            }.get(key)

            if move in legal:
                break
        else:
            if self.last in legal:
                move = self.last
            else:
                move = Directions.STOP

        self.last = move

        return move
