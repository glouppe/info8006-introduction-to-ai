"""Draw the Bayesian networks of lecture 6 in the style of the course.

    uv run python scripts/draw_temporal_networks.py

Writes to `figures/lec6/`:

- `markov-process.svg`, a first-order Markov chain X_{t-2} -> ... -> X_{t+2};
- `smoothing-dbn.svg`, the chain X_0, X_1, ..., X_k, ..., X_t with the evidence E_1, E_k, E_t;
- `weather-bn.svg`, the umbrella world with the CPTs of its transition and sensor models;
- `base-case-predict.svg` and `base-case-update.svg`, the two base cases X_1 -> X_2 and
  X_1 -> E_1, next to the CS188 cartoons cropped from the former `base-case2.png` and
  `base-case1.png` (`figures/lec6/base-case-ghosts.png`, `base-case-sensors.png`);
- `filtering.svg` and `smoothing.svg`, the umbrella world over two days, with the predicted,
  filtered, smoothed and backward messages for the evidence (true, true);
- `kalman-transition.svg` and `kalman-sensor.svg`, the transition X_t -> X_{t+1} and the sensor
  X_t -> E_t of the Kalman filter, at the same height so that they align side by side.

Variables are circles, shaded when observed; the rain and umbrella of the umbrella world
are written R and U, as in their tables, with the names as captions. Helpers and fonts are those of `draw_bn_diagrams.py`.
"""

import base64

from draw_bn_diagrams import BLUE, FILL, GREY, INK, ROOT, STROKE, arrow, cell, fonts, label, link, math, text

OUT = ROOT / "figures" / "lec6"


def node(x, y, name, sub=None, observed=False, r=36, bold=False, size=28):
    """A variable as a circle, shaded when observed."""
    fill = FILL if observed else "white"
    return (f'<circle cx="{x:g}" cy="{y:g}" r="{r}" fill="{fill}" stroke="{INK}" '
            f'stroke-width="{STROKE:g}"/>' + label(x, y, name, sub, size=size, bold=bold))


def dashed(p, q):
    return (f'<path d="M {p[0]:g} {p[1]:g} L {q[0]:g} {q[1]:g}" stroke="{INK}" stroke-width="{STROKE:g}" '
            f'stroke-dasharray="6 7" fill="none" marker-end="url(#head)"/>')


def svg(name, width, height, parts):
    head = (f'<marker id="head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" '
            f'orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="{INK}"/></marker>')
    out = OUT / f"{name}.svg"
    out.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" '
                   f'height="{height}"><defs>{fonts()}{head}</defs>{"".join(parts)}</svg>\n', encoding="utf-8")
    print(f"{out.relative_to(ROOT)}  {width}x{height}")


def markov_process():
    y, xs, subs = 50, [110, 280, 450, 620, 790], ["t−2", "t−1", "t", "t+1", "t+2"]
    r = 36
    parts = [arrow((10, y), (xs[0] - r, y)), arrow((xs[-1] + r, y), (895, y))]
    for x, sub in zip(xs, subs):
        parts.append(node(x, y, "X", sub, r=r, bold=True))
    for a, b in zip(xs, xs[1:]):
        parts.append(link((a, y), (b, y), (r, r), (r, r)))
    return parts


def smoothing_dbn():
    yx, ye, r = 45, 165, (36, 36)
    xs = {"0": 60, "1": 190, "k": 460, "t": 730}
    parts = [node(x, yx, "X", s, r=r[0], bold=True) for s, x in xs.items()]
    parts += [node(xs[s], ye, "E", s, observed=True, r=r[0], bold=True) for s in "1kt"]
    parts += [link((xs["0"], yx), (xs["1"], yx), r, r),
              dashed((xs["1"] + r[0], yx), (xs["k"] - r[0], yx)),
              dashed((xs["k"] + r[0], yx), (xs["t"] - r[0], yx)),
              arrow((xs["t"] + r[0], yx), (830, yx))]
    parts += [link((xs[s], yx), (xs[s], ye), r, r) for s in "1kt"]
    return parts


def table(x, y, head, rows, w=(70, 90)):
    """A CPT from its top left corner: a header row, then (value, probability) rows."""
    h0, h = 34, 30
    parts = [cell(x, y, w[0], h0, FILL), cell(x + w[0], y, w[1], h0, FILL),
             math(x + w[0] / 2, y + h0 / 2, head[0], size=19), math(x + w[0] + w[1] / 2, y + h0 / 2, head[1], size=19)]
    for k, (v, p) in enumerate(rows):
        yy = y + h0 + k * h
        parts += [cell(x, yy, w[0], h), cell(x + w[0], yy, w[1], h),
                  math(x + w[0] / 2, yy + h / 2, [(v, "i")], size=19), math(x + w[0] + w[1] / 2, yy + h / 2, [(p, "")], size=19)]
    return parts


def weather_bn():
    yr, yu, r = 150, 320, (36, 36)
    xs, subs = [210, 480, 750], ["t−1", "t", "t+1"]
    parts = [arrow((100, yr), (xs[0] - r[0], yr)), arrow((xs[-1] + r[0], yr), (880, yr)),
             text(10, yr, "rain", size=20, fill=GREY, anchor="start"),
             text(10, yu, "umbrella", size=20, fill=GREY, anchor="start")]
    for x, s in zip(xs, subs):
        parts += [node(x, yr, "R", s, r=r[0]), node(x, yu, "U", s, observed=True, r=r[0]),
                  link((x, yr), (x, yu), r, r)]
    for a, b in zip(xs, xs[1:]):
        parts.append(link((a, yr), (b, yr), r, r))
    rt1 = [("R", "i"), ("t−1", "s")]
    pr = [("P(", ""), ("R", "i"), ("t", "s"), (")", "")]
    parts += table(265, 10, (rt1, pr), [("true", "0.7"), ("false", "0.3")])
    rt = [("R", "i"), ("t", "s")]
    pu = [("P(", ""), ("U", "i"), ("t", "s"), (")", "")]
    parts += table(500, 180, (rt, pu), [("true", "0.9"), ("false", "0.2")])
    return parts


