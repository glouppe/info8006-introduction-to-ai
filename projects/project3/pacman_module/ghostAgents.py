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
        self.index = index
        self.args = args

    def get_action(self, state):
        dist = self.getDistribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution(dist)

    def getDistribution(self, state):
        """Returns a Counter encoding a distribution
           over actions from the provided state."""
        util.raiseNotDefined()


class ConfusedGhost(GhostAgent):
    """A stochastic ghost which goes anywhere with equal probability."""

    def getDistribution(self, state):
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
        dist = util.Counter()
        legal = state.getLegalActions(self.index)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        pacman_position = state.getPacmanPosition()

        for a in legal:
            mdistance = manhattanDistance(
                state.generateSuccessor(self.index, a).getGhostPosition(self.index),
                pacman_position)
            dist[a] = mdistance
        dist.normalize()

        return dist


class ScaredGhost(GhostAgent):
    """A stochastic ghost which favors actions that makes him move AWAY from
       Pacman."""

    def getDistribution(self, state):
        dist = util.Counter()
        legal = state.getLegalActions(self.index)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        pacman_position = state.getPacmanPosition()

        for a in legal:
            mdistance = manhattanDistance(
                state.generateSuccessor(self.index, a).getGhostPosition(self.index),
                pacman_position)
            dist[a] = mdistance**10
        dist.normalize()

        return dist