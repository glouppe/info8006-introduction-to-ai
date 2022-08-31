from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import Queue, PriorityQueue, manhattanDistance
import math


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


def heuristic(state):
    pos = state.getPacmanPosition()
    food = state.getFood()

    # Initialize
    x_indices = [pos[0], pos[0]]
    y_indices = [pos[1], pos[1]]

    # Compute the sides of the rectangle
    for x in range(food.width):
        for y in range(food.height):
            if food[x][y]:
                if x < x_indices[0]:
                    x_indices[0] = x
                elif x > x_indices[1]:
                    x_indices[1] = x

                if y < y_indices[0]:
                    y_indices[0] = y
                elif y > y_indices[1]:
                    y_indices[1] = y

    # Compute the number of moves to reach each side individually
    left_distance = pos[0] - x_indices[0]
    right_distance = x_indices[1] - pos[0]
    down_distance = pos[1] - y_indices[0]
    up_distance = y_indices[1] - pos[1]

    heuristic = 0.

    if left_distance <= right_distance:
        heuristic += 2*left_distance + right_distance
    else:
        heuristic += left_distance + 2*right_distance

    if down_distance <= up_distance:
        heuristic += 2*down_distance + up_distance
    else:
        heuristic += 2*up_distance + down_distance

    return heuristic


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
            self.moves = self.astar(state)

        try:
            return self.moves.pop(0)

        except IndexError:
            return Directions.STOP

    def astar(self, state):
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
                    fringe.push((next_state, path + [action], next_cost), next_cost + heuristic(next_state))

        return path
