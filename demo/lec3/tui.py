"""Terminal output of the demo: the banner and the framed panels.

A panel is a title and a list of (label, value) rows, drawn in a box sized on
its content. Colours are ANSI, dropped when the output is not a terminal or
when NO_COLOR is set, so that a redirected run stays readable.
"""

import os
import re
import sys

BLUE = "\033[38;5;68m"
YELLOW = "\033[38;5;220m"
GREEN = "\033[38;5;71m"
RED = "\033[38;5;167m"
DIM = "\033[2m"
BOLD = "\033[1m"
OFF = "\033[0m"

ANSI = re.compile(r"\033\[[0-9;]*m")

LOGO = r"""
 ▄▄▄▄▄   ▄▄▄  ▄▄▄▄  ▄▄▄▄▄ ▄▄  ▄▄  ▄▄▄  ▄▄  ▄▄
 ██  ██ ██ ██ ██     ██   ███▄███ ██ ██ ███ ██
 ██▀▀▀  █████ ██     ██   ██ █ ██ █████ ██▀███
 ██     ██ ██  ▀███▄ ██   ██   ██ ██ ██ ██  ██
"""


def colours():
    """True when the terminal can be expected to show ANSI colours."""
    return sys.stdout.isatty() and "NO_COLOR" not in os.environ


def paint(text, colour):
    """Wrap `text` in `colour`, or leave it alone on a plain output."""
    return f"{colour}{text}{OFF}" if colours() else str(text)


def width(text):
    """The number of columns `text` takes, colour codes excluded."""
    return len(ANSI.sub("", str(text)))


def pad(text, size, right=False):
    """Pad `text` to `size` columns, counting what is actually shown."""
    space = " " * max(size - width(text), 0)
    return space + str(text) if right else str(text) + space


def logo():
    """Print the Pacman banner."""
    print(paint(LOGO, YELLOW + BOLD))


def panel(title, rows):
    """Print `rows`, a list of (label, value), in a box titled `title`."""
    labels = max(width(label) for label, _ in rows)
    values = max(width(value) for _, value in rows)
    values = max(values, width(title) + 1 - labels)

    top = paint("┌─ ", BLUE) + paint(title, BLUE + BOLD) + " " \
        + paint("─" * (labels + values + 1 - width(title)) + "┐", BLUE)
    print(top)
    for label, value in rows:
        print(paint("│ ", BLUE) + paint(pad(label, labels), DIM)
              + "  " + pad(value, values, right=True) + paint(" │", BLUE))
    print(paint("└" + "─" * (labels + values + 4) + "┘", BLUE) + "\n")


def outcome(won):
    """The result of a game, as a panel value."""
    return paint("win", GREEN) if won else paint("loss", RED)


def seconds(value):
    """A duration in seconds, with the precision a demo needs."""
    return f"{value:.3f} s"
