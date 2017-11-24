import util
from ghostAgents import GhostAgent


class Randyghost(GhostAgent):

    def getDistribution(self, state):
        dist = util.Counter()
        for a in state.getLegalActions(self.index):
            dist[a] = 1.0
        dist.normalize()
        return dist
