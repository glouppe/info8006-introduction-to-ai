# Lecture 4 demo: Ghostbusters

The game of the two videos of lecture 4, to play live in class. A ghost hides
in the grid; clicking a cell reads its noisy sensor, which reports a color
telling how far the ghost is. The two videos are the same game: in the first
one the player guesses from the colors alone, in the second the posterior
$P(G \mid r_{1:k})$ is maintained by Bayes' rule and shown in every cell,
which makes the ghost easy to find.

Press `p` to switch between the two.

## Running

From this directory, with the project environment:

```bash
uv run python ghostbusters.py
```

- `--beliefs`: start with the beliefs shown (they are hidden by default).
- `--rows`, `--cols`: grid size, 6 by 10 by default, as in the videos.
- `--cell`: cell size in pixels, 70 by default. Use `--cell 90` on a projector.
- `--moving`: the ghost moves one cell per time step, pressed with `t`.
- `--seed`: fix the ghost location and the sensor noise, to replay a game.

The window needs a screen; there is no headless mode.

| Key | |
| --- | --- |
| click | read the sensor of a cell |
| `b` then click | bust, i.e. announce where the ghost is |
| `p` | show or hide the beliefs |
| `t` | let one time step pass (with `--moving`) |
| `n` | new game |
| `q` | quit |

Reading a sensor costs 1 point, busting the right cell is worth 250 and the
wrong one costs 250.

## The model

The sensor reports the color of the band of its Manhattan distance to the
ghost, and a neighboring color 20% of the time (`NOISE` in the code).

| Distance | 0 | 1 or 2 | 3 | 4 or more |
| --- | --- | --- | --- | --- |
| Color | red | orange | yellow | green |

The belief starts uniform over the 60 cells and is updated after each reading,
the readings being conditionally independent given the ghost location:

$$P(G \mid r_{1:k+1}) = \frac{1}{Z} P(r_{k+1} \mid G) \, P(G \mid r_{1:k}).$$

With `--moving`, a time step also pushes the belief through the transition
model, the ghost moving to one of its neighbors or staying put, uniformly.
That is the filtering of lecture 6, and the Bayes filter of project 1.

## In class

Play blind first: a few readings, then ask the room where the ghost is and
bust that cell. Then press `p` and play again. The same readings now single
out one or two cells, which is the whole point of the lecture.
