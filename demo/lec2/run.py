"""Run a Pacman game with one of the search agents of lecture 2.

    uv run python run.py --agentfile astar2.py --layout ex --show 1

Demo of lecture 2, originally written by Victor Mangeleer. Tidied without
changing what it does; see README.md for the options.
"""

import importlib.util
import os
import sys
from argparse import ArgumentParser, ArgumentTypeError

import tui
from pacman_module.ghostAgents import (
    DumbyGhost,
    EastRandyGhost,
    GreedyGhost,
    SmartyGhost,
)
from pacman_module.pacman import runGame

GHOSTS = {
    "greedy": GreedyGhost,
    "smarty": SmartyGhost,
    "dumby": DumbyGhost,
    "rightrandy": EastRandyGhost,
}

SEARCH_NAMES = {
    "bfs.py": "Breadth-First Search",
    "dfs.py": "Depth-First Search",
    "ucs.py": "Uniform-Cost Search",
    "gs.py": "Greedy Search",
    "astar0.py": "A-Star - Euclidean Distance",
    "astar1.py": "A-Star - Manhattan Distance",
    "astar2.py": "A-Star - Perfect Distance",
}


def restricted_float(x):
    """Argument type: a float in [0.1, 1.0]."""
    x = float(x)

    if x < 0.1 or x > 1.0:
        raise ArgumentTypeError(f"{x!r} not in range [0.1, 1.0]")

    return x


def positive_integer(x):
    """Argument type: a non-negative integer."""
    x = int(x)

    if x < 0:
        raise ArgumentTypeError(f"{x!r} is not >= 0")

    return x


def layout_thin_borders(layout, thickness):
    """Write a copy of `layout` with borders `thickness` cells thick.

    Returns the name of the layout to play, unchanged when `thickness` is 1.
    """
    if thickness <= 1:
        return layout

    w = thickness - 1
    lay = layout.replace(".lay", "")

    with open(f"pacman_module/layouts/{lay}.lay") as f:
        lines = f.readlines()

    for _ in range(w * 2):
        lines[0] = '%' + lines[0]
        lines[-1] = '%' + lines[-1]

    for _ in range(w):
        lines.insert(0, lines[0])
        lines.append(lines[0])

    for i in range(w + 1, len(lines) - w - 1):
        lines[i] = lines[i].replace("\n", "")
        for _ in range(w):
            lines[i] = '%' + lines[i] + '%'
        lines[i] += "\n"

    with open(f"pacman_module/layouts/{lay}_thicker.lay", "w+") as f:
        f.writelines(lines)

    return f"{lay}_thicker.lay"


def load_agent_from_file(filepath, class_module):
    """Load and return the `class_module` class defined in `filepath`."""
    mod_name = os.path.splitext(os.path.split(filepath)[-1])[0]

    # importlib replaces imp, which was removed in Python 3.12
    spec = importlib.util.spec_from_file_location(mod_name, filepath)
    py_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(py_mod)

    return getattr(py_mod, class_module, None)


def search_name(agentfile):
    """Return the name of the search implemented by `agentfile`."""
    return SEARCH_NAMES.get(agentfile, agentfile)


def print_results(score, computation_time, expanded_nodes):
    """Print the score, the expanded nodes and the computation time."""
    tui.panel("Result", [
        ("Score", int(score)),
        ("Expanded nodes", expanded_nodes),
        ("Time", tui.seconds(computation_time)),
    ])


def parse_args():
    """Return the command-line arguments of the demo."""
    usage = """
    USAGE:      python run.py <game_options> <agent_options>
    EXAMPLES:   (1) python run.py
                    - plays a game with the human agent
                      in small maze
    """
    parser = ArgumentParser(usage)

    parser.add_argument(
        '--show',
        help='Choose to display the path or the search method',
        type=int,
        default=0)
    parser.add_argument(
        '--seed',
        help='Seed for random number generator',
        type=int,
        default=1)
    parser.add_argument(
        '--agentfile',
        help='Python file containing a `PacmanAgent` class.',
        default="humanagent.py")
    parser.add_argument(
        '--ghostagent',
        help='Ghost agent available in the `ghostAgents` module.',
        choices=list(GHOSTS), default="greedy")
    parser.add_argument(
        '--layout',
        help='Maze layout (from layout folder).',
        default="ex")
    parser.add_argument(
        '--nghosts',
        help='Maximum number of ghosts in a maze.',
        type=int, default=1)
    parser.add_argument(
        '--hiddenghosts',
        help='Whether the ghost is graphically hidden or not.',
        default=False, action="store_true")
    parser.add_argument(
        '--silentdisplay',
        help="Disable the graphical display of the game.",
        action="store_true")
    parser.add_argument(
        '--bsagentfile',
        help='Python file containing a `BeliefStateAgent` class.',
        default=None)
    parser.add_argument(
        '--w',
        help='Thickness of the borders of the layout.',
        type=int, default=1)
    parser.add_argument(
        '--p',
        help='Parameter p, kept for compatibility with the other demos.',
        type=float, default=0.5)

    return parser.parse_args()


def main():
    """Play one game and print what it cost to solve it."""
    args = parse_args()

    tui.logo()
    rows = [("Search", search_name(args.agentfile)), ("Layout", args.layout)]
    if args.nghosts > 0:
        rows.append(("Ghosts", f"{args.nghosts} {args.ghostagent}"))
    tui.panel("Game", rows)

    if args.agentfile == "humanagent.py" and args.silentdisplay:
        print("Human agent cannot play without graphical display")
        sys.exit()

    agent = load_agent_from_file(args.agentfile, "PacmanAgent")(args)

    ghost = GHOSTS[args.ghostagent]
    ghosts = [ghost(i + 1, args) for i in range(max(args.nghosts, 0))]

    bsagent = None
    if args.bsagentfile is not None:
        bsagent = load_agent_from_file(
            args.bsagentfile, "BeliefStateAgent")(args)

    layout = layout_thin_borders(args.layout, args.w)

    score, computation_time, expanded_nodes = runGame(
        layout, agent, ghosts, bsagent, not args.silentdisplay,
        expout=0, hiddenGhosts=args.hiddenghosts, show=args.show)

    print_results(score, computation_time, expanded_nodes)

    # Scratch file read back by the scripts that compare the agents
    with open("temp", "w+") as f:
        f.write(f"{score};{computation_time};{expanded_nodes}")


if __name__ == '__main__':
    main()
