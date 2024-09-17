from pacman_module.game import Agent, Directions


class PacmanAgent(Agent):
    """Empty Pacman agent."""

    def __init__(self):
        super().__init__()

    def get_action(self, state):
        """Given a Pacman game state, returns a legal move.

        Arguments:
            state: a game state. See API or class `pacman.GameState`.

        Returns:
            A legal move as defined in `game.Directions`.
        """

        return Directions.STOP
