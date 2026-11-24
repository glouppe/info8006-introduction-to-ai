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


class EastRandyGhost(GhostAgent):
    """A stochastic ghost which favor EAST direction when legal"""

    def __init__(self, index, p=0.5):
        super().__init__(index)
        self.p = p

    def getDistribution(self, state):
        """
        Returns a distribution such that
        if East is in legal actions, then
        selects it with probability 'p'.
        """

        legal = state.getLegalActions(self.index)
        dist = util.Counter()

        if Directions.EAST in legal:
            for action in legal:
                if action == Directions.EAST:
                    dist[action] = self.p
                else:
                    dist[action] = (1.0 - self.p) / (len(legal) - 1)
        else:
            for action in legal:
                dist[action] = 1.0

        dist.normalize()

        return dist


class DumbyGhost(GhostAgent):
    """A dumb ghost."""

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
    """A greedy ghost."""

    def __init__(self, index, prob_attack=1.0, prob_scaredFlee=1.0):
        super().__init__(index)
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
        bestActions = [[
            action for action,
            distance in zip(
                legalActions,
                distancesToPacman) if distance == bestScore][0]]

        # Construct distribution
        dist = util.Counter()
        for a in bestActions:
            dist[a] = bestProb / len(bestActions)
        for a in legalActions:
            dist[a] += (1 - bestProb) / len(legalActions)
        dist.normalize()

        return dist


class SmartyGhost(GhostAgent):
    """A smart ghost"""

    def __init__(self, index):
        super().__init__(index)
        self.fscore = None
        self.gscore = None
        self.wasScared = False
        self.corners = None
        self.gghost = GreedyGhost(index)

    def _pathsearch(self, state, fscore_in, gscore_in, goal):
        fringe = PriorityQueue()
        closed = np.full(
            (state.data.layout.width,
             state.data.layout.height),
            False)
        initpos = tuple(map(lambda x: int(x),
                            state.getGhostPosition(self.index)))
        if gscore_in is not None:
            gscore = gscore_in
        else:
            gscore = np.full(
                (state.data.layout.width, state.data.layout.height), np.inf)
            gscore[initpos] = 0
        if fscore_in is not None:
            fscore = fscore_in
        else:
            fscore = np.full(
                (state.data.layout.width, state.data.layout.height), np.inf)
            fscore[initpos] = manhattanDistance(goal, initpos)
        fringe.push((state, [], closed), fscore[initpos])
        openset = np.full(
            (state.data.layout.width, state.data.layout.height), False)
        openset[initpos] = True
        while not fringe.isEmpty():
            _, node = fringe.pop()
            curNode, actions, closed = node
            if curNode.getGhostPosition(self.index) == goal:
                return actions[0], fscore, gscore
            closed = np.copy(closed)
            ghostpos = tuple(
                map(lambda x: int(x), curNode.getGhostPosition(self.index)))
            closed[ghostpos] = True
            openset[ghostpos] = False
            succs = [(curNode.generateSuccessor(self.index, action), action)
                     for action in curNode.getLegalActions(self.index)]

            for succNode in succs:
                action = succNode[1]
                succNode = succNode[0]

                succghostpos = tuple(
                    map(lambda x: int(x),
                        succNode.getGhostPosition(self.index)))
                tentative_gscore = gscore[succghostpos] + 1
                tentative_fscore = tentative_gscore + \
                    manhattanDistance(goal, succghostpos)

                if closed[succghostpos]:
                    if tentative_fscore <= fscore[succghostpos]:
                        closed[succghostpos] = False
                    else:
                        continue

                if not openset[succghostpos]:
                    openset[succghostpos] = True
                elif tentative_gscore >= gscore[succghostpos]:
                    continue

                gscore[succghostpos] = tentative_gscore
                fscore[succghostpos] = tentative_fscore
                fringe.push(
                    (succNode,
                     actions + [action],
                        closed),
                    fscore[succghostpos])
        return actions[0], fscore, gscore

    def getDistribution(self, state):
        if self.corners is None:
            self.corners = [
                (1,
                 1),
                (1,
                 state.data.layout.height),
                (state.data.layout.width,
                 1),
                (state.data.layout.width,
                 state.data.layout.height)]
        ghostState = state.getGhostState(self.index)
        isScared = ghostState.scaredTimer > 0
        dist = util.Counter()
        legalActions = state.getLegalActions(self.index)
        for a in legalActions:
            dist[a] = 0
        ghostpos = state.getGhostPosition(self.index)
        goal = state.getPacmanPosition() if not isScared \
            else self.corners[
            np.argmax(list(map(lambda pos:
                               manhattanDistance(pos,
                                                 ghostpos),
                               self.corners)))
        ]
        if not isScared:
            a, self.fscore, self.gscore = self._pathsearch(
                state, self.fscore, self.gscore, goal)
            dist[a] = 1
        else:
            dist = self.gghost.getDistribution(state)

        self.wasScared = isScared
        return dist
