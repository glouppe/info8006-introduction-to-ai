import argparse
from PacmanGym.gym_pacman.envs.game import Agent
from PacmanGym.gym_pacman.envs.pacman import Directions
import numpy as np


class PacmanAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace. Built from both main command-line parser
                  and command-line parser built by `arg_parser`
        """
        self.prob_dir = dict()
        WestProb, SouthProb, EastProb, NorthProb = args.dirprob
        self.prob_dir["West"] = WestProb
        self.prob_dir["South"] = SouthProb
        self.prob_dir["North"] = EastProb
        self.prob_dir["East"] = NorthProb

    def getAction(self, state):
        """
        Given a pacman game state, returns a legal move. Called on-game.
        !!! Constrained computational time (see `args.timeout` parameter)

        Parameters:
        -----------
        - `state`: the current game state. See class pacman.GameState.

        Return:
        -------
        - A legal move as defined in game.Directions.
        """
        legals = state.getLegalPacmanActions()
        if Directions.STOP in legals:
            legals.remove(Directions.STOP)
        # Get probability for each legal move
        probs = [self.prob_dir[x] for x in legals]
        probs = [x / sum(probs) for x in probs]
        # Returns a randomly chosen move according to probability distribution
        return np.random.choice(legals, 1, replace=True, p=probs)[0]

    def registerInitialState(self, state):
        """
        Procedure called before the game
        with the initial game state `state`.
        !!! Not called in the online setting (See instructions).

        Parameters:
        -----------
        - `state`: the current game state. See class pacman.GameState.

        """
        return

    def arg_parser(parser):
        """
        Return a command line parser based on the arguments needed both
        from this agent and the command line. See python module `argparse`.
        """
        parser.add_argument('--dirprob',
                            help='West/South/East/North probabilities',
                            type=float,
                            nargs=4, default=[.25, .25, .25, .25],
                            metavar=('WProb', 'SProb', 'EProb', 'NProb'))
        return parser
