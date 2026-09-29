"""Draw the game trees of lecture 3 in the style of the course.

    uv run python scripts/draw_game_trees.py

Writes `figures/lec3/minimax-tree-1.svg` to `minimax-tree-3.svg`, the two-ply game tree of
Russell and Norvig (Figure 5.2) with its minimax values backed up one level at a time: the
leaves only, then the MIN nodes, then the root and the move of MAX. Same shapes as the game
trees of exercise sheet 2: MAX nodes are triangles pointing up, MIN nodes triangles pointing
down, terminal states boxes, backed-up values in the course blue. Roboto is embedded from
`assets/fonts/`, since an SVG shown as an image cannot load fonts from the page.
"""

import base64
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent

BLUE = "#356aaf"
INK = "#2a2a2a"
GREY = "#555555"
FILL = "#e7eef7"

STROKE = 2.0
HALF = 38       # half the base of a triangle
TOP, BOTTOM = 36, 26   # apex and base offsets from the centre of a triangle
LEAF = (60, 46)        # width and height of a terminal box


def fonts():
    faces = []
    for family, weight, name in [("Roboto", 400, "Roboto-400-latin"), ("Roboto", 900, "Roboto-900-latin")]:
        data = base64.b64encode((ROOT / "assets" / "fonts" / f"{name}.woff2").read_bytes()).decode()
        faces.append(f"@font-face {{ font-family: '{family}'; font-weight: {weight}; "
                     f"src: url(data:font/woff2;base64,{data}) format('woff2'); }}")
    return "<style>" + " ".join(faces) + "</style>"


def text(x, y, words, size=24, weight=400, fill=INK, anchor="middle", style=""):
    return (f'<text x="{x:g}" y="{y + 0.35 * size:.1f}" font-family="Roboto, sans-serif" font-weight="{weight}" '
            f'font-size="{size:g}" fill="{fill}" text-anchor="{anchor}"{style}>{escape(words)}</text>')


def action(x, y, index, fill):
    """The label a_i of an edge, in italics with a subscript."""
    return (f'<text x="{x:g}" y="{y + 8:.1f}" font-family="Roboto, sans-serif" font-size="24" fill="{fill}" '
            f'text-anchor="middle" font-style="italic">a<tspan font-size="17" dy="6">{index}</tspan></text>')


def triangle(x, y, up, value=None):
    """A MAX node (up) or a MIN node (down), centred at (x, y), with its value inside."""
    s = -1 if up else 1
    apex, base = (x, y + s * TOP), y - s * BOTTOM
    points = f"{apex[0]:g},{apex[1]:g} {x - HALF:g},{base:g} {x + HALF:g},{base:g}"
    out = f'<polygon points="{points}" fill="{FILL}" stroke="{INK}" stroke-width="{STROKE}" stroke-linejoin="round"/>'
    if value is not None:
        out += text(x, y - s * 6, str(value), size=26, weight=900, fill=BLUE)
    return out


def leaf(x, y, value):
    w, h = LEAF
    return (f'<rect x="{x - w / 2:g}" y="{y - h / 2:g}" width="{w:g}" height="{h:g}" fill="white" '
            f'stroke="{INK}" stroke-width="{STROKE}"/>' + text(x, y, str(value), size=26))


def line(p, q, colour=INK, width=STROKE):
    return (f'<path d="M {p[0]:g} {p[1]:g} L {q[0]:g} {q[1]:g}" stroke="{colour}" stroke-width="{width:g}" '
            f'stroke-linecap="round" fill="none"/>')


def svg(name, width, height, parts):
    out = ROOT / "figures" / "lec3" / f"{name}.svg"
    out.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" '
                   f'height="{height}"><defs>{fonts()}</defs>{"".join(parts)}</svg>\n', encoding="utf-8")
    print(f"{out.relative_to(ROOT)}  {width}x{height}")


LEAVES = [[3, 12, 8], [2, 4, 6], [14, 5, 2]]


def minimax_tree(step):
    """The two-ply tree after `step` levels are known: 1 the leaves, 2 the MIN nodes, 3 the root."""
    rows = {"MAX": 58, "MIN": 198, "leaves": 345}
    xs = [300, 560, 820]
    root = (560, rows["MAX"])
    parts = [text(110, y, label, size=24, fill=GREY, anchor="end") for label, y in
             [("MAX", rows["MAX"]), ("MIN", rows["MIN"]), ("utility", rows["leaves"])]]

    mins = [min(v) for v in LEAVES]
    best = max(range(3), key=lambda i: mins[i])

    # edges first, so that the nodes are drawn over them
    for i, x in enumerate(xs):
        chosen = step >= 3 and i == best
        parts.append(line((root[0], root[1] + BOTTOM), (x, rows["MIN"] - BOTTOM),
                          colour=BLUE if chosen else INK, width=4 if chosen else STROKE))
        mx, my = (root[0] + x) / 2, (root[1] + BOTTOM + rows["MIN"] - BOTTOM) / 2
        dx, dy = {-1: (-30, -16), 0: (24, 0), 1: (30, -16)}[(x > root[0]) - (x < root[0])]
        parts.append(action(mx + dx, my + dy, i + 1, BLUE if chosen else GREY))
        for j in range(3):
            lx = x + (j - 1) * 82
            parts.append(line((x, rows["MIN"] + TOP), (lx, rows["leaves"] - LEAF[1] / 2)))

    parts.append(triangle(*root, up=True, value=mins[best] if step >= 3 else None))
    for i, x in enumerate(xs):
        parts.append(triangle(x, rows["MIN"], up=False, value=mins[i] if step >= 2 else None))
        for j in range(3):
            parts.append(leaf(x + (j - 1) * 82, rows["leaves"], LEAVES[i][j]))
    return parts


if __name__ == "__main__":
    for step in (1, 2, 3):
        svg(f"minimax-tree-{step}", 960, 380, minimax_tree(step))
