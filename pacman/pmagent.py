# XXX: Complete this class for Project Part I
import argparse
from .game import Agent

class PMAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace. Built from both main command-line parser 
                  and command-line parser built by `arg_parser`
        """
        pass

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
        return Directions.STOP

    
    def registerInitialState(self, state):
        """
        Called before the game.
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
        return parser
