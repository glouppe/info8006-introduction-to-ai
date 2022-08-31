# Project 0
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
1. Depth-first search
2. Breadth-first search
3. Uniform-cost search
4. A-star

We recommend implementing those in this order in an incremental way.

The programming projects are adapted from [CS188 (UC Berkeley)](http://ai.berkeley.edu/project_overview.html).
