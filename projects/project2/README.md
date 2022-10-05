# Project 2

## Deliverables

You are requested to deliver
- A `minimax.py` file containing your implementation of the Minimax algorithm, based on the `pacmanagent.py` template.
- A `hminimax.py` file containing your implementation of H-Minimax algorithm, based on the `pacmanagent.py` template.
- A `report.pdf` file, based on the `report.tex` template.

## Instructions

In [Project 1](../project1), Pacman could wander peacefully in the maze. Now, he needs to avoid a walking ghost that would kill him if it reached his position. Pacman **does not know what is the strategy of the ghost**, but he has access to the ghost's legal actions through the API. In particular, a ghost can go forward, turn left or right, but cannot make a half-turn unless it has no other choice.

Your task is to design an intelligent agent based on adversarial search algorithms (see [Lecture 3](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture3.md)) for **maximizing** the score of Pacman. You are asked to implement the **Minimax** and **H-Minimax** algorithms where Pacman and the ghost are the two players. We recommend to implement the algorithms in this order. It is mandatory to use only the [API](..#api) to retrieve game information. Layouts with capsules will not be considered, but you may take them into account if you feel motivated.

To get started, download and extract the [archive](../project2.zip?raw=true) of the project in the directory of your choice. Use the following command to run your Minimax implementation against the `dumby` ghost in the small layout:
```console
$ python run.py --agent minimax.py --ghost dumby --layout small_adv
```

Several strategies are available for the ghost:
- `dumby` rotates on itself counterclockwise until it can go to its left.
- `greedy` selects the action leading to the cell closest to Pacman.
- `smarty` selects the action leading to the shortest path towards Pacman.

### Report

In addition to `minimax.py` and `hminimax.py`, you are asked to submit a short (2 pages) report.

1. **Formalization** - Formalize the game as an **adversarial search problem** by proposing a definition of its components: state space, initial state, player function, actions, transition model, terminal test and utility functions. For the utility function, assume the game as a **zero-sum game**. :warning: Do not make **references to the API** in the definition of the components.

2. **Minimax** - Consider the direct application of Minimax to the game (assuming zero-sum).
  - 2.a. Is the completeness of Minimax guaranteed in this context? Why?
  - 2.b. From the point of view of Pacman, is there any advantage in going through a cycle, i.e. going back to a state that has already been visited?
  - 2.c. In this regard, how can you adapt the components described in the formalization to guarantee Minimax's completeness, while keeping the same set of optimal strategies?

3. **Heuristic/cut-off** - Describe formally and discuss the heuristic and cut-off of your H-Minimax implementation.

## Evaluation

Your project will be evaluated as follow:

- **Report** (20%): We evaluate the correctness and precision of your answers.
- **Minimax** (35%): We evaluate the optimality of your implementation on both public and private layouts.
- **H-Minimax** (40%): We evaluate the performance of your implementation on both public and private layouts. Both the score and the number of expanded nodes are taken into account.
- **Code style** (5%): No points are awarded if your code is not PEP-8 compliant.
