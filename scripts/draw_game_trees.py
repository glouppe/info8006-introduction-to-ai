"""Draw the game trees of lecture 3 in the style of the course.

    uv run python scripts/draw_game_trees.py

Writes `figures/lec3/minimax-tree-1.svg` to `minimax-tree-3.svg`, the two-ply game tree of
Russell and Norvig (Figure 5.2) with its minimax values backed up one level at a time: the
leaves only, then the MIN nodes, then the root and the move of MAX. Same shapes as the game
trees of exercise sheet 2: MAX nodes are triangles pointing up, MIN nodes triangles pointing
down, terminal states boxes, backed-up values in the course blue. Roboto is embedded from
`assets/fonts/`, since an SVG shown as an image cannot load fonts from the page.

Also writes `minimax-pruned.svg` (the same tree with two unknown leaves), `alpha-beta-1.svg` to
`alpha-beta-6.svg` (the steps of alpha-beta pruning on it, Figure 5.5, unexplored parts faded and
the interval of possible values beside each node), `alpha-beta-path.svg` (Figure 5.6) and
`horizon-1.svg`, `horizon-2.svg` (a search cut at depth 2, then what lies beyond its horizon),
`stochastic-game-tree.svg` (backgammon, Figure 5.11) and `chance-order-preserving.svg`
(Figure 5.12, without its MIN nodes, which only repeat their leaves), and `multi-agent-tree-1.svg`,
`multi-agent-tree-2.svg` (three players and their utility vectors, then the vectors backed up), and
`mcts-1.svg` to `mcts-4.svg` (one round of Monte Carlo tree search, after Wikipedia).
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
        out += text(x, y - s * 6, str(value).replace("-", "\u2212"), size=26, weight=900, fill=BLUE)
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


FADED = "#b5b5b5"
DASH = ' stroke-dasharray="6 6"'

LEAVES = [[3, 12, 8], [2, 4, 6], [14, 5, 2]]
ROWS = {"MAX": 58, "MIN": 198, "leaves": 345}
XS = [300, 560, 820]
SPREAD = 82


def faded_triangle(x, y, up):
    s = -1 if up else 1
    apex, base = (x, y + s * TOP), y - s * BOTTOM
    points = f"{apex[0]:g},{apex[1]:g} {x - HALF:g},{base:g} {x + HALF:g},{base:g}"
    return (f'<polygon points="{points}" fill="white" stroke="{FADED}" stroke-width="{STROKE}" '
            f'stroke-linejoin="round"{DASH}/>')


def faded_leaf(x, y):
    w, h = LEAF
    return (f'<rect x="{x - w / 2:g}" y="{y - h / 2:g}" width="{w:g}" height="{h:g}" fill="white" '
            f'stroke="{FADED}" stroke-width="{STROKE}"{DASH}/>')


def faded_line(p, q):
    return (f'<path d="M {p[0]:g} {p[1]:g} L {q[0]:g} {q[1]:g}" stroke="{FADED}" stroke-width="{STROKE}" '
            f'fill="none"{DASH}/>')


def two_ply(leaves, seen=None, values=None, intervals=None, best=None, labels=("MAX", "MIN", "utility"),
            named=False):
    """The two-ply tree of Russell and Norvig.

    `leaves` gives the 9 leaf labels (a number, or a letter for an unknown value). Only the leaves
    in `seen` (indices 0 to 8, all by default) are drawn solid; a MIN node is solid once one of its
    leaves is seen, and the root once a MIN node is. `values` maps a node ("A", "B", "C", "D") to
    the value written inside it, `intervals` to the interval of possible values written beside it.
    `best` is the index of the move of MAX to highlight, and `named` writes the names of the nodes
    A to D beside them.
    """
    seen = set(range(9)) if seen is None else set(seen)
    values, intervals = values or {}, intervals or {}
    root = (560, ROWS["MAX"])
    names = "BCD"
    parts = [text(110, y, label, size=24, fill=GREY, anchor="end")
             for label, y in zip(labels, ROWS.values())]

    open_min = [any(3 * i + j in seen for j in range(3)) for i in range(3)]

    for i, x in enumerate(XS):
        top, bottom = (root[0], root[1] + BOTTOM), (x, ROWS["MIN"] - BOTTOM)
        if open_min[i]:
            chosen = best == i
            parts.append(line(top, bottom, colour=BLUE if chosen else INK, width=4 if chosen else STROKE))
        else:
            parts.append(faded_line(top, bottom))
        mx, my = (root[0] + x) / 2, (root[1] + BOTTOM + ROWS["MIN"] - BOTTOM) / 2
        dx, dy = {-1: (-30, -16), 0: (24, 0), 1: (30, -16)}[(x > root[0]) - (x < root[0])]
        parts.append(action(mx + dx, my + dy, i + 1, BLUE if best == i else (GREY if open_min[i] else FADED)))
        for j in range(3):
            p, q = (x, ROWS["MIN"] + TOP), (x + (j - 1) * SPREAD, ROWS["leaves"] - LEAF[1] / 2)
            parts.append(line(p, q) if 3 * i + j in seen else faded_line(p, q))

    parts.append(triangle(*root, up=True, value=values.get("A")) if any(open_min)
                 else faded_triangle(*root, up=True))
    if named:
        parts.append(text(root[0] + HALF + 10, root[1] + 4, "A", size=24, weight=900,
                          fill=INK if any(open_min) else FADED, anchor="start"))
    if "A" in intervals:
        parts.append(text(root[0] - HALF - 12, root[1] + 4, intervals["A"], size=24, fill=BLUE, anchor="end"))
    for i, x in enumerate(XS):
        name = names[i]
        parts.append(triangle(x, ROWS["MIN"], up=False, value=values.get(name)) if open_min[i]
                     else faded_triangle(x, ROWS["MIN"], up=False))
        if named:
            parts.append(text(x + HALF + 10, ROWS["MIN"] - 6, name, size=24, weight=900,
                              fill=INK if open_min[i] else FADED, anchor="start"))
        if name in intervals:
            parts.append(text(x - HALF - 12, ROWS["MIN"] - 6, intervals[name], size=24, fill=BLUE, anchor="end"))
        for j in range(3):
            k, lx = 3 * i + j, x + (j - 1) * SPREAD
            if k not in seen:
                parts.append(faded_leaf(lx, ROWS["leaves"]))
            elif isinstance(leaves[k], str):
                parts.append(leaf(lx, ROWS["leaves"], "")
                             + text(lx, ROWS["leaves"], leaves[k], size=26, fill=GREY, style=' font-style="italic"'))
            else:
                parts.append(leaf(lx, ROWS["leaves"], leaves[k]))
    return parts


def minimax_tree(step):
    """The tree after `step` levels are known: 1 the leaves, 2 the MIN nodes, 3 the root and a1."""
    flat = [v for row in LEAVES for v in row]
    mins = [min(v) for v in LEAVES]
    values = dict(zip("BCD", mins)) if step >= 2 else {}
    if step >= 3:
        values["A"] = max(mins)
    return two_ply(flat, values=values, best=0 if step >= 3 else None)


def pruned_tree():
    """The tree with the two unknown leaves x and y of C, whose values do not matter."""
    return two_ply([3, 12, 8, 2, "x", "y", 14, 5, 2], best=0, named=True)


INF = "∞"
ALPHA_BETA = [   # leaves seen, intervals, move of MAX, as in Figure 5.5 of Russell and Norvig
    ({0}, {"A": f"[−{INF}, +{INF}]", "B": f"[−{INF}, 3]"}, None),
    ({0, 1}, {"A": f"[−{INF}, +{INF}]", "B": f"[−{INF}, 3]"}, None),
    ({0, 1, 2}, {"A": f"[3, +{INF}]", "B": "[3, 3]"}, None),
    ({0, 1, 2, 3}, {"A": f"[3, +{INF}]", "B": "[3, 3]", "C": f"[−{INF}, 2]"}, None),
    ({0, 1, 2, 3, 6}, {"A": "[3, 14]", "B": "[3, 3]", "C": f"[−{INF}, 2]", "D": f"[−{INF}, 14]"}, None),
    ({0, 1, 2, 3, 6, 7, 8}, {"A": "[3, 3]", "B": "[3, 3]", "C": f"[−{INF}, 2]", "D": "[2, 2]"}, 0),
]


def alpha_beta_tree(step):
    seen, intervals, best = ALPHA_BETA[step - 1]
    flat = [3, 12, 8, 2, "x", "y", 14, 5, 2]
    return two_ply(flat, seen=seen, intervals=intervals, best=best, named=True)


def alpha_path():
    """A MIN node n deep in the tree, and the value alpha of a MAX choice m higher on its path."""
    rows = [60, 175, 360, 470]
    parts = [text(125, y, label, size=32, fill=GREY, anchor="end")
             for label, y in zip(["MAX", "MIN", "MAX", "MIN"], rows)]
    top = (420, rows[0])
    m = (250, rows[1])
    low = (360, rows[2])
    n = (470, rows[3])
    parts.append(line((top[0] + 60, top[1] - 60), (top[0], top[1] - TOP)))
    parts.append(line((top[0], top[1] + BOTTOM), (m[0], m[1] - BOTTOM)))
    parts.append(line((top[0] + 20, top[1] + BOTTOM), (top[0] + 70, top[1] + 60)))
    for dx in (-60, 0, 60):
        parts.append(line((m[0], m[1] + TOP), (m[0] + dx, m[1] + 90)))
    # the wavy path from the MAX node down to the lower MAX node
    x0, y0, y1 = top[0], top[1] + BOTTOM, low[1] - TOP
    d = f"M {x0} {y0}"
    k = 4
    for i in range(k):
        ya, yb = y0 + (y1 - y0) * i / k, y0 + (y1 - y0) * (i + 1) / k
        side = 30 if i % 2 == 0 else -30
        d += f" Q {x0 + side} {(ya + yb) / 2:g} {x0 - (low[0] - x0) * 0 + (low[0] - x0) * (i + 1) / k:g} {yb:g}"
    parts.append(f'<path d="{d}" stroke="{INK}" stroke-width="{STROKE}" fill="none" stroke-dasharray="7 6"/>')
    parts.append(line((low[0] - 20, low[1] + BOTTOM), (low[0] - 70, low[1] + 60)))
    parts.append(line((low[0] + 5, low[1] + BOTTOM), (n[0], n[1] - BOTTOM)))
    for dx in (-50, 50):
        parts.append(line((n[0], n[1] + TOP), (n[0] + dx, n[1] + 75)))
    parts.append(triangle(*top, up=True))
    parts.append(triangle(*m, up=False))
    parts.append(triangle(*low, up=True))
    parts.append(triangle(*n, up=False))
    parts.append(text(m[0], m[1] - 6, "m", size=30, weight=900, fill=INK, style=' font-style="italic"'))
    parts.append(text(n[0], n[1] - 6, "n", size=30, weight=900, fill=INK, style=' font-style="italic"'))
    parts.append(text(m[0] + HALF + 14, m[1] - 4, "α", size=42, fill=BLUE, anchor="start"))
    parts.append(text(95, (rows[1] + rows[2]) / 2, "⋮", size=40, fill=GREY, anchor="middle"))
    return parts


RED = "#c8463d"


def horizon_tree(step):
    """A search cut at depth 2, and what lies beyond its horizon.

    Step 1: the evaluation at the cutoff makes a1 look best (5 against 0). Step 2: the values
    beyond the horizon show that a1 loses (-9) and that a2 (0) was the right move.
    """
    rows = {"MAX": 50, "MIN": 165, "eval": 285, "beyond": 405}
    horizon = 340
    root = (480, rows["MAX"])
    xs = [300, 660]
    evals = [[5, 6], [0, 1]]
    truth = [[-9, -8], [0, 1]]
    parts = [text(110, rows[k], label, size=24, fill=GREY, anchor="end")
             for k, label in [("MAX", "MAX"), ("MIN", "MIN"), ("eval", "eval"),
                              ("beyond", "true value" if step >= 2 else "")]]
    parts.append(f'<path d="M 125 {horizon} L 900 {horizon}" stroke="{BLUE}" stroke-width="2.5" '
                 f'stroke-dasharray="10 8" fill="none"/>')
    parts.append(text(110, horizon, "horizon", size=24, fill=BLUE, anchor="end"))

    mins = [min(v) for v in (evals if step == 1 else truth)]
    best = max(range(2), key=lambda i: mins[i])
    for i, x in enumerate(xs):
        chosen = i == best
        parts.append(line((root[0], root[1] + BOTTOM), (x, rows["MIN"] - BOTTOM),
                          colour=BLUE if chosen else INK, width=4 if chosen else STROKE))
        mx, my = (root[0] + x) / 2, (root[1] + BOTTOM + rows["MIN"] - BOTTOM) / 2
        parts.append(action(mx + (-30 if x < root[0] else 30), my - 14, i + 1, BLUE if chosen else GREY))
        for j in range(2):
            cx = x + (j - 0.5) * 150
            parts.append(line((x, rows["MIN"] + TOP), (cx, rows["eval"] - LEAF[1] / 2)))
            p, q = (cx, rows["eval"] + LEAF[1] / 2), (cx, rows["beyond"] - LEAF[1] / 2)
            parts.append(faded_line(p, q))
    parts.append(triangle(*root, up=True, value=max(mins)))
    for i, x in enumerate(xs):
        parts.append(triangle(x, rows["MIN"], up=False, value=mins[i]))
        for j in range(2):
            cx = x + (j - 0.5) * 150
            parts.append(leaf(cx, rows["eval"], evals[i][j]))
            if step == 1:
                parts.append(faded_leaf(cx, rows["beyond"]) + text(cx, rows["beyond"], "?", size=26, fill=FADED))
            else:
                v = truth[i][j]
                parts.append(leaf(cx, rows["beyond"], "") +
                             text(cx, rows["beyond"], str(v).replace("-", "\u2212"), size=26, weight=900,
                                  fill=RED if v < 0 else INK))
    return parts


CHANCE_R = 22


def chance(x, y, value=None, side=1):
    """A chance node, a white circle, with its value in blue beside it."""
    out = (f'<circle cx="{x:g}" cy="{y:g}" r="{CHANCE_R}" fill="white" stroke="{INK}" '
           f'stroke-width="{STROKE}"/>')
    if value is not None:
        out += text(x + side * (CHANCE_R + 10), y, str(value), size=24, weight=900, fill=BLUE,
                    anchor="start" if side > 0 else "end")
    return out


def stub(x, y):
    """The first moves below a node that is not expanded, and an ellipsis."""
    return "".join(line((x, y), (x + dx, y + 26), width=1.4) for dx in (-14, 0, 14))


def dice(x, y, p, roll):
    """The probability and the roll of a dice outcome, on an edge."""
    halo = ' stroke="white" stroke-width="6" stroke-linejoin="round" paint-order="stroke"'
    return text(x, y - 13, p, size=20, fill=GREY, style=halo) + text(x, y + 13, roll, size=20, fill=GREY, style=halo)


def stochastic_tree():
    """Backgammon, Figure 5.11 of Russell and Norvig: chance nodes roll the dice before each move."""
    rows = [45, 160, 305, 440, 580, 700]
    parts = [text(150, y, label, size=22, fill=GREY, anchor="end")
             for label, y in zip(["MAX", "CHANCE", "MIN", "CHANCE", "MAX", "TERMINAL"], rows)]
    root = (560, rows[0])

    c1 = [260, 400, 560, 800, 920]      # chance nodes after the move of MAX, the third expanded
    m1 = [300, 470, 700, 880]           # MIN nodes after the roll, the third expanded
    c2 = [480, 660, 820, 920]           # chance nodes after the move of MIN, the first expanded
    m2 = [230, 380, 560, 740]           # MAX nodes after the roll, the third expanded
    leaves = [(420, "2"), (490, "\u22121"), (560, "1"), (690, "\u22121"), (760, "1")]

    for x in c1:
        parts.append(line((root[0], root[1] + BOTTOM), (x, rows[1] - CHANCE_R)))
    parts.append(text(680, rows[1], "\u2026", size=30, fill=GREY))
    for x, (p, roll) in zip(m1, [("1/36", "1,1"), ("1/18", "1,2"), ("1/18", "6,5"), ("1/36", "6,6")]):
        parts.append(line((560, rows[1] + CHANCE_R), (x, rows[2] - BOTTOM)))
        mx, my = 560 + 0.62 * (x - 560), rows[1] + CHANCE_R + 0.62 * (rows[2] - BOTTOM - rows[1] - CHANCE_R)
        parts.append(dice(mx + (-32 if x < 560 else 32), my, p, roll))
    parts.append(text(585, rows[2], "\u2026", size=30, fill=GREY))
    for x in c2:
        parts.append(line((700, rows[2] + TOP), (x, rows[3] - CHANCE_R)))
    parts.append(text(740, rows[3], "\u2026", size=30, fill=GREY))
    for x, (p, roll) in zip(m2, [("1/36", "1,1"), ("1/18", "1,2"), ("1/18", "6,5"), ("1/36", "6,6")]):
        parts.append(line((480, rows[3] + CHANCE_R), (x, rows[4] - TOP)))
        mx, my = 480 + 0.62 * (x - 480), rows[3] + CHANCE_R + 0.62 * (rows[4] - TOP - rows[3] - CHANCE_R)
        parts.append(dice(mx + (-32 if x < 480 else 32), my, p, roll))
    parts.append(text(470, rows[4], "\u2026", size=30, fill=GREY))
    for x, _ in leaves:
        parts.append(line((560, rows[4] + BOTTOM), (x, rows[5] - LEAF[1] / 2)))
    parts.append(text(625, rows[5], "\u2026", size=30, fill=GREY))

    parts.append(triangle(*root, up=True))
    for x in c1:
        parts.append(chance(x, rows[1]))
        if x != 560:
            parts.append(stub(x, rows[1] + CHANCE_R))
    for x in m1:
        parts.append(triangle(x, rows[2], up=False))
        if x != 700:
            parts.append(stub(x, rows[2] + TOP))
    for x in c2:
        parts.append(chance(x, rows[3]))
        if x != 480:
            parts.append(stub(x, rows[3] + CHANCE_R))
    for x in m2:
        parts.append(triangle(x, rows[4], up=True))
        if x != 560:
            parts.append(stub(x, rows[4] + BOTTOM))
    for x, v in leaves:
        parts.append(leaf(x, rows[5], "") + text(x, rows[5], v, size=24))
    return parts


def order_preserving():
    """Figure 5.12 of Russell and Norvig, without its MIN nodes, which only repeat their leaves:
    the transformation 1, 2, 3, 4 -> 1, 20, 30, 400 keeps the order of the leaves but changes the move."""
    rows = {"MAX": 45, "CHANCE": 175, "utility": 320}
    parts = [text(110, y, label, size=22, fill=GREY, anchor="end") for label, y in rows.items()]
    for ox, leaves in [(0, [[2, 3], [1, 4]]), (440, [[20, 30], [1, 400]])]:
        root = (330 + ox, rows["MAX"])
        xs = [240 + ox, 420 + ox]
        values = [round(0.9 * a + 0.1 * b, 1) for a, b in leaves]
        best = max(range(2), key=lambda i: values[i])
        for i, x in enumerate(xs):
            chosen = i == best
            parts.append(line((root[0], root[1] + BOTTOM), (x, rows["CHANCE"] - CHANCE_R),
                              colour=BLUE if chosen else INK, width=4 if chosen else STROKE))
            mx, my = (root[0] + x) / 2, (root[1] + BOTTOM + rows["CHANCE"] - CHANCE_R) / 2
            parts.append(action(mx + (-26 if x < root[0] else 26), my - 12, i + 1, BLUE if chosen else GREY))
            for j, (dx, p) in enumerate([(-45, ".9"), (45, ".1")]):
                lx = x + dx
                parts.append(line((x, rows["CHANCE"] + CHANCE_R), (lx, rows["utility"] - LEAF[1] / 2)))
                parts.append(text((x + lx) / 2 + (-18 if dx < 0 else 18), (rows["CHANCE"] + rows["utility"]) / 2,
                                  p, size=20, fill=GREY))
                parts.append(leaf(lx, rows["utility"], leaves[i][j]))
        parts.append(triangle(*root, up=True))
        parts.append(text(root[0] + HALF + 12, root[1] + 4, f"{max(values):g}", size=24, weight=900,
                          fill=BLUE, anchor="start"))
        for i, x in enumerate(xs):
            parts.append(chance(x, rows["CHANCE"], f"{values[i]:g}", side=-1 if i == 0 else 1))
    return parts


PLAYER_COLOURS = ["#c8463d", "#356aaf", "#3d8a4f"]   # players 1, 2 and 3


def player(x, y, p):
    """A node of a multi-player game, a triangle in the colour of the player to move."""
    points = f"{x:g},{y - TOP:g} {x - HALF:g},{y + BOTTOM:g} {x + HALF:g},{y + BOTTOM:g}"
    return (f'<polygon points="{points}" fill="{PLAYER_COLOURS[p - 1]}" stroke="{INK}" stroke-width="{STROKE}" '
            f'stroke-linejoin="round"/>')


def vector(x, y, v, size=20, weight=400, anchor="middle"):
    """A utility vector, each component in the colour of its player."""
    spans = ", ".join(f'<tspan fill="{PLAYER_COLOURS[i]}">{c}</tspan>' for i, c in enumerate(v))
    return (f'<text x="{x:g}" y="{y + 0.35 * size:.1f}" font-family="Roboto, sans-serif" font-weight="{weight}" '
            f'font-size="{size:g}" fill="{INK}" text-anchor="{anchor}">({spans})</text>')


MULTI_LEAVES = [(1, 6, 6), (7, 1, 2), (6, 1, 2), (7, 2, 1), (5, 1, 7), (1, 5, 2), (7, 7, 1), (5, 2, 5)]


def multi_agent_tree(step):
    """Three players, each maximizing its own component: step 1 the leaves, step 2 the backed-up vectors."""
    rows = [50, 170, 290, 405]
    parts = [text(110, y, label, size=22, fill=PLAYER_COLOURS[i] if i < 3 else GREY, anchor="end")
             for i, (label, y) in enumerate(zip(["player 1", "player 2", "player 3", "utility"], rows))]
    lx = [190 + 108 * k for k in range(8)]
    p3 = [(lx[2 * k] + lx[2 * k + 1]) / 2 for k in range(4)]
    p2 = [(p3[0] + p3[1]) / 2, (p3[2] + p3[3]) / 2]
    root = ((p2[0] + p2[1]) / 2, rows[0])

    v3 = [max(MULTI_LEAVES[2 * k:2 * k + 2], key=lambda v: v[2]) for k in range(4)]
    v2 = [max(v3[2 * k:2 * k + 2], key=lambda v: v[1]) for k in range(2)]
    v1 = max(v2, key=lambda v: v[0])
    shown = step >= 2

    def link(p, q, chosen):
        return line(p, q, colour=INK, width=4.5 if chosen and shown else 1.6)

    for i, x in enumerate(p2):
        parts.append(link((root[0], root[1] + BOTTOM), (x, rows[1] - TOP), v2[i] == v1))
        for j in range(2):
            k = 2 * i + j
            parts.append(link((x, rows[1] + BOTTOM), (p3[k], rows[2] - TOP), v3[k] == v2[i]))
            for m in range(2):
                parts.append(link((p3[k], rows[2] + BOTTOM), (lx[2 * k + m], rows[3] - LEAF[1] / 2),
                                  MULTI_LEAVES[2 * k + m] == v3[k]))
    parts.append(player(*root, 1))
    if shown:
        parts.append(vector(root[0] + HALF + 12, root[1] + 4, v1, size=22, weight=900, anchor="start"))
    for i, x in enumerate(p2):
        parts.append(player(x, rows[1], 2))
        if shown:
            side = -1 if i == 0 else 1
            parts.append(vector(x + side * (HALF + 12), rows[1] + 4, v2[i], size=22, weight=900,
                                anchor="end" if side < 0 else "start"))
    for k, x in enumerate(p3):
        parts.append(player(x, rows[2], 3))
        if shown:
            side = -1 if k % 2 == 0 else 1
            parts.append(vector(x + side * 14, rows[2] - TOP - 4, v3[k], size=20, weight=900,
                                anchor="end" if side < 0 else "start"))
    for k, x in enumerate(lx):
        w, h = 92, LEAF[1]
        parts.append(f'<rect x="{x - w / 2:g}" y="{rows[3] - h / 2:g}" width="{w}" height="{h}" fill="white" '
                     f'stroke="{INK}" stroke-width="{STROKE}"/>' + vector(x, rows[3], MULTI_LEAVES[k]))
    return parts


MCTS_R = 36
DARK = "#c4c4c4"


def mcts_node(x, y, label, dark, highlight=False):
    colour = BLUE if highlight else INK
    return (f'<circle cx="{x:g}" cy="{y:g}" r="{MCTS_R}" fill="{DARK if dark else "white"}" stroke="{INK}" '
            f'stroke-width="{STROKE}"/>' + text(x, y, label, size=20, weight=900 if highlight else 400, fill=colour))


def arrow(p, q, colour=BLUE, width=3.5):
    """A straight edge from p to q, stopped at the border of the circles, with an arrow head at q."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    d = (dx * dx + dy * dy) ** 0.5
    a = (p[0] + dx / d * MCTS_R, p[1] + dy / d * MCTS_R)
    b = (q[0] - dx / d * (MCTS_R + 4), q[1] - dy / d * (MCTS_R + 4))
    ux, uy = dx / d, dy / d
    head = (f"{b[0]:g},{b[1]:g} {b[0] - 14 * ux + 7 * uy:g},{b[1] - 14 * uy - 7 * ux:g} "
            f"{b[0] - 14 * ux - 7 * uy:g},{b[1] - 14 * uy + 7 * ux:g}")
    return (line(a, (b[0] - 10 * ux, b[1] - 10 * uy), colour=colour, width=width)
            + f'<polygon points="{head}" fill="{colour}"/>')


