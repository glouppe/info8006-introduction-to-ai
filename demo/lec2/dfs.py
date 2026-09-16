"""
-----------------------------------------------------------
Introduction to artificial intelligence - Course's Examples
-----------------------------------------------------------
@ Victor Mangeleer - S181670

"""

from pacman_module.game import Agent
from pacman_module.pacman import Directions

import numpy as np

def key(state):
    """
    Returns a key that uniquely identifies a Pacman game state.

    Arguments:
    ----------
    - `state`: the current game state. See FAQ and class
               `pacman.GameState`.

    Return:
    -------
    - A hashable key object that uniquely identifies a Pacman game state.
    """
    #return (state.getFood(), state.getPacmanPosition(), state.getCapsules())
    return (state.getFood(), state.getPacmanPosition())


class PacmanAgent(Agent):
    """
    A Pacman agent based on Depth-First-Search.
    """

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """

        # Initialy,the possible moves are set to zero
        self.moves = []

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

        # If Pacman has no move available, we try to find him some by using
        # the DFS algorithm on the current game state
        if not self.moves:
            self.moves = self.dfs(state)

        # We try to return an action
        try:
            return self.moves.pop(0)

        # No actions available so we trigger an exception
        except IndexError:
            return Directions.STOP

    def dfs(self, state):
        """
        Given a pacman game state, returns a list of
        legal moves to solve the search layout.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A list of legal moves as defined in `game.Directions`.
        """
        # 1 - Declaration of variables :
        # Remembers the path Pacman took (West, East, North,...)
        path = []

        # Contains the state and to the path tassociated to it
        fringe = [(state, path)]

        # Contains all the different states that have already been visited
        closed = set()

        # 2 - Search of a solution.
        while True:

            # 2.1 - If there are no nodes left, we exit the while
            if len(fringe) == 0:
                return []  # failure

            # 2.2 - Retrieves the current state game
            # and the path Pacman took to reach it
            current, path = fringe.pop()

            # 2.3 - Checks if the current state is a winning state
            if current.isWin():
                return path

            # 2.4 - Creates a key representing the current game state
            current_key = key(current)

            # 2.5 - Checks if the node has already been visited,
            # if that's the case we look for another one
            if current_key not in closed:

                # We add the node to the list of the one we've already visited
                closed.add(current_key)

                # We open the successors node and add them to the fringe
                for next_state, action in current.generatePacmanSuccessors():
                    fringe.append((next_state, path + [action]))

        return path
