import gym
from gym import spaces
from gym.utils import seeding
import numpy as np

from .graphicsDisplay import PacmanGraphics, DEFAULT_GRID_SIZE
from gym.envs.classic_control import rendering
from .game import Actions
from .pacman import ClassicGameRules
from .layout import getLayout, getRandomLayout

from .ghostAgents import *
from .pacmanAgents import *

from gym.utils import seeding
import os
import json
import os
import stopit
from copy import deepcopy


from PIL import Image
DEFAULT_GHOST_TYPE = 'DirectionalGhost'

MAX_GHOSTS = 5

PACMAN_ACTIONS = ['North', 'South', 'East', 'West', 'Stop']

PACMAN_DIRECTIONS = ['North', 'South', 'East', 'West']
ROTATION_ANGLES = [0, 180, 90, 270]




fdir = '/'.join(os.path.split(__file__)[:-1])
# print(fdir)
layout_params = json.load(open(fdir + '/../../layout_params.json'))

"""
print("Layout parameters")
print("------------------")
for k in layout_params:
    print(k,":",layout_params[k])
print("------------------")
"""


class PacmanEnv(gym.Env):
    layouts = [
        'capsuleClassic',
        'contestClassic',
        'mediumClassic',
        'mediumGrid',
        'minimaxClassic',
        'openClassic',
        'originalClassic',
        'smallClassic',
        'capsuleClassic',
        'smallGrid',
        'testClassic',
        'trappedClassic',
        'trickyClassic']

    noGhost_layouts = [l + '_noGhosts' for l in layouts]

    MAX_MAZE_SIZE = (7, 7)
    num_envs = 1

    observation_space = spaces.Box(low=0, high=255,
                                   shape=(84, 84, 3), dtype=np.uint8)

    def __init__(self):
        self.action_space = spaces.Discrete(4)  # up, down, left right
        self.display = PacmanGraphics(1.0)
        self._action_set = range(len(PACMAN_ACTIONS))
        self.location = None
        self.viewer = None
        self.done = False
        self.layout = None
        self.np_random = None

    def setObservationSpace(self):
        screen_width, screen_height = self.display.calculate_screen_dimensions(
            self.layout.width, self.layout.height)
        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=(int(screen_height),
                                                   int(screen_width),
                                                   3), dtype=np.uint8)

    def chooseLayout(self, randomLayout=True,
                     chosenLayout=None, no_ghosts=True):

        if randomLayout:
            self.layout = getRandomLayout(layout_params, self.np_random)
        else:
            if chosenLayout is None:
                if not no_ghosts:
                    chosenLayout = self.np_random.choice(self.layouts)
                else:
                    chosenLayout = self.np_random.choice(self.noGhost_layouts)
            self.chosen_layout = chosenLayout
            print("Chose layout", chosenLayout)
            self.layout = getLayout(chosenLayout)
        self.maze_size = (self.layout.width, self.layout.height)

    def seed(self, seed=None):
        if self.np_random is None:
            self.np_random, seed = seeding.np_random(seed)
        self.chooseLayout(randomLayout=True)
        return [seed]

    def reset(
            self,
            layout=None,
            max_ghosts=MAX_GHOSTS,
            ghostclass=DirectionalGhost,
            ghostkwargs={},
            pacmanagent=None,
            timeout=60):
        # get new layout
        # if self.layout is None:
        #    self.chooseLayout(randomLayout=True)
        noGhost = max_ghosts == 0
        if layout is None:
            self.chooseLayout(
                randomLayout=True,
                chosenLayout=None,
                no_ghosts=noGhost)
        else:
            self.chooseLayout(
                randomLayout=False,
                chosenLayout=layout,
                no_ghosts=noGhost)

        self.step_counter = 0
        self.cum_reward = 0
        self.done = False
        self.timeout = timeout

        self.setObservationSpace()

        # we don't want super powerful ghosts
        self.ghosts = [ghostclass(i + 1, **ghostkwargs)
                       for i in range(max_ghosts)]

        # this agent is just a placeholder for graphics to work
        if (pacmanagent is None):
            pacmanagent = GreedyAgent()
        self.pacman = pacmanagent

        self.rules = ClassicGameRules(timeout)
        self.rules.quiet = False

        self.game = self.rules.newGame(self.layout, self.pacman, self.ghosts,
                                       self.display, False, False)

        self.game.init()

        self.display.initialize(self.game.state.data)
        

        self.cum_reward = 0

        

        self.previous_pacman_action = "Stop"

        return self.game.state

    def step(self):
     
        with stopit.ThreadingTimeout(self.timeout) as to_ctx_mgr:
            assert to_ctx_mgr.state == to_ctx_mgr.EXECUTING
            pacman_action = self.pacman.get_action(self.game.state)

        if to_ctx_mgr.state == to_ctx_mgr.TIMED_OUT:
            print("Timed out !")
            pacman_action = self.previous_pacman_action

        legal_actions = self.game.state.getLegalPacmanActions()
        illegal_action = False
        if pacman_action not in legal_actions:
            self.illegal_move_counter += 1
            illegal_action = True
            pacman_action = "STOP"  # Stop is always legal

        reward = self.game.step(pacman_action)
        self.cum_reward += reward

        done = self.game.state.isWin() or self.game.state.isLose()


      
        self.previous_pacman_action = pacman_action

     

        self.done = done

    
        return self.game.state, reward, done, None

    def get_action_meanings(self):
        return [PACMAN_ACTIONS[i] for i in self._action_set]

    # just change the get image function
    def _get_image(self):
        # get x, y

        image = self.display.image

        w, h = image.size
        DEFAULT_GRID_SIZE_X, DEFAULT_GRID_SIZE_Y = w / \
            float(self.layout.width), h / float(self.layout.height)

        self.image_sz = (w // 2, h // 2)
        image = image.resize(self.image_sz, Image.BICUBIC)
        return np.array(image)

    def render(self, mode='human'):
        img = self._get_image()
        if mode == 'rgb_array':
            return img
        elif mode == 'human':
            if self.viewer is None:
                self.viewer = rendering.SimpleImageViewer()
            self.viewer.imshow(img)
            return self.viewer.isopen

    def close(self):
        # TODO: implement code here to do closing stuff
        if self.viewer is not None:
            self.viewer.close()
        self.display.finish()

    def __del__(self):
        self.close()
