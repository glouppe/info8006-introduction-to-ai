"""Draw the Bayesian network diagrams of lecture 5 in the style of the course.

    uv run python scripts/draw_bn_diagrams.py

Writes `figures/lec5/state-percepts.svg`, the agent's model of lecture 1 as a two-node network:
the unobserved state S with its prior P(s), the observed percepts E (shaded) with the sensor
model P(e | s). Also writes `parameterized-bn.svg`, the candy networks of cases (a) and (b) with
their parameterized CPTs (after Figure 20.2 of Russell and Norvig), and `caseb-bayesian.svg`, the
network of Bayesian learning for case (b), with the parameters as variables and the observed
flavors and wrappers shaded (after Figure 20.6). Helpers and fonts are those of `draw_game_trees.py`.
"""

from math import hypot

from draw_game_trees import BLUE, FILL, GREY, INK, ROOT, STROKE, fonts, text

R = 40


def node(x, y, name, observed):
    fill = FILL if observed else "white"
    return (f'<circle cx="{x}" cy="{y}" r="{R}" fill="{fill}" stroke="{INK}" stroke-width="{STROKE:g}"/>'
            + text(x, y, name, size=30, style=' font-style="italic"'))


def arrow(p, q):
    return (f'<path d="M {p[0]:g} {p[1]:g} L {q[0]:g} {q[1]:g}" stroke="{INK}" stroke-width="{STROKE:g}" '
            f'fill="none" marker-end="url(#head)"/>')


def formula(x, y, parts):
    """A formula in the course blue, from (text, italic) pieces."""
    spans = "".join(f'<tspan font-style="italic">{t}</tspan>' if it else f"<tspan>{t}</tspan>" for t, it in parts)
    return (f'<text x="{x}" y="{y + 8:.1f}" font-family="Roboto, sans-serif" font-size="24" fill="{BLUE}" '
            f'text-anchor="middle" xml:space="preserve">{spans}</text>')


def state_percepts():
    xs, xe, y = 110, 390, 90
    return [
        text(xs, 22, "state", size=22, fill=GREY),
        text(xe, 22, "percepts", size=22, fill=GREY),
        node(xs, y, "S", False),
        node(xe, y, "E", True),
        arrow((xs + R, y), (xe - R - 4, y)),
        formula(xs, y + R + 34, [("P(", False), ("s", True), (")", False)]),
        formula(xe, y + R + 34, [("P(", False), ("e", True), ("\u00a0|\u00a0", False), ("s", True), (")", False)]),
    ]


RX, RY = 80, 32   # half axes of a named variable


def label(x, y, name, sub=None, size=26, italic=True, fill=INK):
    """A variable name, in italics, with an optional subscript."""
    style = ' font-style="italic"' if italic else ""
    tail = f'<tspan font-size="{0.7 * size:g}" dy="{0.25 * size:g}" font-style="normal">{sub}</tspan>' if sub else ""
    return (f'<text x="{x:g}" y="{y + 0.35 * size:.1f}" font-family="Roboto, sans-serif" font-size="{size:g}" '
            f'fill="{fill}" text-anchor="middle"{style}>{name}{tail}</text>')


def variable(x, y, name, sub=None, observed=False, rx=RX, ry=RY, italic=True):
    fill = FILL if observed else "white"
    return (f'<ellipse cx="{x:g}" cy="{y:g}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{INK}" '
            f'stroke-width="{STROKE:g}"/>' + label(x, y, name, sub, italic=italic))


