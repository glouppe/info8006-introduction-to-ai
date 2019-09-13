"""
Author : one of the TAs, just after
submitting an important journal manuscript.

I am so tired that I might have screwed up the following DFS implementation.

My fellow TAs are expected to fix all the errors
while I'm taking a very long nap.

I trust them but you should also, student,
check the following code against a possible *unique* error.

"""

import random
import numpy as np

from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.graphicsUtils import keys_waiting, keys_pressed


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
        self.visited = dict()

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

        if not self.moves:
            self.moves = self.dfs(state)

        return self.moves.pop(0)

    def stateKey(self, state):
        """
        Given a pacman game state, returns a list of attributes
        which represents the state.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A list of attributes of the game state space
        """
        return state.getPacmanPosition()

    def dfs(self, state):
        """
        Given a pacman game state,
        returns a list of legal moves to solve the seach layout.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A list of legal moves as defined in `game.Directions`.
        """

        current = state
        key = self.stateKey(current)
        self.paths[key] = []
        self.visited[key] = [key]

        while not current.isWin():
            legal_actions = current.getLegalActions()
            for action in legal_actions:
                # Retrive info of successor
                next_state = current.generatePacmanSuccessor(action)
                next_key = self.stateKey(next_state)
                if next_key not in self.visited[key]:
                    # Add successor to the fringe if not visited yet
                    self.fringe.append(next_state)
                    # Add path information
                    self.paths[next_key] = self.paths[key].copy()
                    self.paths[next_key].append(action)
                    # Add visited states information
                    self.visited[next_key] = self.visited[key].copy()
                    self.visited[next_key].append(next_key)

            # Choose new state to expand
            current = self.fringe.pop()
            key = self.stateKey(current)

        return self.paths[key]
