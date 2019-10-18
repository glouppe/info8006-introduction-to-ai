import imp
import os
from argparse import ArgumentParser, ArgumentTypeError

from pacman_module.pacman import runGame
from pacman_module.ghostAgents import\
    GreedyGhost, SmartyGhost, DumbyGhost, EastRandyGhost


def restricted_float(x):
    x = float(x)
    if x < 0.1 or x > 1.0:
        raise ArgumentTypeError("%r not in range [0.1, 1.0]" % (x,))
    return x


def positive_integer(x):
    x = int(x)
    if x < 0:
        raise ArgumentTypeError("%r is not >= 0" % (x,))
    return x


def layout_thin_borders(layout, thickness):
    if thickness <= 1:
        return layout
    w = thickness-1
    lay = layout.replace(".lay", "")
    with open("pacman_module/layouts/" + lay + ".lay") as f:
        list_lines = f.readlines()
    for _ in range(w * 2):
        list_lines[0] = '%' + list_lines[0]
        list_lines[-1] = '%' + list_lines[-1]
    for _ in range(w):
        list_lines.insert(0, list_lines[0])
        list_lines.append(list_lines[0])
    for i in range(w+1, len(list_lines) - w-1):
        list_lines[i] = list_lines[i].replace("\n", "")
        for _ in range(w):
            list_lines[i] += '%'
            list_lines[i] = '%' + list_lines[i]
        list_lines[i] += "\n"
    with open("pacman_module/layouts/" + lay + "_thicker.lay", "w+") as f:
        f.writelines(list_lines)
    return lay + "_thicker.lay"


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
ghosts["greedy"] = GreedyGhost
ghosts["smarty"] = SmartyGhost
ghosts["dumby"] = DumbyGhost
ghosts["rightrandy"] = EastRandyGhost

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
        default=1)
    parser.add_argument(
        '--agentfile',
        help='Python file containing a `PacmanAgent` class.',
        default="humanagent.py")
    parser.add_argument(
        '--ghostagent',
        help='Ghost agent available in the `ghostAgents` module.',
        choices=["dumby", "greedy", "smarty", "rightrandy"], default="greedy")
    parser.add_argument(
        '--layout',
        help='Maze layout (from layout folder).',
        default="small_adv")
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
    # Specific to Project III
    parser.add_argument(
        '--bsagentfile',
        help='Python file containing a `BeliefStateAgent` class.',
        default=None)
    parser.add_argument(
        '--w',
        help='Parameter w as specified in instructions for Project Part 3.',
        type=int, default=1)
    parser.add_argument(
        '--p',
        help='Parameter p as specified in instructions for Project Part 3.',
        type=float, default=0.5)

    args = parser.parse_args()

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
    layout = layout_thin_borders(args.layout, args.w)
    bsagt = None
    if args.bsagentfile is not None:
        bsagt = load_agent_from_file(
            args.bsagentfile, "BeliefStateAgent")(args)

    total_score, total_computation_time, total_expanded_nodes = runGame(
        layout, agent, gagts, bsagt, not args.silentdisplay,
        expout=0, hiddenGhosts=args.hiddenghosts)

    print("Total score : " + str(total_score))
    print("Total computation time (seconds) : " + str(total_computation_time))
    print("Total expanded nodes : " + str(total_expanded_nodes))
    f = open("temp", "w+")
    s, c, e = total_score, total_computation_time, total_expanded_nodes
    f.write(str(s) + ";" + str(c) + ";" + str(e))
    f.close()
