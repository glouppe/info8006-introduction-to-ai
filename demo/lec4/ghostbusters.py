"""Ghostbusters, the demo of lecture 4.

A ghost hides in the grid. Clicking a cell reads its noisy sensor, which
reports a color depending on how far the ghost is. The game is the one of
the two videos of the lecture: with the beliefs hidden, the player guesses
from the colors; with the beliefs shown, the posterior P(G | readings) is
maintained by Bayes' rule and the ghost has nowhere left to hide.

Press P during the game to switch from one to the other.
"""

import argparse
import random
import tkinter as tk

# Sensor model P(color | distance). The band of a distance gives the color
# the sensor should report; it reports a neighboring color instead with
# probability NOISE, which is what makes a single reading inconclusive.
COLORS = ["red", "orange", "yellow", "green"]
NOISE = 0.2

CELL_FILL = "#1e90ff"
CELL_LINE = "#63b8ff"
PANEL_BG = "#000000"
PANEL_FG = "#bebebe"
READING_INK = {
    "red": "#ff0000",
    "orange": "#ff8c00",
    "yellow": "#ffff00",
    "green": "#00ee00",
}


def band(distance):
    """The color the sensor reports when it is not fooled by the noise."""
    if distance == 0:
        return 0  # red
    if distance <= 2:
        return 1  # orange
    if distance == 3:
        return 2  # yellow
    return 3  # green


def sensor_model(color, distance):
    """P(color | distance), the reading model the lecture assumes known."""
    correct = band(distance)
    index = COLORS.index(color)
    neighbors = [i for i in (correct - 1, correct + 1) if 0 <= i < len(COLORS)]
    if index == correct:
        return 1.0 - NOISE
    if index in neighbors:
        return NOISE / len(neighbors)
    return 0.0


