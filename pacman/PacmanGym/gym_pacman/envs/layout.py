# layout.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from .util import manhattanDistance
from .game import Grid
import os
import random
import numpy as np

VISIBILITY_MATRIX_CACHE = {}

WALL, EMPTY, PACMAN, GHOST, FOOD = 0, 1, 2, 3, 4
ITEM_REPR_STR = '% PG.'

class Layout:
    """
    A Layout manages the static information about the game board.
    """

    def __init__(self, layoutText):
        self.width = len(layoutText[0])
        self.height= len(layoutText)
        self.walls = Grid(self.width, self.height, False)
        self.food = Grid(self.width, self.height, False)
        self.capsules = []
        self.agentPositions = []
        self.numGhosts = 0
        self.processLayoutText(layoutText)
        self.layoutText = layoutText
        self.totalFood = len(self.food.asList())
        # self.initializeVisibilityMatrix()

    def getNumGhosts(self):
        return self.numGhosts

    def initializeVisibilityMatrix(self):
        global VISIBILITY_MATRIX_CACHE
        if reduce(str.__add__, self.layoutText) not in VISIBILITY_MATRIX_CACHE:
            from game import Directions
            vecs = [(-0.5,0), (0.5,0),(0,-0.5),(0,0.5)]
            dirs = [Directions.NORTH, Directions.SOUTH, Directions.WEST, Directions.EAST]
            vis = Grid(self.width, self.height, {Directions.NORTH:set(), Directions.SOUTH:set(), Directions.EAST:set(), Directions.WEST:set(), Directions.STOP:set()})
            for x in range(self.width):
                for y in range(self.height):
                    if self.walls[x][y] == False:
                        for vec, direction in zip(vecs, dirs):
                            dx, dy = vec
                            nextx, nexty = x + dx, y + dy
                            while (nextx + nexty) != int(nextx) + int(nexty) or not self.walls[int(nextx)][int(nexty)] :
                                vis[x][y][direction].add((nextx, nexty))
                                nextx, nexty = x + dx, y + dy
            self.visibility = vis
            VISIBILITY_MATRIX_CACHE[reduce(str.__add__, self.layoutText)] = vis
        else:
            self.visibility = VISIBILITY_MATRIX_CACHE[reduce(str.__add__, self.layoutText)]

    def isWall(self, pos):
        x, col = pos
        return self.walls[x][col]

    def getRandomLegalPosition(self):
        x = random.choice(range(self.width))
        y = random.choice(range(self.height))
        while self.isWall( (x, y) ):
            x = random.choice(range(self.width))
            y = random.choice(range(self.height))
        return (x,y)

    def getRandomCorner(self):
        poses = [(1,1), (1, self.height - 2), (self.width - 2, 1), (self.width - 2, self.height - 2)]
        return random.choice(poses)

    def getFurthestCorner(self, pacPos):
        poses = [(1,1), (1, self.height - 2), (self.width - 2, 1), (self.width - 2, self.height - 2)]
        dist, pos = max([(manhattanDistance(p, pacPos), p) for p in poses])
        return pos

    def isVisibleFrom(self, ghostPos, pacPos, pacDirection):
        row, col = [int(x) for x in pacPos]
        return ghostPos in self.visibility[row][col][pacDirection]

    def __str__(self):
        return "\n".join(self.layoutText)

    def deepCopy(self):
        return Layout(self.layoutText[:])

    def processLayoutText(self, layoutText):
        """
        Coordinates are flipped from the input format to the (x,y) convention here

        The shape of the maze.  Each character
        represents a different type of object.
         % - Wall
         . - Food
         o - Capsule
         G - Ghost
         P - Pacman
        Other characters are ignored.
        """
        maxY = self.height - 1
        for y in range(self.height):
            for x in range(self.width):
                layoutChar = layoutText[maxY - y][x]
                self.processLayoutChar(x, y, layoutChar)
        self.agentPositions.sort()
        self.agentPositions = [ ( i == 0, pos) for i, pos in self.agentPositions]

    def processLayoutChar(self, x, y, layoutChar):
        if layoutChar == '%':
            self.walls[x][y] = True
        elif layoutChar == '.':
            self.food[x][y] = True
        elif layoutChar == 'o':
            self.capsules.append((x, y))
        elif layoutChar == 'P':
            self.agentPositions.append( (0, (x, y) ) )
        elif layoutChar in ['G']:
            self.agentPositions.append( (1, (x, y) ) )
            self.numGhosts += 1
        elif layoutChar in  ['1', '2', '3', '4']:
            self.agentPositions.append( (int(layoutChar), (x,y)))
            self.numGhosts += 1
def getLayout(name, back = 0):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
    if name.endswith('.lay'):
        layout = tryToLoad(path + '/layouts/' + name)
        if layout == None: layout = tryToLoad(name)
    else:
        layout = tryToLoad(path + '/layouts/' + name + '.lay')
        if layout == None: layout = tryToLoad(name + '.lay')
    if layout == None and back >= 0:
        curdir = os.path.abspath('.')
        os.chdir('..')
        layout = getLayout(name, back -1)
        os.chdir(curdir)
    return layout




