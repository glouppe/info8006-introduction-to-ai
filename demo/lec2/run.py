"""
-----------------------------------------------------------
Introduction to artificial intelligence - Course's Examples
-----------------------------------------------------------
@ Victor Mangeleer - S181670

"""

import importlib.util
import os


from Display import *
from pacman_module.pacman import runGame
from argparse import ArgumentParser, ArgumentTypeError
from pacman_module.ghostAgents import GreedyGhost, SmartyGhost, DumbyGhost, EastRandyGhost

#-----------------
# Main's Functions
#-----------------

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
    mod_name = os.path.splitext(os.path.split(filepath)[-1])[0]

    # importlib replaces imp, which was removed in Python 3.12
    spec = importlib.util.spec_from_file_location(mod_name, filepath)
    py_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(py_mod)

    return getattr(py_mod, class_module, None)

def searchName(s):

    if s == "bfs.py":
        return "Breadth-First Search"

    elif s == "dfs.py":
        return "Depth-First Search"

    elif s == "ucs.py":
        return "Uniform-Cost Search"

    elif s == "astar0.py":
        return "A-Star - Euclidean Distance"

    elif s == "astar1.py":
        return "A-Star - Manhattan Distance"

    elif s == "astar2.py":
        return "A-Star - Perfect Distance"

    elif s == "gs.py":
        return "Greedy Search"

    else:
        return s


ghosts = {}
ghosts["greedy"] = GreedyGhost
ghosts["smarty"] = SmartyGhost
ghosts["dumby"] = DumbyGhost
ghosts["rightrandy"] = EastRandyGhost

#---------
#  Main
#---------

if __name__ == '__main__':
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
        choices=["dumby", "greedy", "smarty", "rightrandy"], default="greedy")
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

    #-----------------------
    # Game's Information (1)
    #-----------------------
    # Shows the logo
    display_PACMANLOGO()

    # Shows all the games informations
    display_b("Game's Information")

    # Shows information about the search method
    print("\nSearch Method : " + searchName(args.agentfile))

    #------------
    # Game Itself
    #------------
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
        expout=0, hiddenGhosts=args.hiddenghosts, show = args.show)

    #-----------------------
    # Game's Information (2)
    #-----------------------
    # Creation of the table upper part
    c_time = "Total computation time (seconds) : " + str(total_computation_time)

    table_b = ""
    for i in range(len(c_time) - 8):
        table_b = table_b + "-" 

    # Game's data
    score = "Score                | " + str(total_score)
    exp_n = "Expanded nodes       | " + str(total_expanded_nodes)
    time =  "Computation Time [s] | " + str(total_computation_time)

    # Creation of the left part of the table
    sl = len(table_b) - len(score)
    en = len(table_b) - len(exp_n)
    tm = len(table_b) - len(time)

    for i in range(sl - 1):
        score = score + " "

    for i in range(en - 1):
        exp_n = exp_n + " "

    for i in range(tm - 1):
        time = time + " "

    score = score + "|"
    exp_n = exp_n + "|"
    time = time + "|"

    # Showing the table
    print(table_b)
    print(score)
    print(table_b)
    print(exp_n)
    print(table_b)
    print(time)
    print(table_b + "\n\n")

    f = open("temp", "w+")
    s, c, e = total_score, total_computation_time, total_expanded_nodes
    f.write(str(s) + ";" + str(c) + ";" + str(e))
    f.close()




"""
                     ALL HAIL GRANDPAC.
              LONG LIVE THE GHOSTBUSTING KING.

                  ---      ----      ---
                  |  \    /  + \    /  |
                  | + \--/      \--/ + |
                  |   +     +          |
                  | +     +        +   |
                @@@@@@@@@@@@@@@@@@@@@@@@@@
              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            \   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
             \ /  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
              V   \   @@@@@@@@@@@@@@@@@@@@@@@@@@@@
                   \ /  @@@@@@@@@@@@@@@@@@@@@@@@@@
                    V     @@@@@@@@@@@@@@@@@@@@@@@@
                            @@@@@@@@@@@@@@@@@@@@@@
                    /\      @@@@@@@@@@@@@@@@@@@@@@
                   /  \  @@@@@@@@@@@@@@@@@@@@@@@@@
              /\  /    @@@@@@@@@@@@@@@@@@@@@@@@@@@
             /  \ @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            /    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                @@@@@@@@@@@@@@@@@@@@@@@@@@
                    @@@@@@@@@@@@@@@@@@

"""




