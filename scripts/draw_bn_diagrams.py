"""Draw the Bayesian networks of lecture 5 in the style of the course.

    uv run python scripts/draw_bn_diagrams.py

Variables are circles of radius 36, shaded when observed, with their names in italics; long
names are shortened to initials and spelled out in grey captions. All figures share this scale,
and the deck sets their widths so that one unit shows as about 0.95 px on a 1280 px slide.
Writes to `figures/lec5/`:

- `state-percepts.svg`, the agent's model: the state S with its prior, the percepts E with the
  sensor model;
- `example-d.svg`, the network over L, R, B, D, T, T' used for the definition and d-separation;
- `burglary.svg`, the alarm network with its CPTs (Figure 13.2 of Russell and Norvig);
- `nondescendants.svg` and `markov-blanket.svg`, a variable X with its parents U, children Y and
  the children's other parents Z, and the band of its non-descendants or its Markov blanket;
- `dentist-network.svg`, `traffic-causal.svg`, `traffic-diagnostic.svg`, `burglary-orders.svg`
  (the alarm network built in two other orders), `xyz.svg`, `active-inactive.svg` (the active
  and inactive triples), `bn-alarm.svg` and `ve-ordering.svg`;
- `parameterized-bn.svg` and `caseb-bayesian.svg`, the candy networks with their parameters.

Helpers and fonts are those of `draw_game_trees.py`; `draw_temporal_networks.py` reuses these.
"""

import base64
from math import cos, hypot, radians, sin

from draw_game_trees import BLUE, FILL, GREY, INK, ROOT, STROKE, text
from draw_game_trees import fonts as text_fonts

MATH = "KaTeX_Math"   # italic letters, as LaTeX's math italic
MAIN = "KaTeX_Main"   # digits, operators, words and bold symbols, as LaTeX's roman


def fonts():
    """Roboto for the captions, and the KaTeX fonts of the slides for the mathematics."""
    faces = []
    for family, weight, name in [(MATH, 400, "KaTeX_Math-Italic"), (MAIN, 400, "KaTeX_Main-Regular"),
                                 (MAIN, 700, "KaTeX_Main-Bold")]:
        data = base64.b64encode((ROOT / "assets" / "fonts" / f"{name}.woff2").read_bytes()).decode()
        faces.append(f"@font-face {{ font-family: '{family}'; font-weight: {weight}; "
                     f"src: url(data:font/woff2;base64,{data}) format('woff2'); }}")
    return text_fonts() + "<style>" + " ".join(faces) + "</style>"


def span(t, size=None, dy=None, bold=False):
    """A piece of mathematics: single letters in math italic, the rest in roman."""
    letter = len(t) == 1 and t.isalpha() and not bold and t not in "ΘΣΠ"
    family = MATH if letter else MAIN
    attrs = f' font-family="{family}"' + (' font-weight="700"' if bold else "")
    attrs += f' font-size="{size:g}"' if size else ""
    attrs += f' dy="{dy:g}"' if dy is not None else ""
    return f"<tspan{attrs}>{t}</tspan>"


def sub_spans(sub, size):
    """A subscript such as 1, t, t+1, n−1 or 1j, each character in its own face."""
    return "".join(span(c, size) for c in sub)

R = 36
DARK = "#9a9a9a"   # the variable X whose family is shown
BAND = "#e3e3e3"   # the band of non-descendants, or of the Markov blanket


def label(x, y, name, sub=None, size=28, italic=True, fill=INK, bold=False):
    """A variable name typeset as in LaTeX, with an optional subscript."""
    head = "".join(span(c, bold=bold) for c in name) if italic or bold else f'<tspan font-family="{MAIN}">{name}</tspan>'
    tail = ""
    if sub:
        tail = f'<tspan font-size="{0.7 * size:g}" dy="{0.25 * size:g}">{sub_spans(sub, None)}</tspan>'
    return (f'<text x="{x:g}" y="{y + 0.3 * size:.1f}" font-size="{size:g}" fill="{fill}" '
            f'text-anchor="middle">{head}{tail}</text>')


