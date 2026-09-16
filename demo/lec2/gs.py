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

    # 1 - Retrieves the position of the dots and Pacman.
    food_position = state.getFood()
    pacman_position = state.getPacmanPosition()

    # 2 - We determine the size of the grid in order to later go through it.
    length = 0
    for boolean in food_position:
        length = length + 1

    width = len(food_position[0])

    # 3 - Stores the different Manhattan distances calculated.
    distances = []

    # 4 - Computation of the Manhattan distance.
    i = j = 0

    while i < length:
        while j < width:

            # Calculates the ManhattanDistance only for
            # the cells where we can find a dot on it.
            if food_position[i][j] is True:
                distances.append(manhattanDistance(pacman_position, (i, j)))

            j = j + 1

        i = i + 1
        j = 0

    # 5 - The returned value is the longest distance,
    # i.e the distance to the furthest dot.
    return(max(distances))


def costfunction(state, initial_state, previous_cost):
    
    return 0


class PacmanAgent(Agent):

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """

        # This list will contains all the moves Pacman will execute
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
        - Given a pacman game state, returns a legal move
          which is defined in `game.Directions`.
        """

        # 1 - If Pacman has no move available, we try to find some
        # by using the A star algorithm on the current game state.
        if not self.moves:
            self.moves = self.astar(state)

        # 2 - We try to return an action.
        try:
            return self.moves.pop(0)

        # 3 - No actions are available so we trigger an exception.
        except IndexError:
            return Directions.STOP

    def astar(self, state):
        """
        Given a pacman game state, returns a list of legal moves
        to solve the search layout based on the A* algorithm.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                  `pacman.GameState`.

        Return:
        -------
        - A list of legal moves as defined in `game.Directions`.
        """

        # 1 - Declaration of variables :
        # Remembers the path Pacman took (West, East, North,...).
        path = []

        # Contains the state and the path associated to it.
        fringe = [(state, path)]

        # Contains all the different states that have already been visited.
        closed = set()

        # Contains the cost c = g(n) + h(n) of each next state available.
        # found in the fringe
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

            # 2.3 - Search of the cheapest state.
            elif len(cost_list) != 0:
                if index_min_cost != -1:
                    cost_list.pop(index_min_cost)

                # Retrieves the index of the smallest value in cost_list.
                index_min_cost = cost_list.index(min(cost_list))

                # Update of the state
                current, path = fringe.pop(index_min_cost)

            # Checks if the current state is a winning state.
            if current.isWin():
                return path

            # 2.4 - A "hashkey" representing
            # the current state is created.
            current_key = key(current)

            # 2.5 - Checks if the state has already been visited,
            # if that's not the case, we explore it.
            if current_key not in closed:

                # 2.5.1 - The state is added in the list of
                # already visited states.
                closed.add(current_key)

                # 2.5.2 - Looks through the successors of the current state.
                for next_state, action in current.generatePacmanSuccessors():

                    # Checks if the successor is a winning state.
                    if next_state.isWin():
                        return path + [action]

                    # Computation of the state's path cost.
                    if index_min_cost != -1:
                        cl = cost_list[index_min_cost]
                        cost = costfunction(next_state, current, cl)
                        cost += heuristic(next_state)

                    else:
                        h = -heuristic(current)
                        cost = costfunction(next_state, current, h)
                        cost += heuristic(next_state)

                    # We add it to the list.
                    cost_list.append(cost)

                    # The next state is added to the fringe.
                    fringe.append((next_state, path + [action]))

        return path
