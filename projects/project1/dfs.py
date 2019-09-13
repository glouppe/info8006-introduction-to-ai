import random
import numpy as np

from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.graphicsUtils import keys_waiting, keys_pressed


class PacmanAgent(Agent):
    """
    An agent following DFS strategy in search game.
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

    def dfs(self, state):
        """
        Given a pacman game state,
        returns a list of legal moves to solve the search layout.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A legal path as a list of moves defined in `game.Directions`.
        """

        current = state
        key = tuple([state.getPacmanPosition()] + state.getFood().asList())
        self.paths[key] = []
        self.visited[key] = [key]

        while not current.isWin():
            legal_actions = current.getLegalActions()
            for action in legal_actions:
                # Retrive info of successor
                next_state = current.generatePacmanSuccessor(action)
                pacman_pos = next_state.getPacmanPosition()
                food_pos = next_state.getFood().asList()
                next_state_key = tuple(pacman_pos + food_pos)
                if next_state_key not in self.visited[key]:
                    # Add successor to the fringe if not visited yet
                    self.fringe.append(next_state)
                    # Add path information
                    self.paths[next_state_key] = self.paths[key].copy()
                    self.paths[next_state_key].append(action)
                    # Add visited states information
                    self.visited[next_state_key] = self.visited[key].copy()
                    self.visited[next_state_key].append(next_state_key)

            # Choose new state to expand
            current = self.fringe.pop()
            key = tuple([current.getPacmanPosition()] +
                        current.getFood().asList())

        return self.paths[key]