class Game:
    """The world, the readings and the belief state over the ghost location."""

    def __init__(self, rows, cols, rng, moving=False):
        self.rows, self.cols, self.rng, self.moving = rows, cols, rng, moving
        self.reset()

    def reset(self):
        self.cells = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        self.ghost = self.rng.choice(self.cells)
        self.belief = {cell: 1.0 / len(self.cells) for cell in self.cells}
        self.readings = {}
        self.score = 0
        self.busts = 1
        self.over = False

    def distance(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def sense(self, cell):
        """Read the sensor at cell, then update the belief with Bayes' rule."""
        distance = self.distance(cell, self.ghost)
        weights = [sensor_model(color, distance) for color in COLORS]
        color = self.rng.choices(COLORS, weights=weights)[0]
        self.readings[cell] = color
        self.score -= 1
        # P(G | r_1:k+1) = P(r_k+1 | G) P(G | r_1:k) / Z, the readings being
        # conditionally independent given the ghost location.
        for ghost in self.cells:
            self.belief[ghost] *= sensor_model(color, self.distance(cell, ghost))
        self.normalize()
        return color

    def normalize(self):
        total = sum(self.belief.values())
        if total == 0:  # only reachable if the model gives an impossible reading
            total = len(self.cells)
            self.belief = {cell: 1.0 for cell in self.cells}
        for cell in self.cells:
            self.belief[cell] /= total

    def neighbors(self, cell):
        r, c = cell
        moves = [(r, c), (r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        return [m for m in moves if 0 <= m[0] < self.rows and 0 <= m[1] < self.cols]

    def tick(self):
        """One time step: the ghost moves, and the belief is pushed forward.

        This is the transition model of lecture 6, applied between two
        readings. With a still ghost, it does nothing.
        """
        if not self.moving:
            return
        self.ghost = self.rng.choice(self.neighbors(self.ghost))
        predicted = {cell: 0.0 for cell in self.cells}
        for cell, mass in self.belief.items():
            destinations = self.neighbors(cell)
            for destination in destinations:
                predicted[destination] += mass / len(destinations)
        self.belief = predicted
        self.readings = {}

    def bust(self, cell):
        self.busts -= 1
        hit = cell == self.ghost
        self.score += 250 if hit else -250
        self.over = True
        return hit


class Board:
    """The window: the grid on the left, the score and the readings on the right."""

    def __init__(self, game, cell=70, beliefs=False):
        self.game, self.cell, self.beliefs = game, cell, beliefs
        self.arming = False
        self.messages = []

        self.root = tk.Tk()
        self.root.title("Ghostbusters")
        width = game.cols * cell
        height = game.rows * cell
        self.canvas = tk.Canvas(self.root, width=width, height=height,
                                bg=PANEL_BG, highlightthickness=0)
        self.canvas.grid(row=0, column=0)
        self.panel = tk.Canvas(self.root, width=300, height=height,
                               bg=PANEL_BG, highlightthickness=0)
        self.panel.grid(row=0, column=1)

        self.canvas.bind("<Button-1>", self.click)
        for key in ("p", "P"):
            self.root.bind(key, lambda _: self.toggle_beliefs())
        for key in ("b", "B"):
            self.root.bind(key, lambda _: self.arm())
        for key in ("t", "T"):
            self.root.bind(key, lambda _: self.step())
        for key in ("n", "N"):
            self.root.bind(key, lambda _: self.new_game())
        for key in ("q", "Q", "<Escape>"):
            self.root.bind(key, lambda _: self.root.destroy())
        self.draw()

    # Drawing

    def heat(self, probability):
        """Dark blue for an unlikely cell, red for a likely one."""
        weight = probability ** 0.4
        red = int(30 + 225 * weight)
        green = int(20 * (1 - weight))
        blue = int(110 * (1 - weight) + 30)
        return f"#{red:02x}{green:02x}{blue:02x}"

    def draw(self):
        self.canvas.delete("all")
        for (row, col), probability in self.game.belief.items():
            x, y = col * self.cell, row * self.cell
            fill = self.heat(probability) if self.beliefs else CELL_FILL
            self.canvas.create_rectangle(x, y, x + self.cell, y + self.cell,
                                         fill=fill, outline=CELL_LINE)
            reading = self.game.readings.get((row, col))
            if reading:
                self.canvas.create_rectangle(x + 3, y + 3,
                                             x + self.cell - 3, y + self.cell - 3,
                                             outline=READING_INK[reading], width=4)
            if self.beliefs:
                text = "<0.01" if probability < 0.005 else f"{probability:.2f}"
                self.canvas.create_text(x + self.cell / 2, y + self.cell / 2,
                                        text=text, fill="white",
                                        font=("Courier", max(9, self.cell // 6)))
        if self.game.over:
            row, col = self.game.ghost
            self.canvas.create_text(col * self.cell + self.cell / 2,
                                    row * self.cell + self.cell / 2,
                                    text="GHOST", fill="white",
                                    font=("Courier", max(9, self.cell // 7), "bold"))
        self.draw_panel()

    def draw_panel(self):
        self.panel.delete("all")
        font = ("Courier", 11)
        step = 18
        header = [
            f"GHOSTS REMAINING: {0 if self.game.over else 1}",
            f"BUSTS REMAINING:  {self.game.busts}",
            f"SCORE:            {self.game.score}",
            f"BELIEFS:          {'shown' if self.beliefs else 'hidden'}",
            "",
            "SENSOR:  red     on the ghost",
            "         orange  1 or 2 away",
            "         yellow  3 away",
            "         green   4 or more",
            f"         wrong color {int(NOISE * 100)}% of the time",
            "",
            "MESSAGES:",
        ]
        keys = [
            "click  read a sensor",
            "b      bust, then click a cell",
            "p      show or hide beliefs",
        ]
        if self.game.moving:
            keys.append("t      let one time step pass")
        keys += ["n      new game", "q      quit"]

        height = self.game.rows * self.cell
        for i, line in enumerate(header):
            self.panel.create_text(12, 14 + step * i, text=line, anchor="w",
                                   fill=PANEL_FG, font=font)
        for i, line in enumerate(keys):
            y = height - 12 - step * (len(keys) - 1 - i)
            color = "#ff4040" if self.arming and line.startswith("b ") else PANEL_FG
            self.panel.create_text(12, y, text=line, anchor="w",
                                   fill=color, font=font)
        room = int((height - 12 - step * len(keys) - (14 + step * len(header))) / step)
        for i, line in enumerate(self.messages[-max(room, 0):]):
            self.panel.create_text(12, 14 + step * (len(header) + i), text=line,
                                   anchor="w", fill=PANEL_FG, font=font)

    # Actions

    def click(self, event):
        if self.game.over:
            return
        cell = (event.y // self.cell, event.x // self.cell)
        if cell not in self.game.belief:
            return
        if self.arming:
            self.arming = False
            hit = self.game.bust(cell)
            self.messages.append(f"bust at {cell}: {'HIT' if hit else 'MISS'}")
        else:
            color = self.game.sense(cell)
            self.messages.append(f"sensor at {cell} [{color.upper()}]")
        self.draw()

    def arm(self):
        if not self.game.over:
            self.arming = True
            self.draw()

    def step(self):
        if not self.game.over:
            self.game.tick()
            self.messages.append("one time step passed")
            self.draw()

    def toggle_beliefs(self):
        self.beliefs = not self.beliefs
        self.draw()

    def new_game(self):
        self.game.reset()
        self.messages = []
        self.arming = False
        self.draw()

    def run(self):
        self.root.mainloop()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=6)
    parser.add_argument("--cols", type=int, default=10)
    parser.add_argument("--cell", type=int, default=70, help="cell size, in pixels")
    parser.add_argument("--beliefs", action="store_true",
                        help="start with the beliefs shown")
    parser.add_argument("--moving", action="store_true",
                        help="the ghost moves at each time step (lecture 6)")
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    game = Game(args.rows, args.cols, rng, moving=args.moving)
    Board(game, cell=args.cell, beliefs=args.beliefs).run()


if __name__ == "__main__":
    main()
