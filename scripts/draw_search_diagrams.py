"""Draw the graph-search diagrams of lecture 2 in the style of the course.

    uv run python scripts/draw_search_diagrams.py

Writes `figures/lec2/redundant.svg`, `astar-gone-wrong.svg` and `consistent-heuristic.svg`,
replacing the screenshots of the graph-search sequence. Same palette as the diagrams of the
exercise sheets: dark ink, the course blue as accent, a muted red for what is wrong. Nodes sit
at explicit coordinates, edges are straight or quadratic curves, and Roboto is embedded from
`assets/fonts/`, since an SVG shown as an image cannot load fonts from the page.
"""

import base64
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent

BLUE = "#356aaf"
INK = "#2a2a2a"
GREY = "#555555"
RED = "#c8463d"
FILL = "#e7eef7"

R = 34          # node radius
STROKE = 2.0


def fonts():
    faces = []
    for family, weight, name in [("Roboto", 400, "Roboto-400-latin"), ("Roboto", 900, "Roboto-900-latin")]:
        data = base64.b64encode((ROOT / "assets" / "fonts" / f"{name}.woff2").read_bytes()).decode()
        faces.append(f"@font-face {{ font-family: '{family}'; font-weight: {weight}; "
                     f"src: url(data:font/woff2;base64,{data}) format('woff2'); }}")
    return "<style>" + " ".join(faces) + "</style>"


def text(x, y, words, size=21, weight=400, fill=INK, anchor="middle", style=""):
    return (f'<text x="{x:g}" y="{y + 0.35 * size:.1f}" font-family="Roboto, sans-serif" font-weight="{weight}" '
            f'font-size="{size:g}" fill="{fill}" text-anchor="{anchor}"{style}>{escape(words)}</text>')


def node(x, y, name, r=R, fill=FILL):
    return (f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" fill="{fill}" stroke="{INK}" stroke-width="{STROKE}"/>'
            + text(x, y, name, size=26, weight=900))


def dot(x, y, r=16):
    return f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" fill="#b9b9b9" stroke="{INK}" stroke-width="1.6"/>'


