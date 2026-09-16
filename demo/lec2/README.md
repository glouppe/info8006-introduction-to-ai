# Lecture 2 demo: solving problems by searching

Pacman demonstrations shown during lecture 2, from the instructor's course
examples bundle (`IA - Chapter 2`, by Victor Mangeleer and Axelle Schyns).
Each agent solves the same maze with a different search strategy and reports
the score, the number of expanded nodes and the computation time.

## Running

From this directory, with the project environment:

```bash
uv run python run.py --agentfile dfs.py --layout ex --show 1
```

- `--agentfile`: `dfs.py`, `bfs.py`, `ucs.py`, `gs.py` (greedy), `astar0.py`
  (Euclidean), `astar1.py` (Manhattan), `astar2.py` (exact maze distance).
- `--layout`: `ex` (default, made for the demos), `small`, `medium`, `large`.
- `--show`: `1` draws Pacman's path, `0` does not.
- `--silentdisplay`: no window, prints the result table only.

The graphical display needs a screen; `--silentdisplay` is the headless
version, useful to check the demo still runs.

Every run rewrites a scratch file `temp` with `score;time;expanded nodes`.
It is git-ignored.

## What to show

Expanded nodes on `ex`, which is the point of the demo:

| Agent | Score | Expanded nodes |
| --- | --- | --- |
| `dfs.py` | 461 | 59 |
| `bfs.py` | 491 | 91 |
| `ucs.py` | 491 | 91 |
| `gs.py` | 481 | 39 |
| `astar0.py` | 491 | 57 |
| `astar1.py` | 491 | 54 |
| `astar2.py` | 491 | 19 |

Depth-first and greedy search expand few nodes but return a suboptimal path;
uniform-cost search is optimal but expands everything; A* is optimal and
expands fewer and fewer nodes as the heuristic gets closer to the true cost.
