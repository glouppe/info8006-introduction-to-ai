"""Agent controlled by the keyboard, to play the demo by hand."""

import contextlib
import random

from pacman_module.game import Agent
from pacman_module.graphicsUtils import keys_pressed, keys_waiting
from pacman_module.pacman import Directions


class PacmanAgent(Agent):
    """An agent controlled by the keyboard. Arrow keys also work."""

    WEST_KEY = 'j'
    EAST_KEY = 'l'
    NORTH_KEY = 'i'
    SOUTH_KEY = 'k'

    def __init__(self, args):
        self.lastMove = Directions.STOP
        self.keys = []

    def get_action(self, state):
        """Return the move asked for by the keys, or a legal fallback."""
        keys = keys_waiting() + keys_pressed()
        if keys:
            self.keys = keys

        legal = state.getLegalActions(0)
        move = self._get_move(legal)

        # Without a key, keep going in the same direction if that is legal
        if move == Directions.STOP and self.lastMove in legal:
            move = self.lastMove

        if move not in legal:
            move = random.choice(legal)

        self.lastMove = move

        return move

    def _get_move(self, legal):
        """Return the legal move matching the keys currently held down."""
        move = Directions.STOP

        for keys, direction in [
            ((self.WEST_KEY, 'Left'), Directions.WEST),
            ((self.EAST_KEY, 'Right'), Directions.EAST),
            ((self.NORTH_KEY, 'Up'), Directions.NORTH),
            ((self.SOUTH_KEY, 'Down'), Directions.SOUTH),
        ]:
            if any(k in self.keys for k in keys) and direction in legal:
                move = direction

        return move

    def _on_press(self, key, mod):
        with contextlib.suppress(ValueError, TypeError):
            self.pressedKey = chr(key)

    def _on_release(self, key, mod):
        with contextlib.suppress(AttributeError):
            self.pressedKey = self.lastMove
