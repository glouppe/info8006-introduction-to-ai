from pacman import Directions
from game import Agent
import random


class Randy(Agent):
    def __init__(self, index=0):
        pass

    def getAction(self, state):
        # Generate candidate actions
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        return random.choice(legal)
