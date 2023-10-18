# Project 2

## Deliverables

You are requested to deliver
- A `minimax.py` file containing your implementation of the Minimax algorithm, based on the `pacmanagent.py` template.
- A `hminimax.py` file containing your implementation of H-Minimax algorithm, based on the `pacmanagent.py` template.

## Instructions

In [Project 1](../project1), Pacman could wander peacefully in the maze. Now, he needs to avoid a walking ghost that would kill him if it reached his position. Pacman **does not know what is the strategy of the ghost**, but he has access to the ghost's legal actions through the API. In particular, a ghost can go forward, turn left or right, but cannot make a half-turn unless it has no other choice.

Your task is to design an intelligent agent based on adversarial search algorithms (see [Lecture 3](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture3.md)) for **maximizing** the score of Pacman. You are asked to implement the **Minimax** and **H-Minimax** algorithms where Pacman and the ghost are the two players. We recommend to implement the algorithms in this order. It is mandatory to use only the [API](..#api) to retrieve game information. Layouts with capsules will not be considered, but you may take them into account if you feel motivated. Your implementation of Minimax does not need to run on the `medium_adv` and `large_adv` layouts.

To get started, download and extract the [archive](../project2.zip?raw=true) of the project in the directory of your choice. Use the following command to run your Minimax implementation against the `dumby` ghost in the small layout:
```console
$ python run.py --agent minimax --ghost dumby --layout small_adv
```

Several strategies are available for the ghost:
- `dumby` rotates on itself counterclockwise until it can go to its left.
- `greedy` selects the action leading to the cell closest to Pacman. If several actions are equivalent, `greedy` chooses randomly among them.
- `smarty` selects the action leading to the shortest path towards Pacman.

The random seed of the game can be changed with the `--seed` option (e.g. `--seed 42`).

## Evaluation

Your project will be evaluated as follow:

- **Minimax** (45%): We evaluate the optimality of your implementation on both public and private layouts.
- **H-Minimax** (50%): We evaluate the performance of your implementation on both public and private layouts. Both the score and the number of expanded nodes are taken into account.
- **Code style** (5%): No points are awarded if your code is not PEP-8 compliant.
