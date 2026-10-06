"""Draw the Bayesian network diagrams of lecture 5 in the style of the course.

    uv run python scripts/draw_bn_diagrams.py

Writes `figures/lec5/state-percepts.svg`, the agent's model of lecture 1 as a two-node network:
the unobserved state S with its prior P(s), the observed percepts E (shaded) with the sensor
model P(e | s). Helpers and fonts are those of `draw_game_trees.py`.
"""

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


def svg(name, width, height, parts):
    head = (f'<marker id="head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" '
            f'orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="{INK}"/></marker>')
    out = ROOT / "figures" / "lec5" / f"{name}.svg"
    out.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" '
                   f'height="{height}"><defs>{fonts()}{head}</defs>{"".join(parts)}</svg>\n', encoding="utf-8")
    print(f"{out.relative_to(ROOT)}  {width}x{height}")


if __name__ == "__main__":
    svg("state-percepts", 500, 180, state_percepts())
