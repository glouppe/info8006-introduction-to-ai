# ghostAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects
# were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from .game import Agent
from .game import Actions
from .game import Directions
from .util import manhattanDistance
from .util import PriorityQueue
from . import util
import numpy as np


class GhostAgent(Agent):
    def __init__(self, index, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        - `index` : Strictly positive integer index of the ghost agent.
        """
        if index < 1:
            raise IndexError("Index must be >= 1")
        self.index = index
        self.args = args

    def get_action(self, state):
        """
        Given a ghost game state, returns a legal move

        Arguments:
        ----------
        - `state`: the current game state.
                   See FAQ and class `pacman.GameState`.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """

        dist = self.getDistribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution(dist)

    def getDistribution(self, state):
        """
        Given a ghost game state,
        returns a discrete probability distribution over legal moves

        Arguments:
        ----------
        - `state`: the current game state.
                   See FAQ and class `pacman.GameState`.

        Return:
        -------
        - A `util.Counter` object which represents a discrete
          probability distribution over legal moves.
        """
        util.raiseNotDefined()


class ConfusedGhost(GhostAgent):
    """A stochastic ghost which goes anywhere with equal probability."""

    def getDistribution(self, state):
        """
        Given a ghost game state,
        returns a discrete probability distribution over legal moves

        Arguments:
        ----------
        - `state`: the current game state.
                   See FAQ and class `pacman.GameState`.

        Return:
        -------
        - A `util.Counter` object which represents a discrete
          probability distribution over legal moves.
        """
        dist = util.Counter()
        legal = state.getLegalActions(self.index)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        for a in legal:
            dist[a] = 1.0
        dist.normalize()

        return dist


class AfraidGhost(GhostAgent):
    """A stochastic ghost which favors actions that makes him move away from
       Pacman."""

    def getDistribution(self, state):
        """
        Given a ghost game state,
        returns a discrete probability distribution over legal moves

        Arguments:
        ----------
        - `state`: the current game state.
                   See FAQ and class `pacman.GameState`.

        Return:
        -------
        - A `util.Counter` object which represents a discrete
          probability distribution over legal moves.
        """
        dist = util.Counter()
        legal = state.getLegalActions(self.index)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        pacman_position = state.getPacmanPosition()
        ghost_current_position = state.getGhostPosition(self.index)
        current_distance = manhattanDistance(
            ghost_current_position, pacman_position)
        for a in legal:
            succ_state = state.generateSuccessor(self.index, a)
            ghost_succ_position = succ_state.getGhostPosition(self.index)
            succ_distance = manhattanDistance(
                ghost_succ_position, pacman_position)
            dist[a] = 2 if succ_distance >= current_distance else 1
        dist.normalize()

        return dist


class ScaredGhost(GhostAgent):
    """A stochastic ghost which favors actions that makes him move AWAY from
       Pacman."""

    def getDistribution(self, state):
        """
        Given a ghost game state,
        returns a discrete probability distribution over legal moves

        Arguments:
        ----------
        - `state`: the current game state.
                   See FAQ and class `pacman.GameState`.

        Return:
        -------
        - A `util.Counter` object which represents a discrete
          probability distribution over legal moves.
        """
        dist = util.Counter()
        legal = state.getLegalActions(self.index)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        pacman_position = state.getPacmanPosition()
        ghost_current_position = state.getGhostPosition(self.index)
        current_distance = manhattanDistance(
            ghost_current_position, pacman_position)
        for a in legal:
            succ_state = state.generateSuccessor(self.index, a)
            ghost_succ_position = succ_state.getGhostPosition(self.index)
            succ_distance = manhattanDistance(
                ghost_succ_position, pacman_position)
            dist[a] = 2**3 if succ_distance >= current_distance else 1
        dist.normalize()

        return dist
