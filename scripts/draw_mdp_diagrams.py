"""Draw the diagrams of lecture 8 in the style of the course.

    uv run python scripts/draw_mdp_diagrams.py

Writes to `figures/lec8/`:

- `discounting.svg`, three steps of a run, each a state then the action taken in it, weighted by
  1, gamma and gamma^2, next to the gems of CS188 cropped from the former `discounting.png`;
- `fixed-policy.svg`, one step of a fixed policy: the state s, the action pi(s), the q-state
  (s, pi(s)) and the successors s';
- `policy-evaluation-tree.svg`, one step of the Bellman update: the state s, every action a, and the
  successors s' of the q-state (s, a);
- `optimal-policy-merge.svg`, the argument that the optimal policy does not depend on the starting
  state: the optimal policies of a and of b reach the same state c, where they choose the same action;
- `ddn-1.svg` to `ddn-3.svg`, a dynamic decision network unrolled up to t + 3 (Figure 17.10 of Russell
  and Norvig, 3rd edition), built in three steps: the dynamic Bayesian network of lecture 6, then the
  actions as squares, then the rewards and the utility at the horizon as diamonds; known values shaded;
- `pomdp-tree.svg`, part of the look-ahead search of that network (Figure 17.11), its rows labelled by
  the beliefs b_t of lecture 1 and the percepts.

Edges are arrows, their tips on the outline of the node they reach. States are triangles, q-states and chance nodes circles, as the MAX and chance nodes of lecture 3:
the trees of an MDP are those of expectimax. Nodes, strokes and fonts are those of
`draw_game_trees.py`; the network uses the circles of `draw_bn_diagrams.py`. The deck shows every
figure at about 0.9 px per unit on a 1280 px slide.
"""

import base64
import io

from PIL import Image

from draw_game_trees import (BLUE, BOTTOM, CHANCE_R, FILL, GREY, HALF, INK, LEAF, ROOT, STROKE, TOP, chance,
                             fonts, leaf, line, text, triangle)

OUT = ROOT / "figures" / "lec8"
FADED = "#b5b5b5"
ORANGE = "#d9822b"
R = 36   # the radius of a variable of the network


# ---- typesetting

def span(t, kind):
    """A piece of mathematics: "i" italic letters, "b" bold upright (\\mathbf), "r" roman, "w" a word."""
    if kind == "w":
        return f'<tspan font-family="Roboto, sans-serif">{t}</tspan>'
    if kind == "b":
        return f'<tspan font-family="KaTeX_Main" font-weight="700">{t}</tspan>'
    out = ""
    for c in t:
        italic = kind == "i" and (c.isalpha() and (c.isascii() or c.islower()))
        out += f'<tspan font-family="{"KaTeX_Math" if italic else "KaTeX_Main"}">{c}</tspan>'
    return out


def formula(x, y, pieces, size=24, fill=INK, anchor="middle"):
    """A formula from (text, kind) pieces; kind "_" or "^" sets the next pieces as a subscript or
    superscript until a piece of kind "." returns to the baseline; kind "′" is a prime, and kind "^_" a
    superscript stacked over a subscript, as LaTeX sets π^*_a."""
    # A vertical shift is carried by the next characters written: browsers ignore dy on an empty tspan.
    spans, level, pending = "", 0.0, 0.0
    small = 0.7 * size

    def emit(content, font_size=None, dx=None, family=None):
        nonlocal spans, pending
        attrs = f' font-size="{font_size:g}"' if font_size else ""
        attrs += f' font-family="{family}"' if family else ""
        attrs += f' dx="{dx:g}"' if dx else ""
        attrs += f' dy="{pending:g}"' if pending else ""
        spans += f"<tspan{attrs}>{content}</tspan>"
        pending = 0.0

    for t, kind in pieces:
        if kind == "′":
            pending -= 0.38 * size
            emit("′", font_size=0.75 * size, family="KaTeX_Main")
            pending += 0.38 * size
        elif kind == "^_":
            sup, sub = t
            pending -= 0.38 * size
            emit(span(sup, "r"), font_size=small)
            pending += 0.63 * size
            emit(span(sub, "i"), font_size=small, dx=-0.5 * small)
            pending -= 0.25 * size
        elif kind in "_^":
            target = 0.25 * size if kind == "_" else -0.38 * size
            pending += target - level
            level = target
            if t:
                emit(span(t, "i"), font_size=small)
        elif kind == ".":
            pending -= level
            level = 0.0
        else:
            emit(span(t, kind), font_size=small if level else None)
    return (f'<text x="{x:g}" y="{y + 0.3 * size:.1f}" font-size="{size:g}" fill="{fill}" '
            f'text-anchor="{anchor}" xml:space="preserve">{spans}</text>')


