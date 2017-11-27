import random
from leftyghost import Leftyghost
from greedyghost import Greedyghost
from randyghost import Randyghost
from ghostAgents import GhostAgent


class Rpickyghost(GhostAgent):
    def __init__(self, index, p_greedy=0.33, p_lefty=0.33, p_randy=0.33):
        if index > 1:
            f = open("tempnumghost.tmp")
            a = float(f.read())
        else:
            f = open("tempnumghost.tmp", "w+")
            a = random.random()
            f.write(str(a))
        if a <= p_greedy:
            self.getDistribution = Greedyghost(index).getDistribution
        elif a >= p_greedy and a <= p_greedy + p_lefty:
            self.getDistribution = Leftyghost(index).getDistribution
        else:
            self.getDistribution = Randyghost(index).getDistribution