def node(x, y, name, sub=None, observed=False, italic=True, fill=None):
    """A variable as a circle, shaded when observed."""
    fill = fill or (FILL if observed else "white")
    return (f'<circle cx="{x:g}" cy="{y:g}" r="{R}" fill="{fill}" stroke="{INK}" stroke-width="{STROKE:g}"/>'
            + label(x, y, name, sub, italic=italic))


def caption(x, y, words, anchor="middle"):
    return text(x, y, words, size=20, fill=GREY, anchor=anchor)


def arrow(p, q):
    return (f'<path d="M {p[0]:g} {p[1]:g} L {q[0]:g} {q[1]:g}" stroke="{INK}" stroke-width="{STROKE:g}" '
            f'fill="none" marker-end="url(#head)"/>')


def link(p, q, rp=(R, R), rq=(R, R)):
    """An arrow between the borders of two ellipses (circles by default) centred at p and q."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    sp = 1 / hypot(dx / rp[0], dy / rp[1])
    sq = 1 / hypot(dx / rq[0], dy / rq[1])
    gap = 0   # the arrow tip ends on the outline of the node
    return arrow((p[0] + dx * sp, p[1] + dy * sp), (q[0] - dx * (sq + gap), q[1] - dy * (sq + gap)))


def stub(p, angle, inward, length=36):
    """A short arrow into (inward) or out of a node at p, in a direction given in degrees."""
    ux, uy = cos(radians(angle)), sin(radians(angle))
    far = (p[0] + ux * (R + length), p[1] + uy * (R + length))
    if inward:
        return arrow(far, (p[0] + ux * R, p[1] + uy * R))
    return arrow((p[0] + ux * R, p[1] + uy * R), far)


def cell(x, y, w, h, fill="white"):
    return (f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="{fill}" stroke="{INK}" '
            f'stroke-width="1.5"/>')


def math(x, y, parts, size=22, fill=INK, anchor="middle"):
    """A formula from (text, style) pieces: "i" a symbol or a word, "s" a subscript, "" roman."""
    spans = ""
    for t, st in parts:
        if st == "s":
            spans += (f'<tspan font-size="{0.7 * size:g}" dy="{0.25 * size:g}">{sub_spans(t, None)}</tspan>'
                      f'<tspan dy="{-0.25 * size:g}"></tspan>')
        elif st == "i":
            spans += span(t)
        else:
            spans += f'<tspan font-family="{MAIN}">{t}</tspan>'
    return (f'<text x="{x:g}" y="{y + 0.3 * size:.1f}" font-size="{size:g}" fill="{fill}" '
            f'text-anchor="{anchor}" xml:space="preserve">{spans}</text>')


def table(x, y, head, rows, widths):
    """A CPT from its top left corner: header cells, then rows of cells, as formula pieces."""
    h0, h = 32, 28
    parts, xx = [], x
    for w, hd in zip(widths, head):
        parts += [cell(xx, y, w, h0, FILL), math(xx + w / 2, y + h0 / 2, hd, size=18)]
        xx += w
    for k, row in enumerate(rows):
        yy, xx = y + h0 + k * h, x
        for w, v in zip(widths, row):
            parts += [cell(xx, yy, w, h), math(xx + w / 2, yy + h / 2, v, size=18)]
            xx += w
    return parts


def P(*pieces):
    """The header P(...) of a CPT column."""
    return [("P(", "")] + list(pieces) + [(")", "")]


def svg(name, width, height, parts):
    head = (f'<marker id="head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" '
            f'orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="{INK}"/></marker>')
    out = ROOT / "figures" / "lec5" / f"{name}.svg"
    out.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" '
                   f'height="{height}"><defs>{fonts()}{head}</defs>{"".join(parts)}</svg>\n', encoding="utf-8")
    print(f"{out.relative_to(ROOT)}  {width}x{height}")


def network(nodes, edges):
    """Nodes as {key: (x, y, name)} and edges as (key, key) pairs."""
    parts = [node(x, y, n) for x, y, n in nodes.values()]
    return parts + [link(nodes[a][:2], nodes[b][:2]) for a, b in edges]


# The agent's model

def state_percepts():
    xs, xe, y = 110, 390, 90
    return [
        caption(xs, 26, "state"), caption(xe, 26, "percepts"),
        node(xs, y, "S"), node(xe, y, "E", observed=True), link((xs, y), (xe, y)),
        math(xs, y + R + 32, [("P(", ""), ("s", "i"), (")", "")], size=24, fill=BLUE),
        math(xe, y + R + 32, [("P(", ""), ("e", "i"), (" | ", ""), ("s", "i"), (")", "")], size=24, fill=BLUE),
    ]


# Semantics

def example_d():
    nodes = {"L": (110, 45, "L"), "R": (110, 165, "R"), "B": (250, 165, "B"),
             "D": (40, 290, "D"), "T": (180, 290, "T"), "T2": (180, 415, "T′")}
    return network(nodes, [("L", "R"), ("R", "D"), ("R", "T"), ("B", "T"), ("T", "T2")])


def burglary():
    nodes = {"B": (90, 80, "B"), "E": (410, 80, "E"), "A": (250, 230, "A"), "J": (90, 380, "J"), "M": (410, 380, "M")}
    parts = network(nodes, [("B", "A"), ("E", "A"), ("A", "J"), ("A", "M")])
    parts += [caption(90, 26, "burglar"), caption(410, 26, "earthquake"), caption(250, 175, "alarm"),
              caption(90, 436, "John calls"), caption(410, 436, "Mary calls")]
    b, e, a = [("B", "i")], [("E", "i")], [("A", "i")]
    t, f = [("t", "i")], [("f", "i")]
    parts += table(140, 52, [P(*b)], [[[("0.001", "")]]], [90])
    parts += table(460, 52, [P(*e)], [[[("0.002", "")]]], [90])
    pa = P(("A", "i"), (" | ", ""), ("B", "i"), (", ", ""), ("E", "i"))
    parts += table(470, 165, [b, e, pa], [[t, t, [("0.95", "")]], [t, f, [("0.94", "")]], [f, t, [("0.29", "")]],
                                         [f, f, [("0.001", "")]]], [40, 40, 120])
    pj = P(("J", "i"), (" | ", ""), ("A", "i"))
    pm = P(("M", "i"), (" | ", ""), ("A", "i"))
    parts += table(140, 335, [a, pj], [[t, [("0.90", "")]], [f, [("0.05", "")]]], [40, 90])
    parts += table(460, 335, [a, pm], [[t, [("0.70", "")]], [f, [("0.01", "")]]], [40, 90])
    return parts


def family(band):
    """X with parents U, children Y and the children's other parents Z, inside a grey band."""
    U1, Um, X, Z1, Zn, Y1, Yn = (180, 75), (420, 75), (300, 185), (70, 195), (530, 195), (220, 305), (380, 305)
    if band == "nondescendants":
        shape = (f'<path d="M 40 380 L 70 195 L 180 75 L 420 75 L 530 195 L 560 380" fill="none" stroke="{BAND}" '
                 f'stroke-width="88" stroke-linejoin="round" stroke-linecap="round"/>')
    else:
        shape = f'<ellipse cx="300" cy="190" rx="232" ry="115" fill="none" stroke="{BAND}" stroke-width="88"/>'
    parts = [shape, node(*U1, "U", "1"), node(*Um, "U", "m"), node(*Z1, "Z", "1j"), node(*Zn, "Z", "nj"),
             node(*Y1, "Y", "1"), node(*Yn, "Y", "n"), node(*X, "X", fill=DARK),
             text(300, 75, "…", size=30), text(300, 305, "…", size=30)]
    parts += [link(U1, X), link(Um, X), link(X, Y1), link(X, Yn), link(Z1, Y1), link(Zn, Yn)]
    parts += [stub(U1, -120, True), stub(U1, -60, True), stub(Um, -120, True), stub(Um, -60, True),
              stub(Z1, -150, True), stub(Z1, 150, False), stub(Zn, -30, True), stub(Zn, 30, False),
              stub(Y1, 120, False), stub(Y1, 60, False), stub(Yn, 120, False), stub(Yn, 60, False)]
    return parts


