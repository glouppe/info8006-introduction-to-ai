"""
---------------------------------------
Introduction to artificial intelligence
---------------------------------------
@ Axelle Schyns    - S180598
@ Victor Mangeleer - S181670

"""
import numpy as np

"""
----
Note
----
This idea of computing the exact distance between Pacman and
every other cell in the maze comes from us as well as the
recursiv implementation of the algorithm.

However, while discussing with Thomas Pirrotin, he proposed
to us the excellent idea of implementing the algorithm using queues !

Therefore, all the credit for the function 'maze_distances_iter' belongs
to Thomas Pirottin.

We decided to show both solutions in order to demonstrate what multiple minds
can create while working together.

------------
Maze version
------------
"""
# Defines which version to use (True = recursiv, False = iterativ (queu))
maze_version = False


def md_recursiv(walls, value, pos_x, pos_y, dim, road_map):
    """
    This function calculates the exact distance from Pacman
    to every other position in the maze (Recursiv part of
    the algorithm)

    Arguments:
    ----------
    - 'walls' : a boolean matrix containing the position of the walls

    - 'value' : the distance between Pacman and a cell (Pacman's position
                has the value 0, cells next to it 1, and so on...)

    - 'pos_x/y' : the index of the observed position

    - 'dim' : turple containing the dimension of the maze where
                    dim..[0] = length and dim..[1] = witdh

    - 'road_map' : a numpy matrix containg the value of each cells, i.e
                   the distance from pacman to a cell
    """

    # 1 - Updates the value related to the current position
    road_map[pos_x][pos_y] = value

    # 2 - Updates the values in the cell next to the current one
    # Upper cell
    if md_condition(walls, value, pos_x + 1, pos_y, dim, road_map) is True:
        md_recursiv(walls, value + 1, pos_x + 1, pos_y, dim, road_map)

    # Down cell
    if md_condition(walls, value, pos_x - 1, pos_y, dim, road_map) is True:
        md_recursiv(walls, value + 1, pos_x - 1, pos_y, dim, road_map)

    # Right cell
    if md_condition(walls, value, pos_x, pos_y + 1, dim, road_map) is True:
        md_recursiv(walls, value + 1, pos_x, pos_y + 1, dim, road_map)

    # Left cell
    if md_condition(walls, value, pos_x, pos_y - 1, dim, road_map) is True:
        md_recursiv(walls, value + 1, pos_x, pos_y - 1, dim, road_map)


def md_condition(walls, value, upd_x, upd_y, dim, road_map):
    """
    This function is used to tell if the cell we want to calculate
    the value with md_recursiv is admissible

    Arguments:
    ----------
    - 'walls' : a boolean matrix containing the position of the walls

    - 'value' : the distance between Pacman and a cell (Pacman's position
                has the value 0, cells next to it 1, and so on...)

    - 'upd_x/y' : the index of the new observed position (next to
      the previous one)

    - 'dim' : turple containing the dimension of the maze where
                    dim..[0] = length and dim..[1] = witdh

    - 'road_map' : a numpy matrix containg the value of each cells, i.e
                   the distance from pacman to a cell

    Return:
    -------
    - Returns a boolean value which tells us if we can update the value or not
    """

    # 1 - Verifies that the index is still inbound
    if upd_x >= dim[0] or upd_x < 0:  # Length
        return False

    if upd_y >= dim[1] or upd_y < 0:  # Witdh
        return False

    # 2 - Verifies if there is a wall or not
    if walls[upd_x][upd_y] is True:
        return False

    # 3 - Checks if the cell has already been visited
    if road_map[upd_x][upd_y] >= 0:

        # If the value is > than the one we want to put
        # in it means that there is a shorter way
        if road_map[upd_x][upd_y] > value:
            return True

        else:
            return False

    # 4 - The cell has never been explored
    return True


