"""Shared machinery of the lecture 3 agents.

The agents of this folder differ in three points only, so everything else
lives here:

- the .bold evaluation of a cut-off state, `evals_simple` or `evals_advanced`;
- when to stop, `cutoff_simple` or `cutoff_advanced`;
- what to do at a ghost node, the minimum (the ghost plays against Pacman) or
  the average (the ghost is assumed to move at random).

`hminimax.py`, `hminimax_ADV.py` and `expectimax.py` each pick one
combination. The cutoff depth comes from `--pdepth` and the slow motion from
`--slowmo`, so one file covers every depth.

Demo of lecture 3, originally written by Victor Mangeleer as forty numbered
files. Refactored without changing what the algorithms do, so that the
expanded-node counts shown in class are unchanged.
"""

import time
from collections import Counter

from numpy import sqrt
from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import manhattanDistance

# Value standing for "no move left here"
UNREACHABLE = 5000


def key(state):
    """Return a hashable key identifying a game state."""
    return (state.getFood(), state.getPacmanPosition(),
            state.getGhostPosition(1), state.getGhostDirection(1))


def euclidian(A, B):
    """Return the euclidean distance between two points."""
    return sqrt((A[0] - B[0]) * (A[0] - B[0]) +
                (A[1] - B[1]) * (A[1] - B[1]))


def player(depth):
    """Return 0 on Pacman's turn, 1 on the ghost's.

    Pacman plays at even depths, the ghost at odd ones.
    """
    return 0 if depth % 2 == 0 else 1


def evals_simple(state, depth, food_dots):
    """Return the score of `state`, minus twice the distance to a dot.

    The closer to a dot, the better.
    """
    p_pos = state.getPacmanPosition()
    distances_food = [euclidian(p_pos, food_pos) for food_pos in food_dots]

    return state.getScore() - 2 * min(distances_food)


def evals_advanced(state, depth, food_dots):
    """Return the same, plus the distance to the ghost.

    The further the ghost, the better, which keeps Pacman out of trouble.
    """
    p_pos = state.getPacmanPosition()
    g_pos = state.getGhostPosition(1)

    distances_food = [euclidian(p_pos, food_pos) for food_pos in food_dots]
    distance_ghost = euclidian(p_pos, g_pos)

    return distance_ghost + state.getScore() - 2 * min(distances_food)


def cutoff_simple(state, depth, max_depth, food_dots):
    """Return whether the search must stop in `state`."""
    return state.isWin() or state.isLose() or depth == max_depth


def cutoff_advanced(state, depth, max_depth, food_dots):
    """Return whether the search must stop in `state`.

    Besides the depth threshold, the search stops on a dot that can be eaten
    safely, and once the ghost is far enough for the value not to change much
    (quiescence).
    """
    if state.isWin() or state.isLose():
        return True

    ghost_pos = state.getGhostPosition(1)
    pacman_pos = state.getPacmanPosition()
    ghost_dist = manhattanDistance(ghost_pos, pacman_pos)

    # Note: the original tests the ghost's position against the dots, not
    # Pacman's. Kept as is, so that the demo behaves as it always has.
    if ghost_pos in food_dots and ghost_dist > 2:
        return True

    if ghost_dist > (6 - depth) and ghost_dist > 1:
        return True

    return depth == max_depth


class SearchAgent(Agent):
    """A Pacman agent searching the game tree up to a cutoff depth.

    Subclasses set `evaluation`, `cutoff` and `ghost_value`.
    """

    evaluation = staticmethod(evals_simple)
    cutoff = staticmethod(cutoff_simple)

    @staticmethod
    def ghost_value(values):
        """Back up a ghost node: it plays against Pacman."""
        return min(values)

    def __init__(self, args):
        self.max_depth = args.pdepth
        self.slowmo = getattr(args, "slowmo", "off") == "on"
        self.moves = []

        # Position of every dot left in the maze, and key of every state
        # played so far, kept between the successive calls of the agent
        self.food_dots = []
        self.closed_states = []

    def get_action(self, state):
        """Return a legal move for `state`, as defined in `game.Directions`."""
        if not self.moves:
            self.moves = self.search(state)

        return self.moves.pop(0) if self.moves else Directions.STOP

    def value(self, node, closed):
        """Return the value of `node`, backed up from the states below it.

        `node` is a (state, depth) pair and `closed` holds the states already
        met on the path to it, which are not expanded again.
        """
        state, depth = node

        newclosed = closed.copy()
        newclosed.append(key(state))

        if self.cutoff(state, depth, self.max_depth, self.food_dots):
            return self.evaluation(state, depth, self.food_dots)

        values = []

        if player(depth) == 0:
            for next_state, action in state.generatePacmanSuccessors():
                if key(next_state) not in newclosed:
                    values.append(self.value([next_state, depth + 1],
                                             newclosed))

            return max(values) if values else UNREACHABLE

        for next_state, action in state.generateGhostSuccessors(1):
            if key(next_state) not in newclosed:
                values.append(self.value([next_state, depth + 1], newclosed))

        return self.ghost_value(values) if values else -UNREACHABLE

    def search(self, state):
        """Return the best move in `state`, as a one-element list."""
        if self.slowmo:
            # Slow motion, so that the game can be commented in class
            time.sleep(1)

        # The dots are listed once, then followed as Pacman eats them
        if not self.food_dots:
            food_position = state.getFood()
            height = len(food_position[0])

            self.food_dots.extend(
                (i, j)
                for i, column in enumerate(food_position)
                for j in range(height)
                if column[j] is True)

        if state.getPacmanPosition() in self.food_dots:
            self.food_dots.pop(
                self.food_dots.index(state.getPacmanPosition()))

        # The current state is played, and belongs to every path below it
        self.closed_states.append(key(state))
        closed = [key(state)]

        value = []
        action_list = []
        state_list = []

        # Every successor, whether already visited or not
        action_list_bis = []
        state_list_bis = []

        for next_state, action in state.generatePacmanSuccessors():
            action_list_bis.append(action)
            state_list_bis.append(next_state)

            if key(next_state) not in closed:
                value.append(self.value([next_state, 1], closed))
                action_list.append(action)
                state_list.append(next_state)

        # Drop the moves that led nowhere, marked with |UNREACHABLE|
        a = len(value) - 1

        while a >= 0:
            if abs(value[a]) == UNREACHABLE:
                value.pop(a)
                action_list.pop(a)

            a = a - 1

        if value:
            index_best_action = value.index(max(value))
            self.closed_states.append(key(state_list[index_best_action]))

            return [action_list[index_best_action]]

        # Every successor has been visited already: go to the least visited
        # one, avoiding those that lose the game.
        all_occurence = Counter(self.closed_states)
        occurence = [all_occurence[key(next_state)]
                     for next_state in state_list_bis]

        c = 0
        for action_bis in action_list_bis:
            if state_list_bis[c].isLose() is True:
                occurence.pop(c)
                state_list_bis.pop(c)
                action_list_bis.pop(c)

            c = c + 1

        index_min = occurence.index(min(occurence))
        self.closed_states.append(key(state_list_bis[index_min]))

        return [action_list_bis[index_min]]
