# XXX: Complete this class for Project Part I
import argparse
from gym_pacman.envs.game import Agent
from gym_pacman.envs.pacman import Directions
import numpy as np

class PMAgent(Agent):
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

        Parameters:
        -----------
        - `state`: the current game state. See class pacman.GameState.

        Return:
        -------
        - A legal move as defined in game.Directions.
        """
        legals = state.getLegalPacmanActions()
        if Directions.STOP in legals: legals.remove(Directions.STOP)
        #Get probability for each legal move
        probs = [self.prob_dir[x] for x in legals]
        probs = [x/sum(probs) for x in probs]
        #Returns a randomly chosen move according to probability distribution
        return np.random.choice(legals, 1, replace=True, p=probs)[0]

    
    def registerInitialState(self, state):
        """
        Given a pacman game state, returns a legal move. Called before the game.
        /!\ Not called in the online setting (See assignment).  

        Parameters:
        -----------
        - `state`: the current game state. See class pacman.GameState.

        """    
        return

    @staticmethod
    def arg_parser(parser):
        """
        Return a command line parser based on the arguments needed both 
        from this agent and the command line. See python module `argparse`.
        """ 
        parser.add_argument('--dirprob', help='Probability of taking west/south/east/north directions', type=float, nargs=4, default=[.25,.25,.25,.25], metavar=('WestProb', 'SouthProb','EastProb', 'NorthProb'))
        return parser
