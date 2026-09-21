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
- `--ghost`: how the ghost moves at each time step, `still` (default, lecture 4),
  `random`, `circles` or `swirl` (lecture 6).
- `--rows`, `--cols`: grid size, 6 by 10 by default, as in the videos.
- `--cell`: cell size in pixels, 70 by default. Use `--cell 90` on a projector.
- `--seed`: fix the ghost location and the sensor noise, to replay a game.

The window needs a screen; there is no headless mode.

| Key | Button | |
| --- | --- | --- |
| click | | read the sensor of a cell |
| `b` then click | BUST | bust, i.e. announce where the ghost is |
| `t` | TIME+1 | let one time step pass |
| `p` | | show or hide the beliefs |
| `n` | | new game |
| `q` | | quit |

Reading a sensor costs 1 point and so does a time step; busting the right cell
is worth 250 and the wrong one costs 250.

## The model

The sensor reports the color of the band of its Manhattan distance to the
ghost, and a neighboring color 20% of the time (`NOISE` in the code).

| Distance | 0 | 1 or 2 | 3 | 4 or more |
| --- | --- | --- | --- | --- |
| Color | red | orange | yellow | green |

The belief starts uniform over the 60 cells and is updated after each reading,
the readings being conditionally independent given the ghost location:

$$P(G \mid r_{1:k+1}) = \frac{1}{Z} P(r_{k+1} \mid G) \, P(G \mid r_{1:k}).$$

## Moving ghosts, for lecture 6

A time step moves the ghost according to its policy, and pushes the belief
through the same transition model,

$$P(G_{t+1} \mid r_{1:k}) = \sum_{g} P(G_{t+1} \mid g) \, P(g = G_t \mid r_{1:k}),$$

which is the prediction step of filtering, the update above being the
correction step. Together they are the Bayes filter of project 1.

| `--ghost` | |
| --- | --- |
| `still` | the ghost stays where it is (lecture 4) |
| `random` | it moves to one of its neighbors, or stays, uniformly |
| `circles` | it turns clockwise around the center, 80% of the time |
| `swirl` | it turns clockwise and drifts towards the center |

Each policy depends on the current cell only, so the filter is exact. Readings
are forgotten at each time step, since they describe where the ghost was.

Reading twice per time step and following the most likely cell, the belief
keeps 69% of its mass within one cell of a circling ghost, 53% of a swirling
one and 33% of a random one: the more predictable the ghost, the sharper the
belief, which is the point of the transition model.

## In class

Play blind first: a few readings, then ask the room where the ghost is and
bust that cell. Then press `p` and play again. The same readings now single
out one or two cells, which is the whole point of the lecture.
