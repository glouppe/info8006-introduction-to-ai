from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import Queue, PriorityQueue


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
    return (state.getPacmanPosition(), state.getFood(), tuple(state.getCapsules()))

def step_cost(prev_state, next_state):

    # Eat a capsule
    if len(prev_state.getCapsules()) - len(next_state.getCapsules()) > 0:
        return 6

    # Eat nothing
    else:
        return 1



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
            self.moves = self.ucs(state)

        try:
            return self.moves.pop(0)

        except IndexError:
            return Directions.STOP

    def ucs(self, state):
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
        path = []
        fringe = PriorityQueue()
        fringe.push((state, path, 0.), 0.)
        closed = set()

        while True:
            if fringe.isEmpty():
                return []  # failure

            _, (current, path, cost) = fringe.pop()

            if current.isWin():
                return path

            current_key = key(current)

            if current_key not in closed:
                closed.add(current_key)

                for next_state, action in current.generatePacmanSuccessors():
                    next_cost = cost + step_cost(current, next_state)
                    fringe.push((next_state, path + [action], next_cost), next_cost)

        return path
