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
    def __init__(self, index):
        self.index = index

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


class AfraidGhost(GhostAgent):
    """A stochastic ghost which favors actions that makes it move away from Pacman."""

    def __init__(self, index, fear=1.0):
        super().__init__(index)

        self.fear = fear

    def getDistribution(self, state):
        legal = state.getLegalActions(self.index)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        pacman_position = state.getPacmanPosition()
        ghost_position = state.getGhostPosition(self.index)
        distance = manhattanDistance(ghost_position, pacman_position)

        dist = util.Counter()

        for a in legal:
            succ_position = state.generateSuccessor(self.index, a).getGhostPosition(self.index)
            succ_distance = manhattanDistance(succ_position, pacman_position)

            dist[a] = 2**self.fear if succ_distance >= distance else 1

        dist.normalize()

        return dist


class FearlessGhost(AfraidGhost):
    """A stochastic ghost which does not favor any action."""

    def __init__(self, index):
        super().__init__(index, fear=0.0)


class TerrifiedGhost(AfraidGhost):
    """A stochastic ghost which heavily favors actions that makes it move away from Pacman."""

    def __init__(self, index):
        super().__init__(index, fear=3.0)
