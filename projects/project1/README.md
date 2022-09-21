# Project 1

## Deliverables

You are requested to deliver a *zip* archive containing:
 - Your `astar.py` file containing your implementation of A\* algorithm.
	 - Put the class template defined in `pacmanagent.py` into `astar.py` and fill in the `get_action` function.
 - Your `bfs.py` file containing your implementation of BFS algorithm.
	 - Put the class template defined in `pacmanagent.py` into `bfs.py` and fill in the `get_action` function.
   
No report is required.

## Instructions

You can download the **[archive](https://github.com/glouppe/info8006-introduction-to-ai/raw/master/projects/project0.zip)** of the project into a directory of your choice. In this first part of the project, only food dots, capsules and Pacman are in the maze.
Your task is to design an intelligent agent based on search algorithms (see [Lecture 2](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture2.md)) for maximizing the score.

To help you, we provide base code to implement an agent in the Python file `dfs.py`. Once you have activated your Pacman environment (see our [Python tutorial](https://github.com/glouppe/info8006-introduction-to-ai/tree/master/python-tutorial#creating-a-conda-environment)), you can test DFS algorithm using the following commands:
```bash
python run.py --agentfile dfs.py --layout medium
```
When you want to test one of your implementation, just replace the script parameter `dfs.py` by the name of the file of the agent you want to test. Refer to the [usage section](https://github.com/glouppe/info8006-introduction-to-ai/blob/master/projects/README.md#usage) for more details about the game parameters.

Reminder: it is mandatory to use only the [API](https://github.com/glouppe/info8006-introduction-to-ai/tree/master/projects#api) to retrieve game information.

You are asked to implement the following algorithms:
1. Breadth-first search
2. A-star

We recommend implementing those in this order in an incremental way.

The programming projects are adapted from [CS188 (UC Berkeley)](http://ai.berkeley.edu/project_overview.html).

## Evaluation
In this section, you can find the criteria according to which the different questions will be evaluated, as well as some additional form evaluations of your code.

Each of your codes will be evaluated against new mazes, some being designed to test the common pitfalls. Passing the public tests does not mean that your code is perfect and that you will get the highest grades. The criteria are the following:

* **BFS** (20%)
  If implemented correctly, your implementation should return the same score as our and roughly expand the same amount of nodes. We will take both these criteria into account.

* **A-star** (75%)
   A well-implemented A-star algorithm should return the optimal solution no matter the maze structure. The number of expanded nodes needed to find an      optimal solution depends on the quality of the heuristic. We will check if the optimal solution is returned on all tested maze and will also take the    number of expanded nodes into account (the lower the better).

* **Code style** (5%)
  - 100%: The source code is PEP8 formatted
  - 0%: At least one error was raised when checking PEP8 compatibility
