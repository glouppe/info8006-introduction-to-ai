# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions
import numpy as np


class BeliefStateAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        
    def updateAndGetBeliefStates(self, sensors, belief_states):
        """
        Given a list of (noised) distances from pacman to ghosts,
        returns a list of belief states about ghosts positions

        Arguments:
        ----------
        - `sensors`: list of manhattan distance from pacman to ghosts

        Return:
        -------
        - A list of belief states about ghost positions
          as N*M numpy matrices of probabilities
          where N and M are respectively width and height
          of the maze layout.
        """

        # XXX: Modify this part *only*
        beliefStates = belief_states
        # Random normalized probabilities
        for z in range(len(beliefStates)):
            for i in range(beliefStates[z].shape[0]):
                for j in range(beliefStates[z].shape[1]):
                    if(beliefStates[z][i][j]) != 0 : beliefStates[z][i][j] = np.random.random()
            beliefStates[z] /= np.sum(beliefStates[z])
        # End of modification



        return beliefStates

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """

        """
           XXX: Do NOT modify that function.
                Doing so will result in a 0 grade.
        """
        return self.updateAndGetBeliefStates(state.getNoisyGhostDistances(), state.getGhostBeliefStates())
