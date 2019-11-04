# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions, GhostRules
import numpy as np
from pacman_module import util


class BeliefStateAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        """
            Variables to use in 'updateAndFetBeliefStates' method.
            Initialization occurs in 'get_action' method.
        """
        # Current list of belief states over ghost positions
        self.beliefGhostStates = None
        # Grid of walls (assigned with 'state.getWalls()' method)
        self.walls = None
        # Parameter lambda to get the real distance
        self.lmbda = self.args.lmbda
        self.exp_mlmbda = np.exp(-self.lmbda)

    def updateAndGetBeliefStates(self, evidences):
        """
        Given a list of (noised) distances from pacman to ghosts,
        returns a list of belief states about ghosts positions

        Arguments:
        ----------
        - `evidences`: list of distances between
          pacman and ghosts at state x_{t}
          where 't' is the current time step

        Return:
        -------
        - A list of Z belief states at state x_{t} about ghost positions
          as N*M numpy matrices of probabilities
          where N and M are respectively width and height
          of the maze layout and Z is the number of ghosts.

        N.B. : [0,0] is the bottom left corner of the maze
        """

        beliefStates = self.beliefGhostStates
        # XXX: Your code here
        pass
        # XXX: End of your code
        self.beliefGhostStates = beliefStates
        return beliefStates

    def _getEvidence(self, state):
        """
            Computes noisy distances between pacman and ghosts.
            XXX: DO NOT MODIFY THAT FUNCTION !!!
            Doing so will result in a 0 grade.
        """
        positions = state.getGhostPositions()
        pacman_position = state.getPacmanPosition()
        noisy_distances = []
        for p in positions:
            true_distance = util.manhattanDistance(p, pacman_position)
            # Uniformly sample the direction of the perturbation
            sign = np.random.choice([-1, 1])
            # Simulate a probability distribution of parameter lambda
            k = 0
            p = 1
            while p > self.exp_mlmbda:
                u = np.random.random()
                p *= u
                k += 1
            k -= 1
            noisy_distances.append(true_distance + sign * k)
        return noisy_distances

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
           XXX: DO NOT MODIFY THAT FUNCTION !!!
                Doing so will result in a 0 grade.
        """

        # XXX : You shouldn't care on what is going on below.
        # Variables are specified in constructor.
        if self.beliefGhostStates is None:
            self.beliefGhostStates = state.getGhostBeliefStates()
        if self.walls is None:
            self.walls = state.getWalls()
        return self.updateAndGetBeliefStates(
            self._getEvidence(state))