def svg(name, width, height, parts, x0=0):
    heads = "".join(
        f'<marker id="head-{key}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" '
        f'orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="{colour}"/></marker>'
        for key, colour in COLOURS.items())
    out = OUT / f"{name}.svg"
    out.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} 0 {width} {height}" width="{width}" '
                   f'height="{height}"><defs>{fonts()}{heads}</defs>{"".join(parts)}</svg>\n', encoding="utf-8")
    print(f"{out.relative_to(ROOT)}  {width}x{height}")


COLOURS = {"ink": INK, "blue": BLUE, "orange": ORANGE, "faded": FADED}


def arrow(p, q, colour="ink", width=STROKE, dash=""):
    """An arrow from p to q, its tip at q; `colour` is a key of COLOURS or one of its values."""
    key = next((k for k, v in COLOURS.items() if v == colour), colour)
    return (f'<path d="M {p[0]:g} {p[1]:g} L {q[0]:g} {q[1]:g}" stroke="{COLOURS[key]}" stroke-width="{width:g}" '
            f'fill="none"{dash} marker-end="url(#head-{key})"/>')


# ---- trees: a state (triangle) above a q-state (circle) above the successor states

def below(x, y):
    """The middle of the base of the state triangle centred at (x, y)."""
    return x, y + BOTTOM


def edge_to_chance(p, c, colour=INK, width=STROKE):
    """An arrow from a point to the outline of the chance node centred at c."""
    dx, dy = c[0] - p[0], c[1] - p[1]
    n = (dx * dx + dy * dy) ** 0.5
    return arrow(p, (c[0] - dx / n * CHANCE_R, c[1] - dy / n * CHANCE_R), colour, width)


def edge_to_state(c, s, colour=INK, width=STROKE):
    """An arrow from the outline of the chance node c to the apex of the state triangle s."""
    dx, dy = s[0] - c[0], s[1] - TOP - c[1]
    n = (dx * dx + dy * dy) ** 0.5
    return arrow((c[0] + dx / n * CHANCE_R, c[1] + dy / n * CHANCE_R), (s[0], s[1] - TOP), colour, width)


def faded_triangle(x, y):
    apex, base = (x, y - TOP), y + BOTTOM
    return (f'<polygon points="{apex[0]:g},{apex[1]:g} {x - HALF:g},{base:g} {x + HALF:g},{base:g}" fill="white" '
            f'stroke="{FADED}" stroke-width="{STROKE}" stroke-linejoin="round"/>')


def faded_chance(x, y):
    return f'<circle cx="{x:g}" cy="{y:g}" r="{CHANCE_R}" fill="white" stroke="{FADED}" stroke-width="{STROKE}"/>'


def one_step(action_label, chance_label, actions):
    """The state s at the top, the q-state of the chosen action, its three successors s'. With `actions`,
    the other actions are faded, as alternatives the update compares."""
    s, c = (300, 50), (300, 175)
    kids = [(140, 320), (300, 320), (460, 320)]
    parts = []
    if actions:
        others = [(100, 175), (500, 175)]
        for o in others:
            parts.append(edge_to_chance(below(*s), o, FADED))
            parts.append(faded_chance(*o))
    parts.append(edge_to_chance(below(*s), c))
    for k in kids:
        parts.append(edge_to_state(c, k))
    parts.append(triangle(*s, up=True))
    parts.append(chance(*c))
    for k in kids:
        parts.append(triangle(*k, up=True))
    parts.append(formula(s[0] + HALF + 10, s[1] + 4, [("s", "i")], size=28, anchor="start"))
    parts.append(formula(c[0] + 14, (s[1] + BOTTOM + c[1] - CHANCE_R) / 2, action_label, size=26, anchor="start"))
    parts.append(formula(c[0] + CHANCE_R + 12, c[1], chance_label, size=26, anchor="start"))
    for k in kids:
        parts.append(formula(k[0], k[1] + BOTTOM + 26, [("s", "i"), ("", "′")], size=28))
    return parts


def fixed_policy():
    pi_s = [("π(", "i"), ("s", "i"), (")", "r")]
    return one_step(pi_s, [("s", "i"), (", ", "r")] + pi_s, actions=False)


def policy_evaluation_tree():
    return one_step([("a", "i")], [("s", "i"), (", ", "r"), ("a", "i")], actions=True)


# ---- the optimal policy does not depend on the starting state

