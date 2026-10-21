# Lecture 6 demos

Three demos for the filtering part of the lecture, plus the Ghostbusters game of
`demo/lec4/`, which plays the same story live.

## Forward-backward on the umbrella world

The matrix form of the lecture, run on the umbrella sequence
`[true, true, false, true, true]`: the forward messages, the backward messages,
and the smoothed distributions they multiply into.

```bash
uv run jupyter lab demo/lec6/forward-backward.ipynb
```

## Particle filter in a maze

A robot placed in a maze with no idea where it is, whose only sensor measures
the approximate distance to the nearest beacon. Its particles converge after a
few moves. Written by Martin J. Laubach (2011); it draws with `turtle`, so it
needs a screen.

```bash
cd demo/lec6/particle-filtering && uv run python particle_filter.py
```

The robot is the green turtle, the particles are the red and blue dots, and the
grey circle is the mean of the confident ones, which turns green once the
filter has found the robot.

## Kalman filter on a ball on a spring

The notebook of exercise session 5 (Ball on a spring): a linear-Gaussian model
of a ball on a spring in the wind, its transition and sensor matrices, and the
Kalman filter that tracks the position from noisy measurements.

```bash
uv run jupyter lab demo/lec6/kalman.ipynb
```

The corner plots of the three models come from `demo/lec6/plots.py`, written
for the notebook with numpy, scipy and matplotlib: the histogram of each
variable on the diagonal, the credible regions of each pair below it, and the
mean marked across the panels.

## Ghostbusters with a moving ghost

```bash
cd demo/lec4 && uv run python ghostbusters.py --cell 90 --ghost circles --beliefs
```

`t`, or the TIME+1 button, is the predict step; clicking a cell is the update
step. `--ghost random` spreads the belief fastest, `--ghost swirl` sits in
between.

## Pacman revenge

The maze demo of the two videos, where Pacman hunts ghosts it only senses
through noisy distances, is kept out of the repository: it is a worked Bayes
filter, which is what project 1 asks students to write. It lives in
`demo/lec6/pacman/`, ignored by git, and the commands to play it are in the
speaker notes of the two video slides.

## Kalman filter in orbit

A page embedded in the lecture: a spacecraft orbits the Moon, its position is
measured with Gaussian noise, and a Kalman filter tracks it, with the 2σ ellipse
of its estimate. The orbits are those of Apollo 11, drawn to scale: after the
first lunar orbit insertion burn (60.9 × 169.9 nautical miles, 113 × 315 km) and
after the circularization burn (about 54 × 66 nautical miles, 100 × 122 km),
both taking about two hours; a third, eccentric orbit is illustrative. The
measurements are simulated: Apollo was tracked from Earth by range and Doppler,
and those raw data are not published. Sliders set the measurement noise, the
process noise, the number of steps between measurements and the speed (minutes
of flight per second). The filter's transition model is gravity, linearized at
the estimate (an extended Kalman filter, the default), or constant velocity (a
Kalman filter, which lags outside the curved orbit: its model treats the
persistent pull of the Moon as zero-mean noise). "kick" pushes the spacecraft
with an impulse the filter does not know about. Plain JavaScript, no
dependencies; it replaces a Wolfram demonstration that needed a plugin.

Open `demo/lec6/orbit.html` from the served repository
(`uv run python -m http.server`), or from slide 62 of the deck.
