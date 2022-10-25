import argparse
import importlib
import numpy as np
import random

from pacman_module.pacman import runGame
from pacman_module.ghostAgents import (
    AfraidGhost,
    FearlessGhost,
    TerrifiedGhost,
)


GHOSTS = {
    'afraid': AfraidGhost,
    'fearless': FearlessGhost,
    'terrified': TerrifiedGhost,
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-a',
        '--agent',
        default='bayesfilter',
        help='Python module containing `PacmanAgent` and `BeliefStateAgent` classes.',
    )

    parser.add_argument(
        '-g',
        '--ghost',
        choices=list(GHOSTS.keys()),
        default='afraid',
        help='Ghost agent from the `ghostAgents` module.',
    )

    parser.add_argument(
        '-ng',
        '--nghosts',
        type=int,
        default=1,
        help='The maximum number of ghost agents.',
    )

    parser.add_argument(
        '--visible',
        action='store_true',
        default=False,
        help='Whether ghosts are visbile or not.',
    )

    parser.add_argument(
        '-l',
        '--layout',
        default='large_filter',
        help='Maze layout from the `layouts` directory.',
    )

    parser.add_argument(
        '--nographics',
        action='store_true',
        default=False,
        help='Disable the graphical display of the game.',
    )

    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help='Seed for random number generator.',
    )

    args = parser.parse_args()

    if args.agent == 'humanagent' and args.nographics:
        raise ValueError("Human agent cannot play without graphics")

    random.seed(args.seed)
    np.random.seed(args.seed)

    module = importlib.import_module(args.agent)

    score, time, _ = runGame(
        layout_name=args.layout,
        pacman=module.PacmanAgent(),
        ghosts=[GHOSTS[args.ghost](i+1) for i in range(args.nghosts)],
        beliefstateagent=module.BeliefStateAgent(args.ghost),
        displayGraphics=not args.nographics,
        expout=0.0,
        hiddenGhosts=not args.visible,
        edibleGhosts=True,
    )

    print(f"Score: {score}")
    print(f"Computation time: {time}")
