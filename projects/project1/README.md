# Project 1

## Deliverables

You are requested to deliver
- A `minimax.py` file containing your implementation of the Minimax algorithm, based on the `pacmanagent.py` template.
- A `hminimax.py` file containing your implementation of H-Minimax algorithm, based on the `pacmanagent.py` template.

## Instructions

In [Project 0](../project0), Pacman could wander peacefully in the maze. Now, he needs to avoid a walking ghost that would kill him if it reached his position. Pacman **does not know what is the strategy of the ghost**, but he has access to the ghost's legal actions through the API. In particular, a ghost can go forward, turn left or right, but cannot make a half-turn unless it has no other choice.

Your task is to design an intelligent agent based on adversarial search algorithms (see [Lecture 3](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture3.md)) for **maximizing** the score of Pacman. You are asked to implement the **Minimax** and **H-Minimax** algorithms where Pacman and the ghost are the two players. We recommend to implement the algorithms in this order. It is mandatory to use only the [API](..#api) to retrieve game information. Layouts with capsules will not be considered, but you may take them into account if you feel motivated. Your implementation of Minimax does not need to run on the `medium_adv` and `large_adv` layouts.

To get started, download and extract the [archive](../project1.zip?raw=true) of the project in the directory of your choice. Use the following command to run your Minimax implementation against the `dumby` ghost in the small layout:
```console
$ python run.py --agent minimax --ghost dumby --layout small_adv
```

Several strategies are available for the ghost:
- `dumby` rotates on itself counterclockwise until it can go to its left.
- `greedy` selects the action leading to the cell closest to Pacman. If several actions are equivalent, `greedy` chooses randomly among them.
- `smarty` selects the action leading to the shortest path towards Pacman.

The random seed of the game can be changed with the `--seed` option (e.g. `--seed 42`).

## Evaluation

Your project will be evaluated on both public and private layouts. When submitting your project, you will see the results of public tests. Those are made on public layouts only and warn you if big issues are encountered, such as code crashing or severe issues with your algorithm. Your final grade will be computed based on private tests that are invisible to you when submitting your project. Those tests are made on private layouts that differ from public layouts. Public layouts are very basic layouts that are designed to test your algorithm's general performance, while private layouts are designed to make your agent fail if some implementation errors have been made. Therefore, **we encourage you to make your own tests** to test for edge cases that you might encounter during the private testing phase. The points allocated to each part of the project are the following:

- **Minimax** (45%): We evaluate the optimality of your implementation on both public and private layouts. A layout is considered successful if your agent obtains the best possible score on it. Your grade is the proportion of successful layouts.
- **H-Minimax** (50%): We evaluate the performance of your implementation on both public and private layouts. Both the score and the number of expanded nodes are taken into account. For each layout, an upper and lower threshold are set for both the score and the number of expanded nodes for each ghost. If the score is lower than the low threshold or the number of expanded nodes is higher than the high threshold for any ghost, the layout is considered as failed, and the maximum point penalty is applied. This means that your agent should at least obtain a reasonable score with a reasonable number of nodes expanded for all ghosts. If that condition is met, then your grade for that layout is based on the distance between your score and the high score threshold as well as the distance between the amount of expanded nodes of your agent and the low nodes threshold for each ghost. If your agent gets a higher score than the high threshold while expanding a lower amount of nodes than the low nodes threshold for all ghosts, then you obtain the maximal grade for that layout. In the public tests, we only warn you if your code fails, your agent has a score that is way lower than expected, or if your agent expands way too many nodes.
- **Code style** (5%): You are awarded the maximal grade if your code is PEP-8 compliant and no points otherwise. This test is public.