def optimal_policy_merge():
    a, b, c = (80, 60), (80, 330), (430, 195)
    parts = []
    def run(p, colour, bend):
        """A run of the policy from below the state p to the left of c, a dashed curve."""
        start = (p[0] + HALF * 0.55, p[1] + (BOTTOM - 4 if bend > 0 else -TOP * 0.2))
        end = (c[0] - HALF * 0.62 - 6, c[1] + (-4 if bend > 0 else 12))
        mid = ((start[0] + end[0]) / 2 + 20, (start[1] + end[1]) / 2 + bend)
        c_ = {"blue": BLUE, "orange": ORANGE}[colour]
        return (f'<path d="M {start[0]:g} {start[1]:g} Q {mid[0]:g} {mid[1]:g} {end[0]:g} {end[1]:g}" '
                f'stroke="{c_}" stroke-width="2.6" stroke-dasharray="9 7" fill="none" '
                f'marker-end="url(#head-{colour})"/>')
    parts.append(run(a, "blue", 40))
    parts.append(run(b, "orange", -40))
    # from c, the action both policies choose, to the q-state it leads to
    q = (640, c[1] + 5)
    parts.append(edge_to_chance((c[0] + HALF * 0.55, c[1] + 4), q))
    parts.append(chance(*q))
    for s_ in (a, b, c):
        parts.append(triangle(*s_, up=True))
    parts.append(formula(a[0] - HALF - 10, a[1] + 4, [("a", "i")], size=28, anchor="end"))
    parts.append(formula(b[0] - HALF - 10, b[1] + 4, [("b", "i")], size=28, anchor="end"))
    parts.append(formula(c[0], c[1] + BOTTOM + 28, [("c", "i")], size=28))
    parts.append(formula(270, 95, [("π", "i"), (("∗", "a"), "^_")], size=28, fill=BLUE))
    parts.append(formula(270, 300, [("π", "i"), (("∗", "b"), "^_")], size=28, fill=ORANGE))
    label = [("π", "i"), (("∗", "a"), "^_"), ("(", "r"), ("c", "i"), (") = ", "r"),
             ("π", "i"), (("∗", "b"), "^_"), ("(", "r"), ("c", "i"), (")", "r")]
    parts.append(formula(548, c[1] - 40, label, size=24))
    return parts


# ---- discounting: three steps of a run, weighted by 1, gamma, gamma^2

def gem(box, x, y, height):
    """A gem of CS188, cropped from the former discounting.png, at (x, y) (top left), `height` units tall."""
    im = Image.open(ROOT / "figures" / "lec8" / "discounting-gems.png").convert("RGBA").crop(box)
    w = im.width * height / im.height
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    data = base64.b64encode(buf.getvalue()).decode()
    return (f'<image x="{x:g}" y="{y:g}" width="{w:.1f}" height="{height:g}" '
            f'href="data:image/png;base64,{data}"/>')


def brace(x, y0, y1, w=22):
    """A left curly brace from y0 to y1, its tip at x."""
    ym, r = (y0 + y1) / 2, w / 2
    xm = x + r
    d = (f"M {x + w:g} {y0:g} Q {xm:g} {y0:g} {xm:g} {y0 + r:g} L {xm:g} {ym - r:g} Q {xm:g} {ym:g} {x:g} {ym:g} "
         f"Q {xm:g} {ym:g} {xm:g} {ym + r:g} L {xm:g} {y1 - r:g} Q {xm:g} {y1:g} {x + w:g} {y1:g}")
    return f'<path d="{d}" stroke="{INK}" stroke-width="{STROKE}" fill="none" stroke-linejoin="round"/>'


