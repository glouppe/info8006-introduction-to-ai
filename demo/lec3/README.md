# Lecture 3 demo: games and adversarial search

Pacman demonstrations shown during lecture 3, from the instructor's course
examples bundle (`IA - Chapter 3`). Pacman searches the game tree against one
or more ghosts, with the search depth and the evaluation function chosen on
the command line.

## Running

From this directory, with the project environment:

```bash
uv run python run.py --agentfile hminimax.py --pdepth 4 --nghosts 2 --slowmo on
```

- `--agentfile`, one of the three agents of `SearchMethods/`:
  - `hminimax.py`, h-minimax with the plain evaluation ("the closer to the
    dot, the better");
  - `hminimax_ADV.py`, h-minimax with an evaluation that also keeps away from
    the ghost, and stops the search early on a dot that can be eaten safely;
  - `expectimax.py`, the same as `hminimax_ADV.py` except at ghost nodes,
    where it takes the average instead of the minimum, i.e. it assumes a ghost
    moving at random.

  The search itself is in `SearchMethods/search.py`; the three files above set
  the evaluation, the cutoff and what happens at a ghost node.
- `--pdepth`: the depth at which Pacman cuts off the search.
- `--ghostagent`: `smarty` (default), `greedy`, `dumby`, `rightrandy`, or
  `cheeky`. A cheeky ghost searches the game tree itself, to the depth given
  by `--gdepth`. `rightrandy` goes east with probability `--p` and moves
  uniformly at random otherwise, so `--p 0` is a purely random ghost.
- `--layout`: `EH1` (default, for the horizon effect), `EH2`, `small_adv`,
  `medium_adv`, `large_adv`.
- `--slowmo on`: slow the game down so that it can be commented.
- `--silentdisplay`: no window, prints the result table only.

## What to show

### The horizon effect

On the default layout against two ghosts:

| Agent | Score | Expanded nodes |
| --- | --- | --- |
| `hminimax.py --pdepth 2` | -506 | 16 |
| `hminimax.py --pdepth 10` | 500 | 639 |
| `hminimax_ADV.py --pdepth 2` | 500 | 16 |
| `hminimax_ADV.py --pdepth 10` | 500 | 23 |

At depth 2 Pacman loses: the consequences of its moves lie beyond its
horizon. At depth 10 it wins, but expands forty times more nodes. A better
evaluation function wins at both depths, and at depth 10 it expands 23 nodes
instead of 639 — the same lesson as a good heuristic in lecture 2.

### Mismodelling the opponent

The same Pacman, the same maze, the same ghost: only the assumption about the
ghost changes. Against an adversarial ghost, assuming it plays against you
wins and assuming it moves at random gets you eaten.

```bash
# Assumes an adversarial ghost, and faces one: wins, 505
uv run python run.py --agentfile hminimax_ADV.py --pdepth 6 \
    --ghostagent cheeky --gdepth 2 --layout small_adv

# Assumes a random ghost, and faces the same adversarial one: dies, -501
uv run python run.py --agentfile expectimax.py --pdepth 6 \
    --ghostagent cheeky --gdepth 2 --layout small_adv
```

The other two cases of the section, where the assumption holds, are run
against `--ghostagent rightrandy --p 0`; both agents win there, so the pair
above is the one that makes the point. On `medium_adv` and `large_adv` the
better evaluation keeps Pacman out of trouble whatever it assumes, which is
why the contrast is shown on `small_adv`.

## Known quirks

- `--seed` is parsed but never used, so games against `rightrandy` differ from
  one run to the next.