def generateMaze(maze_size, decimation, start_pos,np_random):
    # credits: Emilio Parisotto
    maze = np.zeros((maze_size, maze_size))

    stack = [((start_pos[0], start_pos[1]), (0, 0))]
    def add_stack(next_pos, next_dir):
        if (next_pos[0] <= 0) or (next_pos[0] >= maze_size - 1):
            return
        if (next_pos[1] <= 0) or (next_pos[1] >= maze_size - 1):
            return
        if maze[next_pos[0]][next_pos[1]] == 0.:
            stack.append((next_pos, next_dir))

    while len(stack) > 0:
        pos, prev_dir = stack.pop()
        # Has this not been filled since being added?
        if maze[pos[0]][pos[1]] == 1.:
            continue

        # Fill in this point + break down wall from previous position
        maze[pos[0]][pos[1]] = 1.
        from_y = pos[0]-prev_dir[0]
        from_x = pos[1]-prev_dir[1]
        maze[from_y][from_x] = 1.

        choices = []
        choices.append(((pos[0]-2, pos[1]  ), (-1, 0)))
        choices.append(((pos[0]  , pos[1]+2), ( 0, 1)))
        choices.append(((pos[0]  , pos[1]-2), ( 0,-1)))
        choices.append(((pos[0]+2, pos[1]  ), ( 1, 0)))

        perm = np_random.permutation(np.array(range(4)))
        for i in range(4):
            choice = choices[perm[i]]
            add_stack(choice[0], choice[1])

    for y in range(1, maze_size-1):
        for x in range(1, maze_size-1):
            if np_random.uniform() < decimation:
                maze[y][x] = 1.
    return maze

def getRandomLayout(layout_params, np_random):
    nok = True
    while nok:
        # print('Sampling new layout')
        layout, nok = randomLayout(layout_params, np_random)
    return layout

def randomLayout(layout_params, np_random):
    nok = False
    size = layout_params.get('size', 7)
    nghosts = layout_params.get('nghosts', 1)
    npellets = layout_params.get('npellets', 1)
    food_proportion = layout_params.get('food_proportion', 1.0)
    by_proportion = layout_params.get('by_proportion', True)

    start_x, start_y = np_random.randint(1, size - 1), np_random.randint(1, size - 1)


    maze = generateMaze(size, 0.3, (start_y, start_x), np_random).astype(np.int)
    # maze = np.zeros((size, size), dtype=np.int)
    # maze[1:size-1,1:size-1] = maze_
    maze[start_y, start_x] = PACMAN

    empty_positions = np.where(maze == EMPTY)
    foods = []
    if by_proportion:
        for ix in range(empty_positions[0].shape[0]):
            if np.random.rand() <= food_proportion:
                maze[empty_positions[0][ix], empty_positions[1][ix]] = FOOD
                foods.append((empty_positions[0][ix], empty_positions[1][ix]))
    else:
        food_positions = np.random.choice(np.arange(empty_positions[0].shape[0]), npellets)
        for pos in food_positions:
            maze[empty_positions[0][pos], empty_positions[1][pos]] = FOOD
            foods.append((empty_positions[0][pos], empty_positions[1][pos]))
    reachable = dfsReachabilityCheck(maze, start_x, start_y, foods)
    if not reachable:
        # print('Not reachable')
        return None, True
    empty_positions = np.where(maze == EMPTY)

    # filter out positions within 2 steps of pacman
    empty_positions = np.vstack(empty_positions)
    filter_ix = np.where(np.sum(np.abs(empty_positions - np.expand_dims([start_y, start_x], 1)), axis=0) > 2)[0]
    empty_positions = empty_positions[:, filter_ix]

    if empty_positions.shape[1] >= nghosts and nghosts > 0: # if found a proper place to put ghost
        ghost_position_ix = np_random.choice(empty_positions.shape[1], nghosts)
        for gix in ghost_position_ix:
            ghost_pos_y, ghost_pos_x = empty_positions[0][gix], empty_positions[1][gix]
            maze[ghost_pos_y, ghost_pos_x] = GHOST
    else:
        # print('Could not find enough positions for ghosts')
        return None, True

    maze_str = []
    for i in range(maze.shape[0]):
        line = ''.join([ITEM_REPR_STR[m] for m in maze[i]])
        maze_str.append(line)
    return Layout(maze_str), nok

def dfsReachabilityCheck(maze, start_x, start_y, food_positions):
    stack = [(start_y, start_x)]
    visited = set()
    while len(stack) > 0:
        curr = stack.pop()
        visited.add(curr)
        neighbors = []
        for delta in [(-1,0), (1,0), (0,-1), (0,1)]:
            next_pos = (curr[0] + delta[0], curr[1] + delta[1])
            if next_pos[0] < 0 or next_pos[1] < 0:
                continue
            elif next_pos[0] >= maze.shape[0] or next_pos[1] >= maze.shape[1]:
                continue
            elif maze[next_pos[0], next_pos[1]] == EMPTY or maze[next_pos[0], next_pos[1]] == FOOD:
                if next_pos not in visited:
                    neighbors.append(next_pos)
        stack.extend(neighbors)
    food_reachable = all([f in visited for f in food_positions])
    return food_reachable


def tryToLoad(fullname):
    if(not os.path.exists(fullname)): return None
    f = open(fullname)
    try: return Layout([line.strip() for line in f])
    finally: f.close()
