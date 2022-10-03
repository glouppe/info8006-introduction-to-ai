# Project 2

## Deliverables

You are requested to deliver
- A `minimax.py` file containing your implementation of the Minimax algorithm, based on the `pacmanagent.py` template.
- A `hminimax.py` file containing your implementation of H-Minimax algorithm, based on the `pacmanagent.py` template.
- A `report.pdf` file, based on the `report.tex` template.

## Instructions

In [Project 1](../project1), Pacman could wander peacefully in the maze. Now, he needs to avoid a walking ghost that would kill him if it reached his position. Pacman **does not know what is the strategy of the ghost**, but he has access to the ghost's legal actions. In particular, a ghost can go forward, turn left or right, but cannot make a half-turn unless it has no other choice.

Several strategies are available for the ghost, as set through the `--ghost` option:
- `dumby` rotates on itself in a counterclockwise fashion until it can go on its left.
- `greedy` selects the action leading to the cell closest to Pacman.
- `smarty` selects the action leading to the shortest path towards Pacman.

Your task is to design an intelligent agent based on adversarial search algorithms (see [Lecture 3](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture3.md)) for maximizing the score. In this project, we will not consider layouts with capsules, but you may take them into account if you feel motivated. You can start by downloading the [archive](../project1.zip) of the project. In order to run you code, you can use the following command (replacing `humanagent.py` by `minimax.py` for example):
```console
$ python run.py --agent humanagent.py --ghost dumby --layout small_adv
```

### Code

TODO

### Report

In addition to `minimax.py` and `hminimax.py`, you are asked to submit a short (2 pages) report.

1. **Formalization** -- Formalize the game as an **adversarial search problem** by proposing a definition of its components (state, initial state, player function, actions, ...). For the utility function, assume the game as a **zero-sum game**. :warning: Do not make **references to the API** in the definition of the components.

2. **Minimax** -- Consider the direct application of Minimax to the game (assuming zero-sum).
  - 2.a. Is the completeness of Minimax guaranteed in this context? Why?
  - 2.b. From the point of view of Pacman, is there any advantage in going through a cycle, i.e. going back to a state that has already been visited?
  - 2.c. In this regard, how can you adapt the components described in the formalization to guarantee Minimax's completeness, while keeping the same set of optimal strategies?

3. **Heuristic** -- Describe formally and discuss the heuristic of your H-Minimax implementation.

## Evaluation

TODO
