# graphicsUtils.py
# ----------------
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


import sys
import math
import random
import string
import time
import types
import tkinter as Tkinter
import io
from time import sleep

from PIL import Image, ImageDraw

d_o_e = None # set this in begin graphics
d_w = Tkinter._tkinter.DONT_WAIT

def formatColor(r, g, b):
        return '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))

def colorToVector(color):
        return map(lambda x: int(x, 16) / 256.0, [color[1:3], color[3:5], color[5:7]])

ghost_shape = [
        (0, - 0.5),
        (0.25, - 0.75),
        (0.5, - 0.5),
        (0.75, - 0.75),
        (0.75, 0.5),
        (0.5, 0.75),
        (- 0.5, 0.75),
        (- 0.75, 0.5),
        (- 0.75, - 0.75),
        (- 0.5, - 0.5),
        (- 0.25, - 0.75)
    ]


class GraphicsUtils:
    def __init__(self):
        self._Windows = sys.platform == 'win32'  # True if on Win95/98/NT

        self._root_window = None      # The root window for graphics output
        self._canvas = None      # The canvas which holds graphics
        self._canvas_xs = None      # Size of canvas object
        self._canvas_ys = None
        self._canvas_x = None      # Current position on canvas
        self._canvas_y = None
        self._canvas_col = None      # Current colour (set to black below)
        self._canvas_tsize = 12
        self._canvas_tserifs = 0

    

    def sleep(self, secs):
        if self._root_window == None:
            time.sleep(secs)
        else:
            self._root_window.update_idletasks()
            self._root_window.after(int(1000 * secs), self._root_window.quit)
            self._root_window.mainloop()

    def begin_graphics(self, width=640, height=480, color=formatColor(0, 0, 0), title=None):
        # Check for duplicate call
        if self._root_window is not None:
            # Lose the window.
            self._root_window.destroy()
        

        # Save the canvas size parameters
        self._canvas_xs, self._canvas_ys = width - 1, height - 1
        self._canvas_x, self._canvas_y = 0, self._canvas_ys
        self._bg_color = color

        # Create the root window
        self._root_window = Tkinter.Tk()
        self.d_o_e = self._root_window.dooneevent
        self._root_window.overrideredirect(1)
        self._root_window.protocol('WM_DELETE_WINDOW', self._destroy_window)
        # self._root_window.title(title or 'Graphics Window')
        self._root_window.resizable(0, 0)

        # Create the canvas object
        try:
            self._canvas = Tkinter.Canvas(self._root_window,
                width=width,
                height=height,
                bd=0.0,
                bg='#000000',
                highlightbackground='#000000',
                highlightcolor='#000000',
                highlightthickness=0)
            self._canvas.pack(fill=Tkinter.BOTH, expand=1)
            self.draw_background()
            self._canvas.update()
        except:
            self._root_window = None
            raise
        
        if self._Windows:
            self._canvas_tfonts = ['times new roman', 'lucida console']
        else:
            self._canvas_tfonts = ['times', 'lucidasans-24']


    def draw_background(self):
        corners = [(0,0), (0, self._canvas_ys), (self._canvas_xs, self._canvas_ys), (self._canvas_xs, 0)]
        self.polygon(corners, self._bg_color, fillColor=self._bg_color, filled=True, smoothed=False)

    def _destroy_window(self, event=None):
        pass
        # sys.exit(0)
        # self._root_window.destroy()
        # self._root_window = None
        # print("DESTROY")

    def end_graphics(self):
        try:
            try:
                sleep(1)
                if self._root_window != None:
                    self._root_window.destroy()
            except SystemExit as e:
                print('Ending graphics raised an exception:', e)
        finally:
            self._root_window = None
            self._canvas = None

    def clear_screen(self, background=None):
        self._canvas.delete('all')
        self.draw_background()
        self._canvas_x, self._canvas_y = 0, self._canvas_ys

    def polygon(self, coords, outlineColor, fillColor=None, filled=1, smoothed=1, behind=0, width=1):
        c = []
        for coord in coords:
            c.append(coord[0])
            c.append(coord[1])
        if fillColor == None: fillColor = outlineColor
        if filled == 0: fillColor = ""
        poly = self._canvas.create_polygon(c, outline=outlineColor, fill=fillColor, smooth=smoothed, width=width)
        if behind > 0:
            self._canvas.tag_lower(poly, behind) # Higher should be more visible
        return poly

    def square(self, pos, r, color, filled=1, behind=0):
        x, y = pos
        coords = [(x - r, y - r), (x + r, y - r), (x + r, y + r), (x - r, y + r)]
        return self.polygon(coords, color, color, filled, 0, behind=behind)

    def circle(self, pos, r, outlineColor, fillColor, endpoints=None, style='pieslice', width=2):
        x, y = pos
        x0, x1 = x - r - 1, x + r
        y0, y1 = y - r - 1, y + r
        if endpoints == None:
            e = [0, 359]
        else:
            e = list(endpoints)
        while e[0] > e[1]: e[1] = e[1] + 360

        return self._canvas.create_arc(x0, y0, x1, y1, outline=outlineColor, fill=fillColor,
                                extent=e[1] - e[0], start=e[0], style=style, width=width)
        
    def image(self, filename="/tmp/pacman-frame"):
        ps = self._canvas.postscript(colormode='color')
        im = Image.open(io.BytesIO(ps.encode('utf-8')))
        w, h = im.size
        im = im.crop((1,1,w-1,h-1))
        return im


    def refresh(self):
        self._canvas.update_idletasks()

    def moveCircle(self, id, pos, r, endpoints=None):
        x, y = pos
    #    x0, x1 = x - r, x + r + 1
    #    y0, y1 = y - r, y + r + 1
        x0, x1 = x - r - 1, x + r
        y0, y1 = y - r - 1, y + r
        if endpoints == None:
            e = [0, 359]
        else:
            e = list(endpoints)
        while e[0] > e[1]: e[1] = e[1] + 360

        self.edit(id, ('start', e[0]), ('extent', e[1] - e[0]))
        self.move_to(id, x0, y0)

    def edit(self, id, *args):
        self._canvas.itemconfigure(id, **dict(args))

    def text(self, pos, color, contents, font='Helvetica', size=12, style='normal', anchor="nw"):
        x, y = pos
        font = (font, str(size), style)
        return self._canvas.create_text(x, y, fill=color, text=contents, font=font, anchor=anchor)

    def changeText(self, id, newText, font=None, size=12, style='normal'):
        self._canvas.itemconfigure(id, text=newText)
        if font != None:
            self._canvas.itemconfigure(id, font=(font, '-%d' % size, style))

    def changeColor(self, id, newColor):
        self._canvas.itemconfigure(id, fill=newColor)

    def line(self, here, there, color=formatColor(0, 0, 0), width=2):
        x0, y0 = here[0], here[1]
        x1, y1 = there[0], there[1]
        return self._canvas.create_line(x0, y0, x1, y1, fill=color, width=width)

    def remove_from_screen(self, x):
        self._canvas.delete(x)
        self.d_o_e(d_w)

    def _adjust_coords(self, coord_list, x, y):
        for i in range(0, len(coord_list), 2):
            coord_list[i] = coord_list[i] + x
            coord_list[i + 1] = coord_list[i + 1] + y
        return coord_list

    def move_to(self, object, x, y=None):
        if y is None:
            try: x, y = x
            except: raise  'incomprehensible coordinates'

        horiz = True
        newCoords = []
        current_x, current_y = self._canvas.coords(object)[0:2] # first point
        for coord in  self._canvas.coords(object):
            if horiz:
                inc = x - current_x
            else:
                inc = y - current_y
            horiz = not horiz

            newCoords.append(coord + inc)

        self._canvas.coords(object, *newCoords)
        self.d_o_e(d_w)

    def move_by(self, object, x, y=None, lift=False):
        if y is None:
            try: x, y = x
            except: raise Exception('incomprehensible coordinates')

        horiz = True
        newCoords = []
        for coord in  self._canvas.coords(object):
            if horiz:
                inc = x
            else:
                inc = y
            horiz = not horiz
            newCoords.append(coord + inc)

        self._canvas.coords(object, *newCoords)
        self.d_o_e(d_w)
        if lift:
            self._canvas.tag_raise(object)

    def writePostscript(self, filename):
        "Writes the current canvas to a postscript file."
        psfile = file(filename, 'w')
        psfile.write(self._canvas.postscript(pageanchor='sw',
                        y='0.c',
                        x='0.c'))
        psfile.close()

    