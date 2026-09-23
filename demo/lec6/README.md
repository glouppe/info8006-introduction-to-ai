# Lecture 6 demos

Two demos for the filtering part of the lecture, plus the Ghostbusters game of
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

It imports `corner` and `mark_point` from `lampe.plots`, which is not in the
environment, so the plotting cells fail as committed.

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
