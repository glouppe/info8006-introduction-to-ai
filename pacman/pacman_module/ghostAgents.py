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
import random
from .util import manhattanDistance
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


class LeftyGhost(GhostAgent):
    "A ghost that turns left at every opportunity."

    def getDistribution(self, state):
        dist = util.Counter()
        legal = state.getLegalActions(self.index)
        current = state.getGhostState(self.index).configuration.direction
        if current == Directions.STOP:
            current = Directions.NORTH
        left = Directions.LEFT[current]
        if left in legal:
            dist[left] = 1.0
        elif current in legal:
            dist[current] = 1.0
        elif Directions.RIGHT[current] in legal:
            dist[Directions.RIGHT[current]] = 1.0
        elif Directions.LEFT[left] in legal:
            dist[Directions.LEFT[left]] = 1.0
        dist.normalize()
        return dist


class GreedyGhost(GhostAgent):
    "A ghost that prefers to rush Pacman, or flee when scared."

    def __init__(self, index, prob_attack=1.0, prob_scaredFlee=1.0):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee

    def getDistribution(self, state):
        # Read variables from state
        ghostState = state.getGhostState(self.index)
        legalActions = state.getLegalActions(self.index)
        pos = state.getGhostPosition(self.index)
        isScared = ghostState.scaredTimer > 0

        speed = 1
        if isScared:
            speed = 0.5

        actionVectors = [
            Actions.directionToVector(
                a, speed) for a in legalActions]
        newPositions = [(pos[0] + a[0], pos[1] + a[1]) for a in actionVectors]
        pacmanPosition = state.getPacmanPosition()

        # Select best actions given the state
        distancesToPacman = [
            manhattanDistance(
                pos, pacmanPosition) for pos in newPositions]
        if isScared:
            bestScore = max(distancesToPacman)
            bestProb = self.prob_scaredFlee
        else:
            bestScore = min(distancesToPacman)
            bestProb = self.prob_attack
        bestActions = [
            action for action,
            distance in zip(
                legalActions,
                distancesToPacman) if distance == bestScore]

        # Construct distribution
        dist = util.Counter()
        for a in bestActions:
            dist[a] = bestProb / len(bestActions)
        for a in legalActions:
            dist[a] += (1 - bestProb) / len(legalActions)
        dist.normalize()
        return dist


class RandyGhost(GhostAgent):
    """A ghost that is a probabilistic mixture
       of Lefty(25%), Randy(25%) and Greedy(50%)."""

    def __init__(self, index, prob_greedy=0.5, prob_lefty=0.25):
        self.index = index
        self.prob_greedy = prob_greedy
        self.prob_lefty = prob_lefty
        self.leftyghost = LeftyGhost(index)
        self.greedyghost = GreedyGhost(index)

    def getDistribution(self, state):
        dist_randy = util.Counter()
        for a in state.getLegalActions(self.index):
            dist_randy[a] = 1.0
        dist_randy.normalize()
        dist_greedy = self.greedyghost.getDistribution(state)
        dist_greedy.normalize()
        dist_lefty = self.leftyghost.getDistribution(state)
        dist_lefty.normalize()
        dist = np.random.choice([dist_greedy, dist_lefty, dist_randy], p=[
                                self.prob_greedy,
                                self.prob_lefty,
                                1 - (self.prob_greedy + self.prob_lefty)])
        return dist
