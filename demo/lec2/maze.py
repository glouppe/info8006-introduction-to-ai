"""Exact distances inside a maze, used as the heuristic of `astar2.py`.

Flooding the maze from a position gives the true remaining cost to every
other cell. The maps are cached by starting position, since the heuristic is
called for every state.

Demo of lecture 2, originally written by Victor Mangeleer and Axelle Schyns,
with the queue-based flooding suggested by Thomas Pirottin. Tidied without
changing what it computes.
"""

import numpy as np

# Flood recursively (True) or with a queue (False)
maze_version = False


def md_recursiv(walls, value, pos_x, pos_y, dim, road_map):
    """Write in `road_map` the distance of every cell reachable from (x, y)."""
    road_map[pos_x][pos_y] = value

    neighbours = [
        (pos_x + 1, pos_y),
        (pos_x - 1, pos_y),
        (pos_x, pos_y + 1),
        (pos_x, pos_y - 1),
    ]

    for x, y in neighbours:
        if md_condition(walls, value, x, y, dim, road_map) is True:
            md_recursiv(walls, value + 1, x, y, dim, road_map)


def md_condition(walls, value, upd_x, upd_y, dim, road_map):
    """Return whether (upd_x, upd_y) should be given the distance `value`."""
    if upd_x >= dim[0] or upd_x < 0:
        return False

    if upd_y >= dim[1] or upd_y < 0:
        return False

    if walls[upd_x][upd_y] is True:
        return False

    # Already visited: only a strictly shorter path is worth writing
    if road_map[upd_x][upd_y] >= 0:
        return road_map[upd_x][upd_y] > value

    return True


def maze_distances_recu(state, start_pos):
    """Return the distances from `start_pos` to every cell, recursively."""
    walls = state.getWalls()
    dimension = (len(walls), len(walls[0]))

    # -1 marks a cell that has not been reached yet
    road_map = np.ones(dimension) * (-1)

    md_recursiv(walls, 0, int(start_pos[0]), int(start_pos[1]),
                dimension, road_map)

    return road_map


def maze_distances_iter(state, start_pos):
    """Return the distances from `start_pos` to every cell, with a queue."""
    walls = state.getWalls()
    dim = (walls.width, walls.height)

    road_map = -np.ones(dim)
    start_pos = (int(start_pos[0]), int(start_pos[1]))
    queue = [(start_pos, 0)]

    while queue:
        current, value = queue.pop(0)

        if md_condition(walls, value, current[0], current[1], dim, road_map):
            road_map[current] = value
            value += 1

            neighbours = [
                (current[0], current[1] + 1),
                (current[0], current[1] - 1),
                (current[0] + 1, current[1]),
                (current[0] - 1, current[1]),
            ]

            for pos in neighbours:
                if md_condition(walls, value, pos[0], pos[1], dim, road_map):
                    queue.append((pos, value))

    return road_map


def maze_retrieve(state, start_pos, end_pos, maze_dictionnary):
    """Return the exact distance between `start_pos` and `end_pos`.

    The map of `start_pos` is computed on the first call and reused after.
    Distances are symmetric, so a map already computed from `end_pos` answers
    the question as well.
    """
    if start_pos in maze_dictionnary:
        return maze_dictionnary[start_pos][int(end_pos[0]), int(end_pos[1])]

    if end_pos in maze_dictionnary:
        return maze_dictionnary[end_pos][int(start_pos[0]), int(start_pos[1])]

    if maze_version is True:
        new_map = maze_distances_recu(state, start_pos)
    else:
        new_map = maze_distances_iter(state, start_pos)

    maze_dictionnary[start_pos] = new_map

    return new_map[int(end_pos[0]), int(end_pos[1])]
