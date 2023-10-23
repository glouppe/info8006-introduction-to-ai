# ------------------------------------------------------------------------
# coding=utf-8
# ------------------------------------------------------------------------
#
#  Created by Martin J. Laubach on 2011-11-15
#
# ------------------------------------------------------------------------

import math
import turtle
import random

turtle.tracer(50000, delay=0)
turtle.register_shape("dot", ((-3,-3), (-3,3), (3,3), (3,-3)))
turtle.register_shape("tri", ((-3, -2), (0, 3), (3, -2), (0, 0)))
turtle.speed(0)
turtle.title("Poor robbie is lost")

UPDATE_EVERY = 0
DRAW_EVERY = 2

class Maze(object):
    def __init__(self, maze):
        self.maze = maze
        self.width   = len(maze[0])
        self.height  = len(maze)
        turtle.setworldcoordinates(0, 0, self.width, self.height)
        self.blocks = []
        self.update_cnt = 0
        self.one_px = float(turtle.window_width()) / float(self.width) / 2

        self.beacons = []
        for y, line in enumerate(self.maze):
            for x, block in enumerate(line):
                if block:
                    nb_y = self.height - y - 1
                    self.blocks.append((x, nb_y))
                    if block == 2:
                        self.beacons.extend(((x, nb_y), (x+1, nb_y), (x, nb_y+1), (x+1, nb_y+1)))

    def draw(self):
        for x, y in self.blocks:
            turtle.up()
            turtle.setposition(x, y)
            turtle.down()
            turtle.setheading(90)
            turtle.begin_fill()
            for _ in range(0, 4):
                turtle.fd(1)
                turtle.right(90)
            turtle.end_fill()
            turtle.up()

        turtle.color("#00ffff")
        for x, y in self.beacons:
            turtle.setposition(x, y)
            turtle.dot()
        turtle.update()

    def weight_to_color(self, weight):
        return "#%02x00%02x" % (int(weight * 255), int((1 - weight) * 255))

    def is_in(self, x, y):
        if x < 0 or y < 0 or x > self.width or y > self.height:
            return False
        return True

    def is_free(self, x, y):
        if not self.is_in(x, y):
            return False

        yy = self.height - int(y) - 1
        xx = int(x)
        return self.maze[yy][xx] == 0

    def show_mean(self, x, y, confident=False):
        if confident:
            turtle.color("#00AA00")
        else:
            turtle.color("#cccccc")
        turtle.setposition(x, y)
        turtle.shape("circle")
        turtle.stamp()

    def show_particles(self, particles):
        self.update_cnt += 1
        if UPDATE_EVERY > 0 and self.update_cnt % UPDATE_EVERY != 1:
            return

        turtle.clearstamps()
        turtle.shape('tri')

        draw_cnt = 0
        px = {}
        for p in particles:
            draw_cnt += 1
            if DRAW_EVERY == 0 or draw_cnt % DRAW_EVERY == 1:
                # Keep track of which positions already have something
                # drawn to speed up display rendering
                scaled_x = int(p.x * self.one_px)
                scaled_y = int(p.y * self.one_px)
                scaled_xy = scaled_x * 10000 + scaled_y
                if not scaled_xy in px:
                    px[scaled_xy] = 1
                    turtle.setposition(*p.xy)
                    turtle.setheading(90 - p.h)
                    turtle.color(self.weight_to_color(p.w))
                    turtle.stamp()

    def show_robot(self, robot):
        turtle.color("green")
        turtle.shape('turtle')
        turtle.setposition(*robot.xy)
        turtle.setheading(90 - robot.h)
        turtle.stamp()
        turtle.update()

    def random_place(self):
        x = random.uniform(0, self.width)
        y = random.uniform(0, self.height)
        return x, y

    def random_free_place(self):
        while True:
            x, y = self.random_place()
            if self.is_free(x, y):
                return x, y

    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def distance_to_nearest_beacon(self, x, y):
        d = 99999
        for c_x, c_y in self.beacons:
            distance = self.distance(c_x, c_y, x, y)
            if distance < d:
                d = distance
                d_x, d_y = c_x, c_y

        return d
