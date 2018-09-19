import sys
from PacmanGym.gym_pacman.envs import PacmanEnv
import time
from argparse import ArgumentParser
import imp
import os


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
    parser.add_argument('--timeout', help='Timeout for getAction method',
                        type=int, default=60)
    parser.add_argument(
        '--agentfile',
        help='Python file containing a PMAgent class',
        default="randomagent.py")
    parser.add_argument(
        '--layout',
        help='Maze layout (from layout folder)',
        default="mediumClassic")
    parser.add_argument(
        '--registerinitialstate',
        help="Enable the call to the registerInitialState\
              method of the agent",
        action="store_true")

    argv2 = list(sys.argv)
    sys.argv = [x for x in sys.argv if x != "-h" and x != "--help"]
    args, _ = parser.parse_known_args()
    sys.argv = argv2

    agent = load_agent_from_file(args.agentfile)

    parser = agent.arg_parser(parser)
    args = parser.parse_args()
    env = PacmanEnv()
    env.seed(args.seed)
    done = False
    agt = agent(args)
    s = env.reset(
        layout=args.layout,
        max_ghosts=args.nghosts,
        pacmanagent=agt,
        timeout=args.timeout)

    # Computation may be done before game if `registerinitialstate` has been
    # specified in command line
    if (args.registerinitialstate):
        agt.register_initial_state(s)

    while not done:
        s_, r, done, info = env.step()
        env.render()
    env.close()
