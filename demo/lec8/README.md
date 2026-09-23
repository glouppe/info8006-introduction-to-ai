# Lecture 8 demo: solving the grid world

The $3 \times 4$ grid world of the slides, solved step by step: the MDP first
(noisy actions, $R(s) = -0.04$ off the terminal states, $\gamma = 1$), then
value iteration, policy extraction, and policy iteration.

## Running

From the repository root, with the project environment:

```bash
uv run jupyter lab demo/lec8/mdp.ipynb
```

The notebook only needs `numpy`.

## What it shows

| Algorithm | Iterations to converge |
| --- | --- |
| Value iteration, stopping at $\lVert V\_{i+1} - V\_i \rVert < 10^{-3}$ | 20 |
| Policy iteration, 20 evaluation updates per step | 3 |

Both return the utilities of the slides,

```
 0.812  0.868  0.918   1.000
 0.762  XXXXX  0.660  -1.000
 0.705  0.655  0.611   0.387
```

and the optimal policy drawn beside them, which goes around the $-1$ state
rather than past it.
