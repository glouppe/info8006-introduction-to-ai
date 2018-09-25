import sys
from pacman_module.pacman import runGame
import time
from argparse import ArgumentParser, ArgumentTypeError
import imp
import os
from pacman_module.ghostAgents import *
import numpy as np
import sys

def restricted_float(x):
    x = float(x)
    if x < 0.1 or x > 1.0:
        raise ArgumentTypeError("%r not in range [0.1, 1.0]"%(x,))
    return x

def positive_integer(x):
    x = int(x)
    if x < 0:
        raise ArgumentTypeError("%r is not >= 0"%(x,))
    return x

def load_agent_from_file(filepath):
    class_mod = None
    expected_class = 'PacmanAgent'
    mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])

    if file_ext.lower() == '.py':
        py_mod = imp.load_source(mod_name, filepath)

    elif file_ext.lower() == '.pyc':
        py_mod = imp.load_compiled(mod_name, filepath)

    if hasattr(py_mod, expected_class):
        class_mod = getattr(py_mod, expected_class)

    return class_mod


ghosts = dict()
ghosts["greedy"] = GreedyGhost
ghosts["randy"] = RandyGhost
ghosts["lefty"] = LeftyGhost

if __name__ == '__main__':

    usageStr = """
            USAGE:      python run.py <game_options> <agent_options>
            EXAMPLES:   (1) python run.py
                            - plays a game with the random agent
                              in mediumClassic maze

            """

    parser = ArgumentParser(usageStr)
    parser.add_argument('--seed', help='RNG seed', type=int, default=1)
    parser.add_argument('--nghosts', help='Number of ghosts',
                        type=int, default=0)
    parser.add_argument('--expout', help='Timeout for get_action method',
                        type=positive_integer, default=0)
    parser.add_argument(
        '--agentfile',
        help='Python file containing a PMAgent class',
        default="humanagent.py")
    parser.add_argument(
        '--ghostagent',
        help='Ghost agent available in ghostAgents module',
        choices=["lefty", "greedy", "randy"], default="greedy")
    parser.add_argument(
        '--layout',
        help='Maze layout (from layout folder)',
        default="mediumClassic")
    parser.add_argument(
        '--silentdisplay',
        help="Disable the graphical display of the game",
        action="store_true")

    argv2 = list(sys.argv)
    sys.argv = [x for x in sys.argv if x != "-h" and x != "--help"]
    args, _ = parser.parse_known_args()
    sys.argv = argv2

    agent = load_agent_from_file(args.agentfile)

    parser = agent.arg_parser(parser)
    args = parser.parse_args()
    agent = agent(args)
    gagt = ghosts[args.ghostagent]
    if (args.nghosts > 0):
        gagts = [gagt(i + 1) for i in range(args.nghosts)]
    else: gagts = []
    total_score, total_computation_time, total_expanded_nodes = runGame(args.layout, agent, gagts, not args.silentdisplay,
            expout=args.expout)
    print ("Total score : " + str(total_score))
    print ("Total computation time (seconds) : " + str(total_computation_time))
    print ("Total expanded nodes : " + str(total_expanded_nodes))
