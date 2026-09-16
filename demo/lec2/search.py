"""Shared machinery of the lecture 2 agents.

All the agents of this folder are the same graph search over the same fringe,
and differ in two points only:

- the .bold heuristic ${h(n)}$ of a state, zero unless the search is informed;
- the .bold cost ${g(n)}$ of reaching it.

The fringe is then ordered by ${g(n) + h(n)}$, which gives breadth-first,
uniform-cost, greedy and A* search in turn. Depth-first is the exception: its
fringe is a LIFO stack, so it has its own class here.

The fringe is scanned linearly for the cheapest node and `cost_list` is kept
in step with it by index, as in the original: the expanded-node counts shown
in class depend on it.

Demo of lecture 2, originally written by Victor Mangeleer. Refactored without
changing what the algorithms do.
"""

from math import sqrt

from pacman_module.game import Agent
from pacman_module.pacman import Directions


def key(state):
    """Return a hashable key identifying a game state."""
    return (state.getFood(), state.getPacmanPosition())


def euclidian(A, B):
    """Return the Euclidean distance between points `A` and `B`."""
    return sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)


def dots(state):
    """Return the position of every dot left in the maze."""
    food_position = state.getFood()

    return [
        (i, j)
        for i, column in enumerate(food_position)
        for j in range(len(food_position[0]))
        if column[j] is True
    ]


def furthest_dot(state, distance):
    """Return the distance from Pacman to the furthest dot."""
    pacman_position = state.getPacmanPosition()

    return max(distance(pacman_position, dot) for dot in dots(state))


class SearchAgent(Agent):
    """Graph search with the fringe ordered by ${g(n) + h(n)}$.

    Subclasses set `heuristic` and, when the cost is not the step cost, `cost`.
    """

    @staticmethod
    def heuristic(state):
        """Return ${h(n)}$. Zero unless the search is informed."""
        return 0

    def cost(self, next_state, current, previous, path):
        """Return ${g(n)}$ of `next_state`, given its parent's ${f(n)}$.

        A dot is cheap (0.1), a capsule expensive (5), an empty cell costs 1.
        The fringe holds ${f = g + h}$, so the parent's ${g}$ is recovered by
        taking its heuristic back out.
        """
        x, y = next_state.getPacmanPosition()
        food_position = current.getFood()
        capsule_position = current.getCapsules()

        g = previous - self.heuristic(current)

        if food_position[x][y] is True:
            return g + 0.1
        elif (x, y) in capsule_position:
            return g + 5
        else:
            return g + 1

    def __init__(self, args):
        self.moves = []

    def get_action(self, state):
        """Return a legal move for `state`, as defined in `game.Directions`."""
        if not self.moves:
            self.moves = self.search(state)

        return self.moves.pop(0) if self.moves else Directions.STOP

    def search(self, state):
        """Return the moves solving the layout, or an empty list on failure."""
        path = []
        fringe = [(state, path)]
        closed = set()

        # f(n) of each node of the fringe, at the same index
        cost_list = []
        index_min_cost = -1

        while fringe:
            if not cost_list:
                current, path = fringe.pop()
            else:
                # The cost of the node expanded last is no longer needed
                if index_min_cost != -1:
                    cost_list.pop(index_min_cost)

                index_min_cost = cost_list.index(min(cost_list))
                current, path = fringe.pop(index_min_cost)

            if current.isWin():
                return path

            current_key = key(current)

            if current_key not in closed:
                closed.add(current_key)

                for next_state, action in current.generatePacmanSuccessors():
                    if next_state.isWin():
                        return path + [action]

                    if index_min_cost != -1:
                        previous = cost_list[index_min_cost]
                    else:
                        previous = -self.heuristic(current)

                    cost = self.cost(next_state, current, previous,
                                     path + [action])
                    cost += self.heuristic(next_state)

                    cost_list.append(cost)
                    fringe.append((next_state, path + [action]))

        return []


class DepthFirstAgent(Agent):
    """Graph search with a LIFO fringe, so the deepest node is expanded first."""

    def __init__(self, args):
        self.moves = []

    def get_action(self, state):
        """Return a legal move for `state`, as defined in `game.Directions`."""
        if not self.moves:
            self.moves = self.search(state)

        return self.moves.pop(0) if self.moves else Directions.STOP

    def search(self, state):
        """Return the moves solving the layout, or an empty list on failure."""
        path = []
        fringe = [(state, path)]
        closed = set()

        while fringe:
            current, path = fringe.pop()

            if current.isWin():
                return path

            current_key = key(current)

            if current_key not in closed:
                closed.add(current_key)

                for next_state, action in current.generatePacmanSuccessors():
                    fringe.append((next_state, path + [action]))

        return []
