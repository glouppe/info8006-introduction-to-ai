"""
-----------------------------------------------------------
Introduction to artificial intelligence - Course's Examples
-----------------------------------------------------------
@ Victor Mangeleer - S181670

"""

from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import manhattanDistance


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

    return (state.getFood(), state.getPacmanPosition())


def heuristic(state):
    """
    Fonction used to get the heuristic value of a given state
    by using the Manhattan distance.

    Arguments:
    ----------
    - 'state' : the current game state. See FAQ and class
                `pacman.GameState`.

    Return:
    -------
    - Returns the distance from Pacman to the furthest dot using
      the Manhattan distance.
    """

    """
    Note : The BFS algorithm is a particular form of the A* algorithm where
    the heuristic has to be set to 0 (We do not need it).
    """
    return 0


def costfunction(path):
    """
    Fonction used to compute the cost associated to a state.

    Arguments:
    ----------
    - 'path' : corresponds to the list of positions
               Pacman went through.
    Return:
    -------
    - Returns the cost of a potential state, i.e Pacman's cost to
      transition from one state to the one given in argument.
    """
    return len(path)


class PacmanAgent(Agent):

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """

        # This list will contains all the moves Pacman will execute.
        self.moves = []

    def get_action(self, state):
        """
        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - Given a pacman game state, returns a legal move
          which is defined in `game.Directions`.
        """

        # 1 - If Pacman has no move available, we try to find some
        # by using the A* algorithm on the current game state.
        if not self.moves:
            self.moves = self.bfs(state)

        # 2 - We try to return an action.
        try:
            return self.moves.pop(0)

        # 3 - No actions are available so we trigger an exception.
        except IndexError:
            return Directions.STOP

    def bfs(self, state):
        """
        Given a pacman game state, returns a list of legal moves
        to solve the search layout based on the bfs algorithm.

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

        # Contains the state and to the path tassociated to it.
        fringe = [(state, path)]

        # Contains all the different states that have already been visited.
        closed = set()

        # Contains the cost c = g(n) + h(n) of each next state available
        # fin the fringe.
        cost_list = []

        # Contains the index of the lowest path cost (Initially set to -1).
        index_min_cost = -1

        # 2 - Search of a solution.
        while True:

            # 2.1 - If there are no nodes left, exits.
            if len(fringe) == 0:
                return []  # failure

            # 2.2 - Checks if the current state is the initial one.
            if len(cost_list) == 0:

                current, path = fringe.pop()

                # This variable will be later used to store
                # the total cost of a path by adding the
                # value calculated by the cost function
                # at each state.

            # 2.3 - Search of the cheapest state.
            elif len(cost_list) != 0:

                # Removes the cost of the past state since
                # we already used it.
                if index_min_cost != -1:
                    cost_list.pop(index_min_cost)

                # Retrieves the index of the smallest value in cost_list.
                index_min_cost = cost_list.index(min(cost_list))

                # Update of the state.
                current, path = fringe.pop(index_min_cost)

            # 2.4 - Checks if the current state is a winning state.
            if current.isWin():
                return path

            # 2.5 - A "hashkey" representing
            # the current state is created.
            current_key = key(current)

            # 2.6 - Checks if the state has already been visited,
            # if that's not the case, we explore it.
            if current_key not in closed:

                # 2.6.1 - The state is added in the list
                # of already visited states.
                closed.add(current_key)

                # 2.6.2 - Looks through the successors of the current state.
                for next_state, action in current.generatePacmanSuccessors():

                    # Checks if the successor is not a winning state.
                    if next_state.isWin():
                        return path + [action]

                    # Computation of the state's path cost.
                    if index_min_cost != -1:
                        cost = costfunction(path + [action])
                        cost += heuristic(next_state)

                    else:
                        cost = costfunction(path + [action])
                        cost += heuristic(next_state)

                    # We add it to the list.
                    cost_list.append(cost)

                    # The next state is added to the fringe.
                    fringe.append((next_state, path + [action]))

        return path