def discounting():
    step = 175
    xs, xc = 470, 520    # the run zigzags: states on the left, q-states on the right
    states = [(xs if k % 2 == 0 else xc - 10, 45 + k * step) for k in range(4)]
    qs = [(xc if k % 2 == 0 else xs - 10, 45 + k * step + step / 2 + 5) for k in range(3)]
    parts = []
    # the alternatives: the other actions from each state, the other outcomes of each q-state
    for (x, y), (qx, qy) in zip(states, qs):
        for dx in (-110, 110):
            if (x + dx) != qx:
                parts.append(arrow((x, y + BOTTOM), (x + dx * 0.75, y + BOTTOM + (qy - y - BOTTOM) * 0.75), FADED, 1.6))
    for (qx, qy), (x, y) in zip(qs, states[1:]):
        for dx in (-120, 120):
            parts.append(arrow((qx, qy + CHANCE_R), (qx + dx * 0.7, qy + CHANCE_R + (y - TOP - qy - CHANCE_R) * 0.7),
                               FADED, 1.6))
    for (x, y), q in zip(states, qs):
        parts.append(edge_to_chance(below(x, y), q))
    for q, s_ in zip(qs, states[1:]):
        parts.append(edge_to_state(q, s_))
    for s_ in states:
        parts.append(triangle(*s_, up=True))
    for q in qs:
        parts.append(chance(*q))
    # the weights, one per step: a gem that loses its shine, the factor, a brace over the step
    boxes = [(38, 61, 173, 185), (35, 283, 136, 377), (15, 502, 165, 574)]
    heights = [110, 82, 62]
    factors = [[("1", "r")], [("γ", "i")], [("γ", "i"), ("2", "^"), ("", ".")]]
    for k, (box, h, f) in enumerate(zip(boxes, heights, factors)):
        top, bot = states[k][1] + 4, states[k + 1][1] + 4
        mid = (top + bot) / 2
        parts.append(gem(box, 10 + (150 - (box[2] - box[0]) * h / (box[3] - box[1])) / 2, mid - h / 2, h))
        parts.append(formula(235, mid, f, size=46, fill=BLUE))
        parts.append(brace(320, top, bot))
    return parts


# ---- the dynamic decision network

def variable(x, y, name, sub, known=False):
    fill = FILL if known else "white"
    return (f'<circle cx="{x:g}" cy="{y:g}" r="{R}" fill="{fill}" stroke="{INK}" stroke-width="{STROKE}"/>'
            + formula(x, y, [(name, "b"), (sub, "_"), ("", ".")], size=26))


def decision(x, y, sub, known=False):
    h = 30
    fill = FILL if known else "white"
    return (f'<rect x="{x - h:g}" y="{y - h:g}" width="{2 * h}" height="{2 * h}" fill="{fill}" stroke="{INK}" '
            f'stroke-width="{STROKE}"/>' + formula(x, y, [("A", "i"), (sub, "_"), ("", ".")], size=26))


def utility(x, y, name, sub, known=False):
    h = 38
    fill = FILL if known else "white"
    return (f'<polygon points="{x:g},{y - h:g} {x + h:g},{y:g} {x:g},{y + h:g} {x - h:g},{y:g}" fill="{fill}" '
            f'stroke="{INK}" stroke-width="{STROKE}" stroke-linejoin="round"/>'
            + formula(x, y, [(name, "i"), (sub, "_"), ("", ".")], size=24))


