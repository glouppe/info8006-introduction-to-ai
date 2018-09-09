import gym
from gym import spaces
from gym.utils import seeding
import numpy as np

from .graphicsDisplay import PacmanGraphics, DEFAULT_GRID_SIZE

from .game import Actions
from .pacman import ClassicGameRules
from .layout import getLayout, getRandomLayout

from .ghostAgents import *
from .pacmanAgents import *

from gym.utils import seeding

import json
import os
import stopit
from copy import deepcopy

DEFAULT_GHOST_TYPE = 'DirectionalGhost'

MAX_GHOSTS = 5

PACMAN_ACTIONS = ['North', 'South', 'East', 'West', 'Stop']

PACMAN_DIRECTIONS = ['North', 'South', 'East', 'West']
ROTATION_ANGLES = [0, 180, 90, 270]

MAX_EP_LENGTH = np.inf

import os
fdir = '/'.join(os.path.split(__file__)[:-1])
#print(fdir)
layout_params = json.load(open(fdir + '/../../layout_params.json'))

"""
print("Layout parameters")
print("------------------")
for k in layout_params:
    print(k,":",layout_params[k])
print("------------------")
"""


def get_action_timeout_call(agent,queue,state):
    queue.put(agent.getAction(state))

class PacmanEnv(gym.Env):
    layouts = [
        'capsuleClassic', 'contestClassic', 'mediumClassic', 'mediumGrid', 'minimaxClassic', 'openClassic', 'originalClassic', 'smallClassic', 'capsuleClassic', 'smallGrid', 'testClassic', 'trappedClassic', 'trickyClassic'
    ]

    noGhost_layouts = [l + '_noGhosts' for l in layouts]

    MAX_MAZE_SIZE = (7, 7)
    num_envs = 1

    observation_space = spaces.Box(low=0, high=255,
            shape=(84, 84, 3), dtype=np.uint8)

    def __init__(self):
        self.action_space = spaces.Discrete(4) # up, down, left right
        self.display = PacmanGraphics(1.0)
        self._action_set = range(len(PACMAN_ACTIONS))
        self.location = None
        self.viewer = None
        self.done = False
        self.layout = None
        self.np_random = None

    def setObservationSpace(self):
        screen_width, screen_height = self.display.calculate_screen_dimensions(self.layout.width,   self.layout.height)
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

    def reset(self, layout=None,max_ghosts=MAX_GHOSTS,ghostclass=DirectionalGhost, ghostkwargs={}, pacmanagent=None, timeout=60, reginitstate=True):
        # get new layout
        #if self.layout is None:
        #    self.chooseLayout(randomLayout=True)
        noGhost = max_ghosts == 0
        if layout is None:
                self.chooseLayout(randomLayout=True,chosenLayout=None, no_ghosts=noGhost)
        else:
                self.chooseLayout(randomLayout=False,chosenLayout=layout, no_ghosts=noGhost)

        self.step_counter = 0
        self.cum_reward = 0
        self.done = False
        self.timeout = timeout

        self.setObservationSpace()

        # we don't want super powerful ghosts
        self.ghosts = [ghostclass( i+1, **ghostkwargs) for i in range(max_ghosts)]

        # this agent is just a placeholder for graphics to work
        if (pacmanagent is None):
            pacmanagent = GreedyAgent()
        self.pacman = pacmanagent
        self.pacman.displutils = self.display.graphicsUtils

        self.rules = ClassicGameRules(timeout)
        self.rules.quiet = False

        self.game = self.rules.newGame(self.layout, self.pacman, self.ghosts,
            self.display, False, False)

        self.game.init()
        
        if (reginitstate):
            self.pacman.registerInitialState(self.game.state)

        self.display.initialize(self.game.state.data)
        self.display.updateView()

        self.location = self.game.state.data.agentStates[0].getPosition()
        self.ghostLocations = [a.getPosition() for a in self.game.state.data.agentStates[1:]]
        self.ghostInFrame = any([np.sum(np.abs(np.array(g) - np.array(self.location))) <= 2 for g in self.ghostLocations])

        self.location_history = [self.location]
        self.orientation = PACMAN_DIRECTIONS.index(self.game.state.data.agentStates[0].getDirection())
        self.orientation_history = [self.orientation]
        self.illegal_move_counter = 0

        self.cum_reward = 0

        self.initial_info = {
            'past_loc': [self.location_history[-1]],
            'curr_loc': [self.location_history[-1]],
            'past_orientation': [[self.orientation_history[-1]]],
            'curr_orientation': [[self.orientation_history[-1]]],
            'illegal_move_counter': [self.illegal_move_counter],
            'ghost_positions': [self.ghostLocations],
            'ghost_in_frame': [self.ghostInFrame],
            'step_counter': [[0]],
        }

        
        self.previous_pacman_action = "Stop"
        

        return self._get_image()

    def step(self):
        # implement code here to take an action
        if self.step_counter >= MAX_EP_LENGTH or self.done:
            self.step_counter += 1
            return np.zeros(self.observation_space.shape), 0.0, True, {
                'past_loc': [self.location_history[-2]],
                'curr_loc': [self.location_history[-1]],
                'past_orientation': [[self.orientation_history[-2]]],
                'curr_orientation': [[self.orientation_history[-1]]],
                'illegal_move_counter': [self.illegal_move_counter],
                'step_counter': [[self.step_counter]],
                'ghost_positions': [self.ghostLocations],
                'r': [self.cum_reward],
                'l': [self.step_counter],
                'ghost_in_frame': [self.ghostInFrame],
                'episode': [{
                    'r': self.cum_reward,
                    'l': self.step_counter
                }]
            }

        """
        queue = Queue()
        proc = Process(target=get_action_timeout_call, args=(self.pacman,queue,self.game.state))
        proc.start()
        try:
            pacman_action = queue.get(timeout=self.timeout)
            proc.join()
        except:
            pacman_action = self.previous_pacman_action
            proc.terminate()
            
        """
        with stopit.ThreadingTimeout(self.timeout) as to_ctx_mgr:
            assert to_ctx_mgr.state == to_ctx_mgr.EXECUTING
            pacman_action = self.pacman.getAction(self.game.state)

        if to_ctx_mgr.state == to_ctx_mgr.TIMED_OUT:
            print("Timed out !")
            pacman_action = self.previous_pacman_action
        
        legal_actions = self.game.state.getLegalPacmanActions()
        illegal_action = False
        if pacman_action not in legal_actions:
            self.illegal_move_counter += 1
            illegal_action = True
            pacman_action = "STOP" # Stop is always legal



        reward = self.game.step(pacman_action)
        self.cum_reward += reward
        # reward shaping for illegal actions
        

        done = self.game.state.isWin() or self.game.state.isLose()

        self.location = self.game.state.data.agentStates[0].getPosition()
        self.location_history.append(self.location)
        self.ghostLocations = [a.getPosition() for a in self.game.state.data.agentStates[1:]]

        self.orientation = PACMAN_DIRECTIONS.index(self.game.state.data.agentStates[0].getDirection())
        self.orientation_history.append(self.orientation)

        extent = (self.location[0] - 1, self.location[1] - 1),(self.location[0] + 1, self.location[1] + 1),
        self.ghostInFrame = any([ g[0] >= extent[0][0] and g[1] >= extent[0][1] and g[0] <= extent[1][0] and g[1] <= extent[1][1]
            for g in self.ghostLocations])
        self.step_counter += 1
        info = {
            'past_loc': [self.location_history[-2]],
            'curr_loc': [self.location_history[-1]],
            'past_orientation': [[self.orientation_history[-2]]],
            'curr_orientation': [[self.orientation_history[-1]]],
            'illegal_move_counter': [self.illegal_move_counter],
            'step_counter': [[self.step_counter]],
            'episode': [None],
            'ghost_positions': [self.ghostLocations],
            'ghost_in_frame': [self.ghostInFrame],
        }
        self.previous_pacman_action = pacman_action

        if self.step_counter >= MAX_EP_LENGTH:
            done = True

        self.done = done

        if self.done: # only if done, send 'episode' info
            info['episode'] = [{
                'r': self.cum_reward,
                'l': self.step_counter
            }]
        return self._get_image(), reward, done, info

    def get_action_meanings(self):
        return [PACMAN_ACTIONS[i] for i in self._action_set]

    # just change the get image function
    def _get_image(self):
        # get x, y
        image = self.display.image

        w, h = image.size
        DEFAULT_GRID_SIZE_X, DEFAULT_GRID_SIZE_Y = w / float(self.layout.width), h / float(self.layout.height)

        extent = [
            DEFAULT_GRID_SIZE_X *  (self.location[0] - 1),
            DEFAULT_GRID_SIZE_Y *  (self.layout.height - (self.location[1] + 2.2)),
            DEFAULT_GRID_SIZE_X *  (self.location[0] + 2),
            DEFAULT_GRID_SIZE_Y *  (self.layout.height - (self.location[1] - 1.2))]
        extent = tuple([int(e) for e in extent])
        self.image_sz = (84,84)
        image = image.crop(extent).resize(self.image_sz)
        return np.array(image)

    def render(self, mode='human'):
        img = self._get_image()
        if mode == 'rgb_array':
            return img
        elif mode == 'human':
            from gym.envs.classic_control import rendering
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