def mcts_tree(step):
    """One round of Monte Carlo tree search: 1 selection, 2 expansion, 3 simulation, 4 backpropagation.
    As in the other trees, a node is coloured by the player to move in it, grey for Black and white for
    White, and every label counts Black's wins and visits, as minimax values are MAX's utility. The counts
    are chosen so that UCB1 with c = sqrt(2) selects the path drawn (Wikipedia's example does not)."""
    y = [50, 160, 270, 380, 490]
    nodes = {   # name: (x, level, dark, label before, label after backpropagation)
        "root": (560, 0, True, "11/21", "12/22"),
        "a": (300, 1, False, "8/10", "9/11"), "b": (620, 1, False, "3/8", None), "c": (780, 1, False, "0/3", None),
        "a1": (220, 2, True, "4/4", None), "a2": (380, 2, True, "4/6", "5/7"),
        "b1": (520, 2, True, "1/2", None), "b2": (620, 2, True, "1/3", None), "b3": (720, 2, True, "1/3", None),
        "a21": (300, 3, False, "1/3", None), "a22": (460, 3, False, "3/3", "4/4"),
    }
    parent = {"a": "root", "b": "root", "c": "root", "a1": "a", "a2": "a", "b1": "b", "b2": "b", "b3": "b",
              "a21": "a2", "a22": "a2"}
    path = ["root", "a", "a2", "a22"]
    new = (460, y[4])
    pos = {k: (v[0], y[v[1]]) for k, v in nodes.items()}

    parts = []
    for k, p in parent.items():
        on_path = step in (1, 4) and k in path
        if not on_path:
            parts.append(line(pos[p], pos[k], colour="#9a9a9a", width=1.6))
    if step == 1:
        for a, b in zip(path, path[1:]):
            parts.append(arrow(pos[a], pos[b]))
    if step >= 2:
        parts.append(arrow(pos["a22"], new) if step == 2 else line(pos["a22"], new, colour="#9a9a9a", width=1.6))
    if step == 3:
        x0, y0, y1 = new[0], new[1] + MCTS_R, new[1] + 105
        d, k = f"M {x0} {y0}", 4
        for i in range(k):
            ya, yb = y0 + (y1 - y0) * i / k, y0 + (y1 - y0) * (i + 1) / k
            d += f" Q {x0 + (14 if i % 2 == 0 else -14)} {(ya + yb) / 2:g} {x0} {yb:g}"
        parts.append(f'<path d="{d}" stroke="{BLUE}" stroke-width="3" fill="none"/>')
        parts.append(text(x0, y1 + 22, "Black wins", size=22, weight=900, fill=BLUE))
    if step == 4:
        parts.append(arrow(new, pos["a22"]))
        for a, b in zip(path, path[1:]):
            parts.append(arrow(pos[b], pos[a]))

    for k, (x, lvl, dark, before, after) in nodes.items():
        updated = step == 4 and after is not None
        parts.append(mcts_node(x, y[lvl], after if updated else before, dark, highlight=updated))
    if step >= 2:
        parts.append(mcts_node(*new, "1/1" if step == 4 else "0/0", True, highlight=step in (2, 4)))
    return ['<g transform="translate(-150, 0)">'] + parts + ["</g>"]


if __name__ == "__main__":
    for step in (1, 2, 3):
        svg(f"minimax-tree-{step}", 960, 380, minimax_tree(step))
    svg("minimax-pruned", 960, 380, pruned_tree())
    for step in range(1, 7):
        svg(f"alpha-beta-{step}", 960, 380, alpha_beta_tree(step))
    svg("alpha-beta-path", 620, 560, alpha_path())
    for step in (1, 2):
        svg(f"horizon-{step}", 960, 440, horizon_tree(step))
    svg("stochastic-game-tree", 1000, 740, stochastic_tree())
    svg("chance-order-preserving", 980, 360, order_preserving())
    for step in (1, 2):
        svg(f"multi-agent-tree-{step}", 1000, 440, multi_agent_tree(step))
    for step in range(1, 5):
        svg(f"mcts-{step}", 700, 640, mcts_tree(step))