def toward(p, q, rp, rq):
    """The segment from p to q, cut by rp at p and rq at q (circles, or the half side of a square)."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = (dx * dx + dy * dy) ** 0.5
    return (p[0] + dx / n * rp, p[1] + dy / n * rp), (q[0] - dx / n * rq, q[1] - dy / n * rq)


def generic_ddn(step=3):
    """The network built in three steps, at the same size: 1 the dynamic Bayesian network of lecture 6,
    2 with the actions, 3 with the rewards and the utility at the horizon."""
    subs = ["t−1", "t", "t+1", "t+2", "t+3"]
    acts = ["t−2", "t−1", "t", "t+1", "t+2"]
    y_a, y_x, y_r, y_e = 50, 175, 260, 330
    xs = [150 + 175 * k for k in range(5)]
    parts = []
    # a square's border is at distance h / cos of the angle; a diamond's at h / (|cos| + |sin|)
    for k, x in enumerate(xs):
        a = (x - 75, y_a)
        p, q = toward(a, (x, y_x), 0, R)
        dx, dy = x - a[0], y_x - a[1]
        t = 30 / max(abs(dx), abs(dy))
        if step >= 2:
            parts.append(arrow((a[0] + dx * t, a[1] + dy * t), q))
        parts.append(arrow(*toward((x, y_x), (x, y_e), R, R)))
        if k < 4:
            parts.append(arrow(*toward((x, y_x), (xs[k + 1], y_x), R, R)))
        if k < 4 and step >= 3:
            r = (x + 62, y_r)
            dx, dy = r[0] - x, r[1] - y_x
            n = (dx * dx + dy * dy) ** 0.5
            cut = 38 / (abs(dx) + abs(dy)) * n
            p, _ = toward((x, y_x), r, R, 0)
            parts.append(arrow(p, (r[0] - dx / n * cut, r[1] - dy / n * cut)))
    parts.append(arrow((20, y_x), (xs[0] - R, y_x)))
    if step >= 3:
        parts.append(arrow((xs[-1] + R, y_x), (xs[-1] + 95 - 38, y_x)))
    for k, x in enumerate(xs):
        if step >= 2:
            parts.append(decision(x - 75, y_a, acts[k], known=k < 2))
        parts.append(variable(x, y_x, "X", subs[k]))
        parts.append(variable(x, y_e, "E", subs[k], known=k < 2))
        if k < 4 and step >= 3:
            parts.append(utility(x + 62, y_r, "R", subs[k], known=k < 2))
    if step >= 3:
        parts.append(utility(xs[-1] + 95, y_x, "U", "t+3"))
    return parts


# ---- the look-ahead search of the network

def stub(x, y):
    return "".join(line((x, y), (x + dx, y + 16), width=1.4, arrow=False) for dx in (-10, 0, 10))


def pomdp_tree():
    rows = [40, 175, 300, 435, 560, 695, 805]   # edges long enough to carry their labels
    # the rows: the belief states b where the agent decides, the percepts the environment draws, the leaves
    labels = [[("b", "i"), (sub, "_"), ("", ".")] for sub in ("t", "t+1", "t+2")]
    percepts = [[("E", "b"), (sub, "_"), ("", ".")] for sub in ("t+1", "t+2", "t+3")]
    labels = [labels[0], percepts[0], labels[1], percepts[1], labels[2], percepts[2], [("U", "i"), ("t+3", "_"), ("", ".")]]
    parts = [formula(345, y, lab, size=32, fill=GREY, anchor="end") for lab, y in zip(labels, rows)]
    # each level: the x of its nodes, the one expanded, where the ellipsis goes
    levels = [[600], [400, 490, 600, 710, 800], [430, 540, 700, 820], [540, 660, 790, 880],
              [430, 540, 660, 790], [470, 580, 720, 820], [500, 610, 760, 860]]
    open_ = [600, 600, 700, 540, 660, 580]
    dots = [None, 545, 620, 725, 600, 650, 685]
    for k in range(1, 7):
        parent, y0 = open_[k - 1], rows[k - 1]
        start = parent, y0 + (BOTTOM if k % 2 == 1 else CHANCE_R)
        for x in levels[k]:
            if k == 6:
                end = (x, rows[k] - LEAF[1] / 2)
            elif k % 2 == 1:
                end = (x, rows[k] - CHANCE_R)
            else:
                end = (x, rows[k] - TOP)
            parts.append(arrow(start, end))
        parts.append(text(dots[k], rows[k], "…", size=30, fill=GREY))
    parts.append(triangle(600, rows[0], up=True))
    for k in range(1, 6):
        for x in levels[k]:
            if k % 2 == 1:
                parts.append(chance(x, rows[k]))
                if x != open_[k]:
                    parts.append(stub(x, rows[k] + CHANCE_R))
            else:
                parts.append(triangle(x, rows[k], up=True))
                if x != open_[k]:
                    parts.append(stub(x, rows[k] + BOTTOM))
    for x, v in zip(levels[6], ["10", "4", "6", "3"]):
        parts.append(leaf(x, rows[6], v))
    # on the expanded path, the action taken at each belief and the percept drawn at each chance node
    path = open_ + [500]
    for k, (letter, sub) in enumerate([("a", "t"), ("e", "t+1"), ("a", "t+1"), ("e", "t+2"), ("a", "t+2"), ("e", "t+3")], 1):
        x0 = path[k - 1]
        y0 = rows[k - 1] + (BOTTOM if letter == "a" else CHANCE_R)
        x1 = path[k]
        y1 = rows[k] - (CHANCE_R if letter == "a" else (LEAF[1] / 2 if k == 6 else TOP))
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        # on the edge itself, its halo breaking the line, as the dice of lecture 3's backgammon tree
        lx, ly, anchor = mx, my, "middle"
        label = formula(lx, ly, [(letter, "i"), (sub, "_"), ("", ".")], size=28, anchor=anchor)
        # the halo is a copy of the label underneath: a stroke on the label itself would paint over its glyphs
        parts.append(label.replace("<text ", '<text stroke="white" stroke-width="16" stroke-linejoin="round" ', 1)
                     .replace(f'fill="{INK}"', 'fill="white"', 1))
        parts.append(label)
    return parts


if __name__ == "__main__":
    svg("fixed-policy", 460, 385, fixed_policy(), x0=80)
    svg("policy-evaluation-tree", 520, 385, policy_evaluation_tree(), x0=60)
    svg("optimal-policy-merge", 700, 370, optimal_policy_merge())
    svg("discounting", 620, 610, discounting())
    for step in (1, 2, 3):
        svg(f"ddn-{step}", 1000, 380, generic_ddn(step))
    svg("pomdp-tree", 640, 838, pomdp_tree(), x0=270)
