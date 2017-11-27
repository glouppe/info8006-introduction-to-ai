import util
from leftyghost import Leftyghost
from greedyghost import Greedyghost
from ghostAgents import GhostAgent
import random


class Randyghost(GhostAgent):

    def __init__(self,index,p_greedy=0.5, p_lefty=0.25):
        self.lst_patterns = []
        self.lst_patterns.append((Greedyghost(index).getDistribution, p_greedy))
        self.lst_patterns.append((Leftyghost(index).getDistribution, p_lefty))
        self.rand_proba = 1-(p_greedy + p_lefty)
        self.index = index

    def getDistribution(self, state):
        dist = util.Counter()
        legalActions = state.getLegalActions(self.index)
        n_legalActions = len(legalActions)
        for a in legalActions:
            dist[a] = 1.0/n_legalActions
        lst_dist = [dist]
        lst_proba = [self.rand_proba]
        for pa,pr in self.lst_patterns:
            lst_dist.append(pa(state))
            lst_proba.append(pr)
        dist = random.choices(lst_dist, lst_proba, k=1)[0]
        return dist
        