def cartoon(name, x, y, w, h):
    data = base64.b64encode((OUT / f"{name}.png").read_bytes()).decode()
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/png;base64,{data}"/>'


def base_cases():
    r = (36, 36)
    svg("base-case-predict", 560, 292, [
        cartoon("base-case-ghosts", 0, 0, 300, 292),
        node(370, 146, "X", "1", r=r[0]), node(500, 146, "X", "2", r=r[0]),
        link((370, 146), (500, 146), r, r)])
    svg("base-case-update", 560, 292, [
        cartoon("base-case-sensors", 0, 0, 300, 292),
        node(440, 70, "X", "1", r=r[0]), node(440, 222, "E", "1", observed=True, r=r[0]),
        link((440, 70), (440, 222), r, r)])


def pair(x, y, values, fill=INK):
    """A belief over (true, false), as two stacked numbers."""
    return [math(x, y, [(values[0], "")], size=22, fill=fill), math(x, y + 28, [(values[1], "")], size=22, fill=fill)]


def chain(xs, yr, yu, r=(36, 36)):
    parts = [text(40, yr, "rain", size=19, fill=GREY, anchor="start"),
             text(40, yu, "umbrella", size=19, fill=GREY, anchor="start")]
    for k, x in enumerate(xs):
        parts.append(node(x, yr, "R", str(k), r=r[0]))
        if k:
            parts += [node(x, yu, "U", str(k), observed=True, r=r[0]),
                      link((x, yr), (x, yu), r, r), link((xs[k - 1], yr), (x, yr), r, r)]
    return parts


def filtering():
    xs, yp, yf = [190, 450, 710], 30, 110
    parts = [text(40, yf, "true", size=19, fill=GREY, anchor="start"), text(40, yf + 26, "false", size=19, fill=GREY, anchor="start")]
    parts += pair(xs[0], yf, ("0.500", "0.500"), BLUE)
    for x, pred, filt in [(xs[1], ("0.500", "0.500"), ("0.818", "0.182")), (xs[2], ("0.627", "0.373"), ("0.883", "0.117"))]:
        parts += pair(x, yp, pred, GREY) + pair(x, yf, filt, BLUE)
        parts.append(arrow((x, yp + 40), (x, yf - 16)))
    parts += [arrow((xs[0] + 40, yf + 10), (xs[1] - 40, yp + 10)), arrow((xs[1] + 40, yf + 10), (xs[2] - 40, yp + 10))]
    parts += [text(830, yp + 13, "predicted", size=17, fill=GREY, anchor="start"),
              text(830, yf + 13, "filtered", size=17, fill=GREY, anchor="start")]
    return parts + chain(xs, 220, 340)


def smoothing():
    xs, yp, yf, ys, yb = [190, 450, 710], 30, 110, 190, 270
    parts = [text(40, yf, "true", size=19, fill=GREY, anchor="start"), text(40, yf + 26, "false", size=19, fill=GREY, anchor="start")]
    parts += pair(xs[0], yf, ("0.500", "0.500"), BLUE)
    for x, pred, filt in [(xs[1], ("0.500", "0.500"), ("0.818", "0.182")), (xs[2], ("0.627", "0.373"), ("0.883", "0.117"))]:
        parts += pair(x, yp, pred, GREY) + pair(x, yf, filt, BLUE) + pair(x, ys, ("0.883", "0.117"), INK)
        parts += [arrow((x, yp + 40), (x, yf - 16)), arrow((x, yf + 40), (x, ys - 16)), arrow((x, yb - 14), (x, ys + 42))]
    parts += pair(xs[1], yb, ("0.690", "0.410"), GREY) + pair(xs[2], yb, ("1.000", "1.000"), GREY)
    parts += [arrow((xs[0] + 40, yf + 10), (xs[1] - 40, yp + 10)), arrow((xs[1] + 40, yf + 10), (xs[2] - 40, yp + 10)),
              arrow((xs[2] - 40, yb + 13), (xs[1] + 40, yb + 13))]
    for y, name in [(yp, "predicted"), (yf, "forward"), (ys, "smoothed"), (yb, "backward")]:
        parts.append(text(830, y + 13, name, size=17, fill=GREY, anchor="start"))
    return parts + chain(xs, 380, 500)


def kalman():
    r = (36, 36)
    svg("kalman-transition", 240, 220, [
        node(40, 110, "X", "t", r=36, bold=True), node(200, 110, "X", "t+1", r=36, bold=True),
        link((40, 110), (200, 110), r, r)])
    svg("kalman-sensor", 96, 220, [
        node(48, 40, "X", "t", r=36, bold=True), node(48, 180, "E", "t", observed=True, r=36, bold=True),
        link((48, 40), (48, 180), r, r)])


if __name__ == "__main__":
    svg("markov-process", 900, 100, markov_process())
    svg("smoothing-dbn", 840, 210, smoothing_dbn())
    svg("weather-bn", 900, 370, weather_bn())
    base_cases()
    svg("filtering", 940, 380, filtering())
    svg("smoothing", 940, 540, smoothing())
    kalman()