def dentist():
    nodes = {"W": (60, 70, "W"), "C": (330, 70, "C"), "T": (240, 210, "T"), "H": (420, 210, "H")}
    parts = network(nodes, [("C", "T"), ("C", "H")])
    return parts + [caption(60, 18, "weather"), caption(330, 18, "cavity"), caption(240, 268, "toothache"),
                    caption(420, 268, "catch")]


def two(a, b):
    return network({a: (50, 45, a), b: (50, 185, b)}, [(a, b)])


def burglary_orders():
    left = {"M": (60, 50), "J": (230, 110), "A": (145, 200), "B": (60, 300), "E": (230, 350)}
    right = {"M": (480, 50), "J": (670, 60), "E": (750, 180), "B": (480, 280), "A": (670, 300)}
    parts = []
    for nodes, edges in [(left, [("M", "J"), ("M", "A"), ("J", "A"), ("A", "B"), ("A", "E"), ("B", "E")]),
                         (right, [("M", "J"), ("M", "E"), ("J", "E"), ("M", "B"), ("J", "B"), ("E", "B"),
                                  ("M", "A"), ("J", "A"), ("E", "A"), ("B", "A")])]:
        parts += [node(x, y, k) for k, (x, y) in nodes.items()]
        parts += [link(nodes[a], nodes[b]) for a, b in edges]
    return parts + [caption(145, 420, "(a)"), caption(615, 420, "(b)")]