def link(p, q, rp=(RX, RY), rq=(RX, RY)):
    """An arrow between the borders of two ellipses centred at p and q."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    sp = 1 / hypot(dx / rp[0], dy / rp[1])
    sq = 1 / hypot(dx / rq[0], dy / rq[1])
    gap = 5 / hypot(dx, dy)
    a = (p[0] + dx * sp, p[1] + dy * sp)
    b = (q[0] - dx * (sq + gap), q[1] - dy * (sq + gap))
    return arrow(a, b)


def cell(x, y, w, h, fill="white"):
    return (f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="{fill}" stroke="{INK}" '
            f'stroke-width="1.5"/>')


def math(x, y, parts, size=22, fill=INK, anchor="middle"):
    """A formula from (text, style) pieces: style is "i" (italic), "s" (subscript) or ""."""
    spans = ""
    for t, st in parts:
        if st == "i":
            spans += f'<tspan font-style="italic">{t}</tspan>'
        elif st == "s":
            spans += f'<tspan font-size="{0.7 * size:g}" dy="{0.25 * size:g}">{t}</tspan><tspan dy="{-0.25 * size:g}"></tspan>'
        else:
            spans += f"<tspan>{t}</tspan>"
    return (f'<text x="{x:g}" y="{y + 0.35 * size:.1f}" font-family="Roboto, sans-serif" font-size="{size:g}" '
            f'fill="{fill}" text-anchor="{anchor}" xml:space="preserve">{spans}</text>')


PF = [("P(", ""), ("F", "i"), ("\u00a0=\u00a0", ""), ("cherry", "i"), (")", "")]


def prior_table(x, y):
    """The CPT of Flavor, centred at x, from y down."""
    w = 170
    return [cell(x - w / 2, y, w, 36, FILL), math(x, y + 18, PF, size=20),
            cell(x - w / 2, y + 36, w, 42), math(x, y + 57, [("θ", "")], size=24, fill=BLUE)]


def wrapper_table(x, y):
    """The CPT of Wrapper, from its top left corner."""
    w1, w2, h = 82, 150, 42
    head = [("P(", ""), ("W", "i"), ("\u00a0=\u00a0", ""), ("red", "i"), ("\u00a0|\u00a0", ""), ("F", "i"), (")", "")]
    parts = [cell(x, y, w1, 36, FILL), cell(x + w1, y, w2, 36, FILL),
             math(x + w1 / 2, y + 18, [("F", "i")], size=20), math(x + w1 + w2 / 2, y + 18, head, size=20)]
    for k, (flavor, sub) in enumerate([("cherry", "1"), ("lime", "2")]):
        yy = y + 36 + k * h
        parts += [cell(x, yy, w1, h), cell(x + w1, yy, w2, h),
                  math(x + w1 / 2, yy + h / 2, [(flavor, "i")], size=20),
                  math(x + w1 + w2 / 2, yy + h / 2, [("θ", ""), (sub, "s")], size=24, fill=BLUE)]
    return parts


def parameterized():
    xa, xb = 160, 460
    parts = prior_table(xa, 110) + [variable(xa, 250, "Flavor"), text(xa, 420, "(a)", size=22, fill=GREY)]
    parts += prior_table(xb, 20) + [variable(xb, 160, "Flavor"), variable(xb, 340, "Wrapper"),
                                    link((xb, 160), (xb, 340))]
    parts += wrapper_table(xb + 100, 212) + [text(xb, 420, "(b)", size=22, fill=GREY)]
    return parts


def bayesian_learning():
    xs, yt, yf, yw, yb = [150, 370, 590], 50, 190, 330, 450
    theta = lambda x, y, sub=None: variable(x, y, "Θ", sub, rx=36, ry=36, italic=False)
    parts = [theta(370, yt), theta(260, yb, "1"), theta(480, yb, "2")]
    for i, x in enumerate(xs, 1):
        parts += [variable(x, yf, "Flavor", str(i), observed=True), variable(x, yw, "Wrapper", str(i), observed=True),
                  link((370, yt), (x, yf), (36, 36)), link((x, yf), (x, yw))]
        for xt in (260, 480):
            parts.append(link((xt, yb), (x, yw), (36, 36)))
    for y in (yf, yw):
        parts.append(text(735, y, "…", size=30))
    return parts


def svg(name, width, height, parts):
    head = (f'<marker id="head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" '
            f'orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="{INK}"/></marker>')
    out = ROOT / "figures" / "lec5" / f"{name}.svg"
    out.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" '
                   f'height="{height}"><defs>{fonts()}{head}</defs>{"".join(parts)}</svg>\n', encoding="utf-8")
    print(f"{out.relative_to(ROOT)}  {width}x{height}")


if __name__ == "__main__":
    svg("state-percepts", 500, 180, state_percepts())
    svg("parameterized-bn", 800, 450, parameterized())
    svg("caseb-bayesian", 780, 500, bayesian_learning())
