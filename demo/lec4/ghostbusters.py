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

    def __init__(self, rows, cols, rng, policy="still"):
        self.rows, self.cols, self.rng, self.policy = rows, cols, rng, policy
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

    def step_towards(self, cell, direction):
        """The neighbor of cell in that direction, or None if off the grid."""
        destination = (cell[0] + direction[0], cell[1] + direction[1])
        return destination if destination in self.belief else None

    def turning(self, cell):
        """Clockwise and inward steps around the center of the grid."""
        dr = cell[0] - (self.rows - 1) / 2
        dc = cell[1] - (self.cols - 1) / 2
        # Rotating (dr, dc) by a quarter turn gives the clockwise tangent,
        # from which we keep the dominant axis, so that the ghost circles.
        tr, tc = dc, -dr
        clockwise = (1 if tr > 0 else -1, 0) if abs(tr) >= abs(tc) else (0, 1 if tc > 0 else -1)
        inward = (-1 if dr > 0 else 1, 0) if abs(dr) >= abs(dc) else (0, -1 if dc > 0 else 1)
        if dr == 0 and dc == 0:
            return None, None
        return self.step_towards(cell, clockwise), self.step_towards(cell, inward)

    def transition(self, cell):
        """The transition model P(next | cell) of the ghost's policy.

        It depends on the current cell only, so the filter below is exact.
        """
        if self.policy == "still":
            return {cell: 1.0}
        moves = self.neighbors(cell)
        uniform = {move: 1.0 / len(moves) for move in moves}
        if self.policy == "random":
            return uniform
        clockwise, inward = self.turning(cell)
        if self.policy == "circles":
            intents = [(clockwise, 0.8)]
        else:  # swirl: circle around the center, and drift towards it
            intents = [(clockwise, 0.6), (inward, 0.25)]
        model = {move: 0.0 for move in moves}
        spread = 1.0
        for destination, mass in intents:
            if destination is not None:
                model[destination] += mass
                spread -= mass
        for move in moves:  # what is left is spread over the legal moves
            model[move] += spread / len(moves)
        return model

    def tick(self):
        """One time step: the ghost moves, and the belief is pushed forward.

        This is the prediction step of lecture 6, applied between two
        readings. With a still ghost, it does nothing.
        """
        if self.policy == "still":
            return
        model = self.transition(self.ghost)
        self.ghost = self.rng.choices(list(model), weights=list(model.values()))[0]
        self.score -= 1
        # P(G_t+1 | r_1:k) = sum_g P(G_t+1 | g) P(g | r_1:k)
        predicted = {cell: 0.0 for cell in self.cells}
        for cell, mass in self.belief.items():
            for destination, probability in self.transition(cell).items():
                predicted[destination] += probability * mass
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

        self.buttons = {}
        self.canvas.bind("<Button-1>", self.click)
        self.panel.bind("<Button-1>", self.panel_click)
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
                text = "<0.001" if probability < 0.0005 else f"{probability:.3f}"
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
            f"GHOST:            {self.game.policy}",
            "",
            "SENSOR:  red 0   orange 1-2",
            "         yellow 3   green 4+",
            f"         wrong color {int(NOISE * 100)}% of time",
            "",
            "MESSAGES:",
        ]
        keys = [
            "click  read a sensor",
            "b      bust, then click a cell",
            "p      show or hide beliefs",
            "n      new game, q quit",
        ]

        height = self.game.rows * self.cell
        for i, line in enumerate(header):
            self.panel.create_text(12, 14 + step * i, text=line, anchor="w",
                                   fill=PANEL_FG, font=font)
        for i, line in enumerate(keys):
            y = height - 12 - step * (len(keys) - 1 - i)
            self.panel.create_text(12, y, text=line, anchor="w",
                                   fill=PANEL_FG, font=font)

        # The two buttons of the original game, above the keys.
        self.buttons = {}
        bottom = height - 12 - step * len(keys) - 16
        for i, (name, label) in enumerate([("time", "TIME+1"), ("bust", "BUST")]):
            y1 = bottom - i * 40
            box = (12, y1 - 26, 288, y1)
            active = self.arming if name == "bust" else False
            fill = "#ff0000" if active else ("#1e90ff" if name == "bust" else "#606060")
            self.panel.create_rectangle(*box, fill=fill, outline=fill)
            self.panel.create_text((box[0] + box[2]) / 2, (box[1] + box[3]) / 2,
                                   text=label, fill="white", font=("Courier", 12, "bold"))
            self.buttons[name] = box

        room = int((bottom - 52 - (14 + step * len(header))) / step)
        for i, line in enumerate(self.messages[-max(room, 0):]):
            self.panel.create_text(12, 14 + step * (len(header) + i), text=line,
                                   anchor="w", fill=PANEL_FG, font=font)

    def panel_click(self, event):
        for name, (x1, y1, x2, y2) in self.buttons.items():
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.arm() if name == "bust" else self.step()
                return

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
        if self.game.over:
            return
        if self.game.policy == "still":
            self.messages.append("the ghost does not move")
        else:
            self.game.tick()
            self.messages.append(f"one time step, ghost {self.game.policy}")
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
    parser.add_argument("--ghost", default="still",
                        choices=["still", "random", "circles", "swirl"],
                        help="how the ghost moves at each time step (lecture 6)")
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    game = Game(args.rows, args.cols, rng, policy=args.ghost)
    Board(game, cell=args.cell, beliefs=args.beliefs).run()


if __name__ == "__main__":
    main()
