"""Terminal output of the demo: banner, messages and framed titles."""

LOGO = r"""
 _ __   __ _  ___ _ __ ___   __ _ _ __
| '_ \ / _` |/ __| '_ ` _ \ / _` | '_ \
| |_) | (_| | (__| | | | | | (_| | | | |
| .__/ \__,_|\___|_| |_| |_|\__,_|_| |_|
| |
|_|
"""


def display(message):
    """Print `message`, followed by a blank line."""
    print(message + "\n")


def display_PACMANLOGO():
    """Print the Pacman banner."""
    print(LOGO)


def display_b(message):
    """Print `message` between two rules of its own width."""
    rule = "-" * len(message)

    print()
    print(rule)
    print(message)
    print(rule)