def shorten(p, q, d):
    """Move `p` towards `q` by `d`, so that an edge stops at the border of a node."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    length = (dx * dx + dy * dy) ** 0.5
    return p[0] + dx / length * d, p[1] + dy / length * d


def edge(p, q, label=None, colour=INK, dashed=False, gap=R, label_side=1, tip="tip"):
    a, b = shorten(p, q, gap), shorten(q, p, gap + 6)
    style = ' stroke-dasharray="4 7" stroke-linecap="round"' if dashed else ""
    out = (f'<path d="M {a[0]:g} {a[1]:g} L {b[0]:g} {b[1]:g}" stroke="{colour}" stroke-width="{STROKE}" '
           f'fill="none"{style} marker-end="url(#{tip})"/>')
    if label is not None:
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        nx, ny = -(b[1] - a[1]), b[0] - a[0]
        n = (nx * nx + ny * ny) ** 0.5
        out += text(mx + nx / n * 22 * label_side, my + ny / n * 22 * label_side, label, size=23, fill=GREY)
    return out


def svg(name, width, height, parts):
    markers = "".join(
        f'<marker id="{i}" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" '
        f'markerWidth="11" markerHeight="11" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="{c}"/></marker>'
        for i, c in [("tip", INK), ("tipblue", BLUE), ("tipred", RED)])
    out = ROOT / "figures" / "lec2" / f"{name}.svg"
    out.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" '
                   f'height="{height}"><defs>{fonts()}{markers}</defs>{"".join(parts)}</svg>\n', encoding="utf-8")
    print(f"{out.relative_to(ROOT)}  {width}x{height}")


def redundant():
    """Four states with two ways between consecutive ones, and the tree they unfold into.

    The point is countable: the state space stays small while the number of paths doubles at
    every level, which is what a search that does not detect repeated states explores.
    """
    parts, r = [], 16

    def curve(x0, y0, x1, y1, bulge):
        mx, my = (x0 + x1) / 2 + bulge, (y0 + y1) / 2
        return (f'<path d="M {x0:g} {y0:g} Q {mx:g} {my:g} {x1:g} {y1:g}" stroke="{INK}" '
                f'stroke-width="{STROKE}" fill="none" marker-end="url(#tip)"/>')

    def segment(x0, y0, x1, y1):
        return f'<path d="M {x0:g} {y0:g} L {x1:g} {y1:g}" stroke="{INK}" stroke-width="2" fill="none"/>'

    rows = [48, 160, 272, 384]

    # left: the state space, two edges between consecutive states
    xs = 210
    for name, y in zip("ABCD", rows):
        parts += [text(xs - 120, y, name, size=27, weight=900), dot(xs, y)]
    for top, bottom in zip(rows, rows[1:]):
        parts.append(curve(xs - 7, top + r - 2, xs - 9, bottom - r + 1, -58))
        parts.append(curve(xs + 7, top + r - 2, xs + 9, bottom - r + 1, 58))
    parts.append(text(xs, rows[-1] + 58, "4 states, 6 edges", size=23, fill=GREY))

    # right: every level doubles, so there are 2^3 = 8 paths from A to D
    levels = [[790], [650, 930], [580, 720, 860, 1000], []]
    for x in levels[2]:
        levels[3] += [x - 35, x + 35]
    for depth, (xsr, y) in enumerate(zip(levels, rows)):
        for x in xsr:
            parts.append(dot(x, y))
        if depth:
            for x in xsr:
                parent = min(levels[depth - 1], key=lambda px: abs(px - x))
                parts.append(segment(parent, rows[depth - 1] + r - 1, x, y - r + 1))
    for name, y in zip("ABCD", rows):
        parts.append(text(500, y, name, size=27, weight=900))
    parts.append(text(790, rows[-1] + 58, "8 paths from A to D", size=23, fill=GREY))
    return parts


def gone_wrong():
    """S to G with an admissible but inconsistent h: C is closed too early, through B."""
    S, A, B, C, G = (80, 170), (300, 70), (250, 330), (470, 190), (470, 450)
    return [
        edge(S, A, "1"), edge(S, B, "1", label_side=-1), edge(A, C, "1"),
        edge(B, C, "2", label_side=-1), edge(C, G, "3"),
        node(*S, "S"), node(*A, "A"), node(*B, "B"), node(*C, "C"), node(*G, "G"),
        text(S[0] - 6, S[1] + 48, "h = 2", size=23, fill=BLUE),
        text(A[0], A[1] - 44, "h = 4", size=23, fill=BLUE),
        text(B[0] - 4, B[1] + 48, "h = 1", size=23, fill=BLUE),
        text(C[0] + 70, C[1], "h = 1", size=23, fill=BLUE),
        text(G[0] + 70, G[1], "h = 0", size=23, fill=BLUE),
    ]


def consistent():
    """The triangle inequality: h(A) must not exceed c(A, a, C) + h(C)."""
    A, C, G = (115, 80), (330, 190), (330, 450)
    return [
        edge(A, C, "1", colour=BLUE, tip="tipblue"),
        edge(C, G, "3"),
        edge(A, G, None, colour=RED, dashed=True, tip="tipred"),
        node(*A, "A"), node(*C, "C"), node(*G, "G"),
        text(A[0] - 44, A[1] + 46, "h = 4", size=23, fill=RED, anchor="end"),
        f'<path d="M {A[0] - 96:g} {A[1] + 46:g} L {A[0] - 38:g} {A[1] + 46:g}" stroke="{RED}" stroke-width="2"/>',
        text(A[0] - 44, A[1] + 80, "h = 2", size=23, fill=BLUE, anchor="end"),
        text(C[0] + 72, C[1], "h = 1", size=23, fill=BLUE),
        text(G[0] + 72, G[1], "h = 0", size=23, fill=BLUE),
    ]


if __name__ == "__main__":
    svg("redundant", 1120, 470, redundant())
    svg("astar-gone-wrong", 600, 545, gone_wrong())
    svg("consistent-heuristic", 450, 535, consistent())
