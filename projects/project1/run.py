import argparse
import importlib

from pacman_module.pacman import runGame


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-a',
        '--agent',
        default='humanagent',
        help='Python module containing a `PacmanAgent` class.',
    )

    parser.add_argument(
        '-l',
        '--layout',
        default='large',
        help='Maze layout from the `layouts` directory.',
    )

    parser.add_argument(
        '--nographics',
        action='store_true',
        default=False,
        help='Disable the graphical display of the game.',
    )

    args = parser.parse_args()

    if args.agent == 'humanagent' and args.nographics:
        raise ValueError("Human agent cannot play without graphics")

    score, time, nodes = runGame(
        layout_name=args.layout,
        pacman=importlib.import_module(args.agent).PacmanAgent(),
        ghosts=[],
        beliefstateagent=None,
        displayGraphics=not args.nographics,
        expout=0.0,
        hiddenGhosts=False,
    )

    print(f"Score: {score}")
    print(f"Computation time: {time}")
    print(f"Expanded nodes: {nodes}")