def xyz():
    return network({"X": (40, 40, "X"), "Y": (180, 40, "Y"), "Z": (320, 40, "Z")}, [("X", "Y"), ("Y", "Z")])


def triple(x, y, kind, observed=(), descendant=False):
    """A triple A, B, C at (x, y), its observed nodes shaded; a v-structure may add a descendant D of B."""
    pos = {"cascade": {"A": (x, y), "B": (x + 110, y), "C": (x + 220, y)},
           "parent": {"A": (x, y + 80), "B": (x + 110, y), "C": (x + 220, y + 80)},
           "v": {"A": (x, y), "B": (x + 110, y + 80), "C": (x + 220, y)}}[kind]
    edges = {"cascade": [("A", "B"), ("B", "C")], "parent": [("B", "A"), ("B", "C")],
             "v": [("A", "B"), ("C", "B")]}[kind]
    if descendant:
        pos["D"] = (x + 110, y + 190)
        edges = edges + [("B", "D")]
    parts = [f'<circle cx="{px:g}" cy="{py:g}" r="{R}" fill="{FILL if k in observed else "white"}" stroke="{INK}" '
             f'stroke-width="{STROKE:g}"/>' for k, (px, py) in pos.items()]
    parts += [link(pos[a], pos[b]) for a, b in edges]
    if descendant:   # a path of descendants, drawn dashed
        parts[-1] = parts[-1].replace('fill="none"', 'fill="none" stroke-dasharray="6 6"')
    return parts


def active_inactive():
    """Rows: cascade, common parent, v-structure; the first two columns are active, the last inactive."""
    parts = [text(310, 18, "active", size=22, fill=BLUE), text(790, 18, "inactive", size=22, fill=GREY),
             f'<path d="M 650 0 L 650 590" stroke="{GREY}" stroke-width="1.5"/>']
    parts += triple(40, 80, "cascade") + triple(40, 175, "parent") + triple(40, 360, "v", "B")
    parts += triple(360, 360, "v", "D", True)
    parts += triple(700, 80, "cascade", "B") + triple(700, 175, "parent", "B") + triple(700, 360, "v")
    return parts


def bn_alarm():
    nodes = {"B": (50, 45, "B"), "E": (250, 45, "E"), "A": (150, 160, "A"), "J": (50, 275, "J"), "M": (250, 275, "M")}
    return network(nodes, [("B", "A"), ("E", "A"), ("A", "J"), ("A", "M")])


