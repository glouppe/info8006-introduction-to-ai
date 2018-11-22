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
        """
           Dictionary of legal actions per (x,y,dir) keys
           where x and y are respectively the horizontal
           and the vertical location of the ghost,
           and dir is the orientation of the ghost
           (Necessary because Ghosts cannot make half-turn).
        """
        self.legalActionsPerGhostPosition = None

    def updateAndGetBeliefStates(self, evidences):
        """
        Given a list of (noised) distances from pacman to ghosts,
        returns a list of belief states about ghosts positions

        Arguments:
        ----------
        - `evidences`: list of (noised) ghost positions at state x_{t}
          where 't' is the current time step

        Return:
        -------
        - A list of Z belief states about ghost positions
          as N*M numpy matrices of probabilities
          where N and M are respectively width and height
          of the maze layout and Z is the number of ghosts.

        N.B. : [1,1] is the bottom left corner of the maze
        """

        beliefStates = self.beliefGhostStates
        # Random normalized probabilities
        # XXX: Modify this part *only*
        for z in range(len(beliefStates)):
            for i in range(beliefStates[z].shape[0]):
                for j in range(beliefStates[z].shape[1]):
                    beliefStates[z][i][j] = np.random.random()
            beliefStates[z] /= np.sum(beliefStates[z])
        # End of modifications
        self.beliefGhostStates = beliefStates
        return beliefStates

    def _computeNoisyPositions(self, state):
        """
            Compute a noisy position from true ghosts positions.
            XXX: DO NOT MODIFY THAT FUNCTION !!!
            Doing so will result in a 0 grade.
        """
        positions = state.getGhostPositions()
        w = self.args.w

        div = float(w * w)
        new_positions = []
        for p in positions:
            (x, y) = p
            dist = util.Counter()
            for i in range(x - w, x + w):
                for j in range(y - w, y + w):
                    dist[(i, j)] = 1.0 / (w * w)
            dist.normalize()
            new_positions.append(util.chooseFromDistribution(dist))
        return new_positions

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
        if self.legalActionsPerGhostPosition is None:
            self.legalActionsPerGhostPosition = dict()
            for i in range(self.beliefGhostStates[0].shape[0]):
                for j in range(self.beliefGhostStates[0].shape[1]):
                    for d in [
                            Directions.NORTH,
                            Directions.SOUTH,
                            Directions.WEST,
                            Directions.EAST]:
                        self.legalActionsPerGhostPosition[(i, j, d)] = \
                            GhostRules.getLegalActionsAtPositionAndDirection(
                            state, 1, (i, j), d)\
                            if not state.hasWall(i, j) else []
        return self.updateAndGetBeliefStates(
            self._computeNoisyPositions(state))
