import imp
import os
from argparse import ArgumentParser, ArgumentTypeError
import random
from pacman_module.pacman import runGame
from pacman_module.ghostAgents import\
    ConfusedGhost, AfraidGhost, ScaredGhost
import numpy as np


def proba_float(x):
    x = float(x)
    if x < 0 or x > 1:
        raise ArgumentTypeError("%r is not between 0 and 1" % (x,))
    return x


def strictly_positive_integer(x):
    x = int(x)
    if x <= 0:
        raise ArgumentTypeError("%r is not > 0" % (x,))
    return x


def strictly_positive_float(x):
    x = float(x)
    if x <= 0:
        raise ArgumentTypeError("%r is not > 0" % (x,))
    return x


def load_agent_from_file(filepath, class_module):
    class_mod = None
    expected_class = class_module
    mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])

    if file_ext.lower() == '.py':
        py_mod = imp.load_source(mod_name, filepath)

    elif file_ext.lower() == '.pyc':
        py_mod = imp.load_compiled(mod_name, filepath)

    if hasattr(py_mod, expected_class):
        class_mod = getattr(py_mod, expected_class)

    return class_mod


ghosts = {}
ghosts["confused"] = ConfusedGhost
ghosts["afraid"] = AfraidGhost
ghosts["scared"] = ScaredGhost

if __name__ == '__main__':
    usage = """
    USAGE:      python run.py <game_options> <agent_options>
    EXAMPLES:   (1) python run.py
                    - plays a game with the human agent
                      in small maze
    """

    parser = ArgumentParser(usage)
    parser.add_argument(
        '--seed',
        help='Seed for random number generator',
        type=int,
        default=-1)
    parser.add_argument(
        '--agentfile',
        help='Python file containing a `PacmanAgent` class.',
        default="humanagent.py")
    parser.add_argument(
        '--ghostagent',
        help='Ghost agent available in the `ghostAgents` module.',
        choices=["confused", "afraid", "scared"], default="confused")
    parser.add_argument(
        '--layout',
        help='Maze layout (from layout folder).',
        default="large_filter")
    parser.add_argument(
        '--nghosts',
        help='Maximum number of ghosts in a maze.',
        type=int, default=1)
    parser.add_argument(
        '--silentdisplay',
        help="Disable the graphical display of the game.",
        action="store_true")

    # Specific to Project III
    parser.add_argument(
        '--bsagentfile',
        help='Python file containing a `BeliefStateAgent` class.',
        default=None)
    parser.add_argument(
        '--edibleghosts',
        help='Whether the ghost can be eaten.',
        default=True,
        action="store_true")
    parser.add_argument(
        '--hiddenghosts',
        help='Whether the ghosts are graphically hidden or not.',
        default=False,
        action="store_true")
    parser.add_argument(
        '--sensorvariance',
        help='The variance of the sensor estimates.',
        default=1.0,
        type=float)

    args = parser.parse_args()

    if args.seed >= 0:
        np.random.seed(args.seed)
        random.seed(args.seed)

    if (args.agentfile == "humanagent.py" and args.silentdisplay):
        print("Human agent cannot play without graphical display")
        exit()
    agent = load_agent_from_file(args.agentfile, "PacmanAgent")(args)

    gagt = ghosts[args.ghostagent]
    nghosts = args.nghosts
    if (nghosts > 0):
        gagts = [gagt(i + 1, args) for i in range(nghosts)]
    else:
        gagts = []
    layout = args.layout
    bsagt = None
    if args.bsagentfile is not None:
        bsagt = load_agent_from_file(
            args.bsagentfile, "BeliefStateAgent")(args)

    total_score, total_computation_time, _ = runGame(
        layout, agent, gagts, bsagt, not args.silentdisplay, expout=0,
        hiddenGhosts=args.hiddenghosts, edibleGhosts=args.edibleghosts)

    print("Total score : " + str(total_score))
    print("Total computation time (seconds) : " + str(total_computation_time))
    f = open("temp", "w+")
    s, c = total_score, total_computation_time
    f.write(str(s) + ";" + str(c))
    f.close()