def maze_distances_recu(state, start_pos):
    """
    This function is used to create a matrix that contains the exact
    distance from a starting point to every other position in the maze.
    (recursively)

    Arguments:
    ----------
    - 'state' : the current game state. See FAQ and class
                `pacman.GameState`.

    - 'start_pos' : turple containing the coordinates of the
                    starting point

    Return:
    -------
    - Returns a matrix containing the distance from a position
      to every other position in the maze
    """

    # 1 - Initialization of variables
    walls = state.getWalls()

    # Determines the size of the maze.
    length = 0
    for boolean in walls:
        length = length + 1

    width = len(walls[0])

    # Stores the size of the maze
    dimension = (length, width)

    # Matrix of distances (Inialize at -1, convention)
    road_map = np.ones((length, width)) * (-1)

    # 2 - Computation of every possibilities
    md_recursiv(walls, 0, int(start_pos[0]), int(start_pos[1]),
                dimension, road_map)

    return road_map


def maze_distances_iter(state, start_pos):
    """
    This function is used to create a matrix that contains the exact
    distance from a starting point to every other position in the maze.
    (iteratively)

    Arguments:
    ----------
    - 'state' : the current game state. See FAQ and class
                `pacman.GameState`.

    - 'start_pos' : turple containing the coordinates of the
                    starting point

    Return:
    -------
    - Returns a matrix containing the distance from a position
      to every other position in the maze
    """
    # 1 - Initialization of variables
    walls = state.getWalls()

    dim = (walls.width, walls.height)

    roadMap = -np.ones(dim)
    
    start_pos = (int(start_pos[0]), int(start_pos[1]))

    posQueue = [(start_pos, 0)]

    # 2 - Updates the roadMap
    while posQueue:

        # Value corresponds to the distance between curPos and start_pos
        curPos, value = posQueue.pop(0)

        if md_condition(walls, value, curPos[0], curPos[1], dim, roadMap):

            # Places the value at the correct position
            roadMap[curPos] = value

            # Updates the value
            value += 1

            # Adds the neighbours to the queue
            nextPos = [(curPos[0], curPos[1] + 1),
                       (curPos[0], curPos[1] - 1),
                       (curPos[0] + 1, curPos[1]),
                       (curPos[0] - 1, curPos[1])]

            # Updates roadMap for each valid neighbour in the queue
            for pos in nextPos:
                if md_condition(walls, value, pos[0], pos[1], dim, roadMap):
                    posQueue.append((pos, value))

    return roadMap


def maze_retrieve(state, start_pos, end_pos, maze_dictionnary):
    """
    This function is used to get the exact distance from a starting
    point to an ending point. First it look for the distance in the
    maze dictionnary in order to see if we have not already calculated.
    If it's not the case, it computes the matrix, determines the distance
    and then add it to the dictionnary

    Arguments:
    ----------
    - 'state' : the current game state. See FAQ and class
                `pacman.GameState`.

    - 'start_pos' : turple containing the coordinates of the
                    starting point

    - 'ending_pos' : turple containing the coordinates of the
                     ending point

    Return:
    -------
    - Returns the distance from the starting point to the ending point
    """
    # 1 - Looks for the matrix associated to the starting point
    if start_pos in maze_dictionnary.keys():

        # Returns the distance
        return maze_dictionnary[start_pos][int(end_pos[0]), int(end_pos[1])]

    # 2 - Looks for the matrix associated to the ending point
    if end_pos in maze_dictionnary.keys():

        # Returns the distance
        return maze_dictionnary[end_pos][int(start_pos[0]), int(start_pos[1])]

    # 3 - The matrix has not been calculated so we compute the map and
    # add it to the dictionnary and return the distance
    if maze_version is True:
        new_map = maze_distances_recu(state, start_pos)

    else:
        new_map = maze_distances_iter(state, start_pos)

    maze_dictionnary[start_pos] = new_map

    return new_map[int(end_pos[0]), int(end_pos[1])]
