"""Draw the agent diagrams of lecture 1 in the style of the course.

    uv run python scripts/draw_agent_diagrams.py

Redraws Figures 2.9, 2.11, 2.13, 2.14 and 2.15 of Russell and Norvig (AIMA) as SVG files in
`figures/lec1/`, together with the agent-environment loop of the first slides. Pills are the knowledge of the agent, white boxes what it computes, and the blue
box its decision. Elements sit on a fixed grid, so that a box keeps its place from one diagram to the
next, and arrows are horizontal or vertical. Roboto and Lato are embedded from `assets/fonts/`, since
an SVG shown as an image cannot load fonts from the page.
"""

import base64
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent

BLUE = "#356aaf"
SOFT_BLUE = "#5b82b5"
INK = "#2a2a2a"
GREY = "#555555"
AGENT_FILL = "#f2f6fb"
ENV_FILL = "#f5f7fa"
ENV_STROKE = "#b8b8b8"
PILL_FILL = "#dde8f5"
PILL_INK = "#1e3f6b"
BOX_STROKE = "#9fb6d6"

WIDTH, AGENT_RIGHT, ENV_LEFT, ENV_WIDTH = 900, 650, 730, 120
PX, PILL_W, PILL_H = 175, 250, 40    # knowledge column
BX, BOX_W, BOX_H = 500, 250, 64      # computation column
BUS = (PX + PILL_W / 2 + BX - BOX_W / 2) / 2

# Rows of the four diagrams of Figures 2.9 to 2.14
SENSORS, A, B, C, D, ACTUATORS = 60, 136, 232, 328, 424, 500
STATE, HOW, ACTIONS = 120, 176, 232


def fonts():
    faces = []
    for family, weight, name in [("Roboto", 400, "Roboto-400-latin"), ("Lato", 900, "Lato-900-latin")]:
        data = base64.b64encode((ROOT / "assets" / "fonts" / f"{name}.woff2").read_bytes()).decode()
        faces.append(f"@font-face {{ font-family: '{family}'; font-weight: {weight}; "
                     f"src: url(data:font/woff2;base64,{data}) format('woff2'); }}")
    return "<style>" + " ".join(faces) + "</style>"


def text(x, y, lines, size=19, weight=400, family="Roboto", fill=INK, anchor="middle", extra=""):
    lines = [lines] if isinstance(lines, str) else lines
    step = 1.25 * size
    top = y - (len(lines) - 1) * step / 2 + 0.35 * size
    spans = "".join(f'<tspan x="{x:g}" y="{top + i * step:.1f}">{escape(line)}</tspan>' for i, line in enumerate(lines))
    return (f'<text font-family="{family}, sans-serif" font-weight="{weight}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}"{extra}>{spans}</text>')


def label(x, y, words, anchor="start"):
    return text(x, y, words, size=17, fill=SOFT_BLUE, anchor=anchor)


def pill(cy, words):
    return (f'<rect x="{PX - PILL_W / 2:g}" y="{cy - PILL_H / 2:g}" width="{PILL_W}" height="{PILL_H}" '
            f'rx="{PILL_H / 2:g}" fill="{PILL_FILL}"/>' + text(PX, cy, words, fill=PILL_INK))


def box(cx, cy, lines, w=BOX_W, h=BOX_H, decision=False):
    fill, stroke, ink = (BLUE, BLUE, "#ffffff") if decision else ("#ffffff", BOX_STROKE, INK)
    return (f'<rect x="{cx - w / 2:g}" y="{cy - h / 2:g}" width="{w}" height="{h}" rx="8" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="1.5"/>' + text(cx, cy, lines, fill=ink))


