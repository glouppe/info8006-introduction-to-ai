"""
Author : one of the TAs, just after
submitting an important journal manuscript.

I am so tired that I might have screwed up the following DFS implementation.

My fellow TAs are expected to fix all the errors
while I'm taking a very long nap.

I trust them but you should also, student,
check the following code against a possible *unique* error.

"""

from pacman_module.game import Agent
from pacman_module.pacman import Directions


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

        try:
            return self.moves.pop(0)
        except IndexError:
            return Directions.STOP

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
        returns a list of legal moves to solve the search layout.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A list of legal moves as defined in `game.Directions`.
        """

        current = state
        key = self.stateKey(state)
        path = []
        len_path = 0
        # Item in the fringe is composed
        # of a state and a sequence of actions
        fringe = [(state, [])]
        # No need to revisit the initial state later
        visited = {key}
        current = state
        while not current.isWin():
            # Expand the current node
            for next_state, action in current.generatePacmanSuccessors():
                next_key = self.stateKey(next_state)
                if next_key not in visited:
                    # Add successor to the fringe if not visited yet
                    fringe.append((next_state, path+[action]))
                    visited.add(next_key)

            # Choose new node to expand if any - quit otherwise
            try:
                current, path = fringe.pop()
                key = self.stateKey(current)
            except BaseException:
                key = self.stateKey(current)
                break

        return path