def ve_ordering():
    parts = [node(300, 45, "Z")]
    for x, s in [(60, "1"), (160, "2"), (440, "n−1"), (540, "n")]:
        parts += [node(x, 180, "X", s), node(x, 310, "Y", s, observed=True), link((300, 45), (x, 180)),
                  link((x, 180), (x, 310))]
    return parts + [text(300, 180, "…", size=30), text(300, 310, "…", size=30)]


# Parameter learning

PF = [("P(", ""), ("F", "i"), (" = ", ""), ("cherry", "i"), (")", "")]


def prior_table(x, y):
    """The CPT of the flavor F, centred at x, from y down."""
    w = 160
    return [cell(x - w / 2, y, w, 34, FILL), math(x, y + 17, PF, size=19),
            cell(x - w / 2, y + 34, w, 40), math(x, y + 54, [("θ", "")], size=24, fill=BLUE)]


def wrapper_table(x, y):
    """The CPT of the wrapper W, from its top left corner."""
    w1, w2, h = 80, 150, 40
    head = [("P(", ""), ("W", "i"), (" = ", ""), ("red", "i"), (" | ", ""), ("F", "i"), (")", "")]
    parts = [cell(x, y, w1, 34, FILL), cell(x + w1, y, w2, 34, FILL),
             math(x + w1 / 2, y + 17, [("F", "i")], size=19), math(x + w1 + w2 / 2, y + 17, head, size=19)]
    for k, (flavor, sub) in enumerate([("cherry", "1"), ("lime", "2")]):
        yy = y + 34 + k * h
        parts += [cell(x, yy, w1, h), cell(x + w1, yy, w2, h), math(x + w1 / 2, yy + h / 2, [(flavor, "i")], size=19),
                  math(x + w1 + w2 / 2, yy + h / 2, [("θ", ""), (sub, "s")], size=24, fill=BLUE)]
    return parts


def parameterized():
    xa, xb = 130, 420
    parts = prior_table(xa, 100) + [node(xa, 240, "F"), caption(xa, 300, "flavor"), caption(xa, 400, "(a)")]
    parts += prior_table(xb, 10) + [node(xb, 150, "F"), node(xb, 320, "W"), link((xb, 150), (xb, 320)),
                                    caption(xb - 50, 150, "flavor", "end"), caption(xb - 50, 320, "wrapper", "end")]
    return parts + wrapper_table(xb + 60, 200) + [caption(xb, 400, "(b)")]


def bayesian_learning():
    xs, yt, yf, yw, yb = [170, 340, 510], 45, 165, 285, 405
    parts = [node(340, yt, "Θ", italic=False), node(255, yb, "Θ", "1", italic=False), node(425, yb, "Θ", "2", italic=False),
             caption(10, yf, "flavor", "start"), caption(10, yw, "wrapper", "start")]
    for i, x in enumerate(xs, 1):
        parts += [node(x, yf, "F", str(i), observed=True), node(x, yw, "W", str(i), observed=True),
                  link((340, yt), (x, yf)), link((x, yf), (x, yw)), link((255, yb), (x, yw)), link((425, yb), (x, yw))]
    return parts + [text(610, yf, "…", size=30), text(610, yw, "…", size=30)]


if __name__ == "__main__":
    svg("state-percepts", 500, 180, state_percepts())
    svg("example-d", 290, 455, example_d())
    svg("burglary", 680, 460, burglary())
    svg("nondescendants", 600, 400, family("nondescendants"))
    svg("markov-blanket", 600, 370, family("blanket"))
    svg("dentist-network", 480, 280, dentist())
    svg("traffic-causal", 100, 230, two("R", "T"))
    svg("traffic-diagnostic", 100, 230, two("T", "R"))
    svg("burglary-orders", 800, 440, burglary_orders())
    svg("xyz", 360, 80, xyz())
    svg("active-inactive", 960, 590, active_inactive())
    svg("bn-alarm", 300, 320, bn_alarm())
    svg("ve-ordering", 600, 350, ve_ordering())
    svg("parameterized-bn", 720, 420, parameterized())
    svg("caseb-bayesian", 640, 445, bayesian_learning())