def path(points, head=True, dashed=False, radius=10, width=2, tip="tip"):
    """Polyline through `points`, with rounded corners."""
    def toward(p, q, dist):
        length = ((q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2) ** 0.5
        return p[0] + (q[0] - p[0]) / length * dist, p[1] + (q[1] - p[1]) / length * dist
    d = f"M {points[0][0]:g} {points[0][1]:g}"
    for prev, corner, nxt in zip(points, points[1:], points[2:]):
        a, b = toward(corner, prev, radius), toward(corner, nxt, radius)
        d += f" L {a[0]:g} {a[1]:g} Q {corner[0]:g} {corner[1]:g} {b[0]:g} {b[1]:g}"
    d += f" L {points[-1][0]:g} {points[-1][1]:g}"
    style = ' stroke-dasharray="7 5"' if dashed else ""
    marker = f' marker-end="url(#{tip})"' if head else ""
    return f'<path d="{d}" stroke="{BLUE}" stroke-width="{width}" fill="none"{style}{marker}/>'


def arrow(x1, y1, x2, y2):
    return path([(x1, y1), (x2, y2)])


def dot(x, y):
    return f'<circle cx="{x:g}" cy="{y:g}" r="4" fill="{BLUE}"/>'


def frame(height, top, sensors_y, actuators_y):
    bottom = height - 20
    gap = (AGENT_RIGHT + ENV_LEFT) / 2
    env_x, env_y = ENV_LEFT + ENV_WIDTH / 2, (top + bottom) / 2
    return "".join([
        f'<rect x="20" y="{top}" width="{AGENT_RIGHT - 20}" height="{bottom - top}" rx="22" fill="{AGENT_FILL}" '
        f'stroke="{BLUE}" stroke-width="2"/>',
        text(46, bottom - 24, "Agent", size=28, weight=900, family="Lato", fill=BLUE, anchor="start"),
        f'<rect x="{ENV_LEFT}" y="{top}" width="{ENV_WIDTH}" height="{bottom - top}" rx="22" fill="{ENV_FILL}" '
        f'stroke="{ENV_STROKE}" stroke-width="2"/>',
        text(env_x, env_y, "Environment", size=26, weight=900, family="Lato", fill=GREY,
             extra=f' transform="rotate(90 {env_x:g} {env_y:g})"'),
        text(BX, sensors_y, "Sensors", size=18, fill=GREY),
        arrow(ENV_LEFT, sensors_y, BX + 48, sensors_y),
        text(gap, sensors_y - 18, "Percepts", size=16, fill=SOFT_BLUE),
        text(BX, actuators_y, "Actuators", size=18, fill=GREY),
        arrow(BX + 52, actuators_y, ENV_LEFT, actuators_y),
        text(gap, actuators_y - 18, "Actions", size=16, fill=SOFT_BLUE),
    ])


def svg_sized(width, height, parts):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" '
            f'height="{height}"><defs>{fonts()}<marker id="tip" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto">'
            f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{BLUE}"/></marker><marker id="bigtip" viewBox="0 0 10 10" '
            f'refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="20" markerHeight="20" orient="auto">'
            f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{BLUE}"/></marker></defs>{"".join(parts)}</svg>\n')


def svg(height, parts):
    return svg_sized(WIDTH, height, parts)


def perception(with_model, to_prediction):
    left, right = PX + PILL_W / 2, BX - BOX_W / 2
    parts = [arrow(BX, SENSORS + 12, BX, A - BOX_H / 2), box(BX, A, ["What the world", "is like now"])]
    if with_model:
        upper, lower = A - 16, A + 16
        parts += [
            pill(STATE, "State"), pill(HOW, "How the world evolves"), pill(ACTIONS, "What my actions do"),
            arrow(left, upper, right, upper),
            path([(left, HOW), (BUS, HOW)], head=False), dot(BUS, HOW),
            path([(BX - 60, A - BOX_H / 2), (BX - 60, STATE - PILL_H / 2 - 18), (PX, STATE - PILL_H / 2 - 18),
                  (PX, STATE - PILL_H / 2)], dashed=True, radius=8),
        ]
        if to_prediction:
            # "What my actions do" sits on the row of the prediction and feeds it directly
            parts += [arrow(left, ACTIONS, right, ACTIONS), path([(BUS, ACTIONS), (BUS, lower), (right, lower)]),
                      dot(BUS, ACTIONS)]
        else:
            parts += [path([(left, ACTIONS), (BUS, ACTIONS), (BUS, lower), (right, lower)])]
    return parts


def decision(rule):
    return [pill(D, rule), arrow(PX + PILL_W / 2, D, BX - BOX_W / 2, D),
            box(BX, D, ["What action I", "should do now"], decision=True),
            arrow(BX, D + BOX_H / 2, BX, ACTUATORS - 12)]


def reflex(with_model):
    parts = [frame(560, 20, SENSORS, ACTUATORS)] + perception(with_model, to_prediction=False)
    parts += [arrow(BX, A + BOX_H / 2, BX, D - BOX_H / 2)] + decision("Condition-action rules")
    return svg(560, parts)


def goal_based():
    parts = [frame(560, 20, SENSORS, ACTUATORS)] + perception(True, to_prediction=True) + [
        arrow(BX, A + BOX_H / 2, BX, B - BOX_H / 2),
        box(BX, B, ["What it will be like", "if I do action A"]),
        arrow(BX, B + BOX_H / 2, BX, D - BOX_H / 2),
    ]
    return svg(560, parts + decision("Goals"))


def utility_based():
    parts = [frame(560, 20, SENSORS, ACTUATORS)] + perception(True, to_prediction=True) + [
        arrow(BX, A + BOX_H / 2, BX, B - BOX_H / 2),
        box(BX, B, ["What it will be like", "if I do action A"]),
        arrow(BX, B + BOX_H / 2, BX, C - BOX_H / 2),
        box(BX, C, ["How happy I will be", "in such a state"]),
        pill(C, "Utility"),
        arrow(PX + PILL_W / 2, C, BX - BOX_W / 2, C),
        arrow(BX, C + BOX_H / 2, BX, D - BOX_H / 2),
    ]
    return svg(560, parts + [
        box(BX, D, ["What action I", "should do now"], decision=True),
        arrow(BX, D + BOX_H / 2, BX, ACTUATORS - 12),
    ])


def learning():
    lx, lw, rx, rw, h = 175, 190, 500, 230, 64
    top, middle, bottom = 150, 310, 470
    parts = [
        frame(570, 70, top, bottom),
        text(lx, 32, "Performance standard", size=18, fill=GREY),
        arrow(lx, 46, lx, top - h / 2),
        box(lx, top, "Critic", w=lw, h=h),
        arrow(rx - 44, top, lx + lw / 2, top),
        arrow(lx, top + h / 2, lx, middle - h / 2),
        label(lx + 12, (top + h / 2 + middle - h / 2) / 2, "feedback"),
        box(lx, middle, ["Learning", "element"], w=lw, h=h),
        box(rx, middle, ["Performance", "element"], w=rw, h=h, decision=True),
        arrow(lx + lw / 2, middle - 16, rx - rw / 2, middle - 16),
        label((lx + lw / 2 + rx - rw / 2) / 2, middle - 34, "changes", anchor="middle"),
        arrow(rx - rw / 2, middle + 16, lx + lw / 2, middle + 16),
        label((lx + lw / 2 + rx - rw / 2) / 2, middle + 36, "knowledge", anchor="middle"),
        arrow(rx, top + 12, rx, middle - h / 2),
        arrow(lx, middle + h / 2, lx, bottom - h / 2),
        label(lx + 12, (middle + h / 2 + bottom - h / 2) / 2, "learning goals"),
        box(lx, bottom, ["Problem", "generator"], w=lw, h=h),
        path([(lx + lw / 2, bottom), (rx - 75, bottom), (rx - 75, middle + h / 2)]),
        arrow(rx, middle + h / 2, rx, bottom - 12),
    ]
    return svg(570, parts)


def loop():
    """Agent on top, environment below; actions go down on the right, percepts up on the left."""
    w, h, outer, margin = 250, 90, 90, 4
    left, right = margin + outer, margin + outer + w
    agent_y, env_y = margin + h / 2, margin + h / 2 + 170
    center = (left + right) / 2
    return svg_sized(right + outer + margin, env_y + h / 2 + margin, [
        f'<rect x="{left}" y="{agent_y - h / 2}" width="{w}" height="{h}" rx="18" fill="{AGENT_FILL}" '
        f'stroke="{BLUE}" stroke-width="2.5"/>',
        text(center, agent_y, "Agent", size=36, weight=900, family="Lato", fill=BLUE),
        f'<rect x="{left}" y="{env_y - h / 2}" width="{w}" height="{h}" rx="18" fill="{ENV_FILL}" '
        f'stroke="{ENV_STROKE}" stroke-width="2.5"/>',
        text(center, env_y, "Environment", size=36, weight=900, family="Lato", fill=GREY),
        path([(right, agent_y), (right + outer - 2, agent_y), (right + outer - 2, env_y), (right + 2, env_y)],
             radius=30, width=4, tip="bigtip"),
        path([(left, env_y), (left - outer + 2, env_y), (left - outer + 2, agent_y), (left - 2, agent_y)],
             radius=30, width=4, tip="bigtip"),
    ])


def main():
    figures = {
        "loop.svg": loop(),
        "simple-reflex-agent.svg": reflex(with_model=False),
        "model-based-reflex-agent.svg": reflex(with_model=True),
        "goal-based-agent.svg": goal_based(),
        "utility-based-agent.svg": utility_based(),
        "learning-agent.svg": learning(),
    }
    for name, content in figures.items():
        (ROOT / "figures" / "lec1" / name).write_text(content, encoding="utf-8")
        print(Path("figures") / "lec1" / name)


if __name__ == "__main__":
    main()
