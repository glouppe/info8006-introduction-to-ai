import random
import numpy as np

from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.graphicsUtils import keys_waiting, keys_pressed

from utils import get_state_info

class PacmanAgent(Agent):
    """
    An agent following DFS in search game.
    """

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.moves = []
        self.fringe = []
        self.paths = dict()
        self.visisted_states = dict()

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """

        if not self.moves: self.moves = self.dfs(state)

        return self.moves.pop(0)

    def dfs(self, state):
        """
        Given a pacman game state, returns a list of legal moves to solve the seach layout.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A list of legal moves as defined in `game.Directions`.
        """

        current = state
        key = tuple([state.getPacmanPosition()] + state.getFood().asList())
        self.paths[key] = []
        self.visisted_states[key] = [key]

        while not current.isWin():
            legal_actions = current.getLegalActions()
            for action in legal_actions:
                # Retrive info of successor
                next_state = current.generatePacmanSuccessor(action)
                next_key = tuple([next_state.getPacmanPosition()] + next_state.getFood().asList())
                if next_key not in self.visisted_states[key]:
                    # Add successor to the fringe if not visited yet
                    self.fringe.append(next_state)
                    # Add path information
                    self.paths[next_key] = self.paths[key].copy()
                    self.paths[next_key].append(action)
                    # Add visited states information
                    self.visisted_states[next_key] = self.visisted_states[key].copy()
                    self.visisted_states[next_key].append(next_key)

            # Choose new state to expand
            current = self.fringe.pop()
            key = tuple([current.getPacmanPosition()] + current.getFood().asList())

        return self.paths[key]

