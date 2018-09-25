# Pacman Project


<p align="center">
<img src="https://github.com/glouppe/info8006-introduction-to-ai/blob/pacman_project/pacman/pacman_game.png" width="50%"/>
</p>
The project is split into three parts. Your task is to design an intelligent agent for each part of the project.

In this classical Pacman game, the player navigates Pacman through a maze filled of food dots. The goal is to collect them all in a minimum amount of time (Part 1/3). Ghosts, which are Pacman's enemies, may also be part of the game. In this configuration, Pacman needs to avoid them while collecting all the food dots (Part 2/3). To help him, Pacman may have access to capsules in the maze, giving him the ability to eat scared ghosts, resetting them to their initial state (i.e., to their initial position and not scared anymore), in a short amount of time. The game ends if either Pacman have collected all the dots (*winning end*) or Pacman collides with one of the Ghosts (*losing end*). Cherry on the cake, some walls on the game may randomly be crossed or not over time (Part 3/3).

See sections below for installation, usage and project instructions.
# Table Of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Score function](#score-function)
- [Instructions](#instructions)
  * [Search Agent (Part 1/3)](#search-agent--part-1-3-)
  * [Search Agent Against Ghosts (Part 2/3)](#search-agent-against-ghosts--part-2-3-)
  * [Search Agent Against Ghosts With Blinking Walls (Part 3/3)](#search-agent-against-ghosts-with-blinking-walls--part-3-3-)
  * [Computation Node Budget](#computation-node-budget)
  * [Illegal Moves](#illegal-moves)
  * [Helpers](#helpers)
  * [Evaluation](#evaluation)
- [Credits](#credits)

# Installation


All the instructions below have been tested under Windows, Linux and MacOS.

 - See [Anaconda webpage](https://conda.io/docs/user-guide/install/index.html) for instructions to install Anaconda/Miniconda (recommended).

 - Open the Anaconda prompt (Windows) or a Terminal (Linux/MacOS)

 - (Linux/MacOS) Create your own Anaconda environment and activate it.
```bash
conda create -n <env_name> python=3.6
source activate <env_name>
```

 - (Windows) Create your own Anaconda environment and activate it.
```bash
conda create -n <env_name> python=3.6
activate <env_name>
```

From now, it is assumed that <env_name> is activated.

 - Install dependencies.
```bash
pip install -U numpy
```

# Usage



 - Display the command-line help section
```bash
python run.py -h
```

 - Interactive game.
```bash
python run.py
```

 - Silent game.
```bash
python run.py --silentdisplay
```

 - Launches a game with a random agent in default map mediumClassic:
```bash
python run.py
```

 - Launches a game with your Pacman agent class, named PacmanAgent located in `youragentmodule.py`, and with the maze `originalClassic` (see layout folder).
```bash
python run.py --layout originalClassic --agentfile youragentmodule.py
```

 - Same configuration as above but in *online setting* with a limit of 100 node expansions per call to ` get_action `.
```bash
python run.py --layout originalClassic --agentfile youragentmodule.py --expout 100
```




See the help section of the command line for more information about the parameters.

# Score function

The score function is computed as follows:

`score = -#time steps + 10*#number of eaten food dots + 200*#number of eaten ghost + (-500 if #losing end) + (500 if #winning end)`.

# Instructions

For each part of the project, you need to provide the following deliverables :

 - The source code of your intelligent agent. Complete this [class template](https://github.com/glouppe/info8006-introduction-to-ai/blob/pacman_project/pacman/pacmanagent.py) to do so. If you have written separate modules, provide them in a subfolder.
 - A report in PDF format of 4 pages max.

The whole project must be done in group of 2 students (same group across all parts). Submit your deliverables as an archive in the [Montefiore Submission Platform](https://submit.montefiore.ulg.ac.be/teacher/courseDetails/INFO8006/).

## Search Agent (Part 1/3)
This part is due to Oct 28,2018.

In this part, only food dots are included in mazes. The purpose of this part is to design an intelligent agent, based on the search algorithms seen during [Lecture 2](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture2.md).


You are asked to implement the following an agent based on each of these search algorithms:

 - Depth-First Search (DFS) ,
 - Breadth-First Search (BFS) ,
 - Uniform Cost Search (UCS),
 - A* (and an associated heuristic of your choice).

Each agent should be implemented in a different python file (DfsAgent.py, BfsAgent.py, UcsAgent.py, AStarAgent.py) using this [class template](https://github.com/glouppe/info8006-introduction-to-ai/blob/pacman_project/pacman/pacmanagent.py). Be careful, the A* implementation should take into account both *online setting* (possible early stopping of the search) and *offline setting*, as described [there](#computation-time-budget).


Your report should be organised into 4 parts. First you should formalize this game configuration as a search problem, as seen in [Lecture 2](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture2.md). Secondly, you should run your agents against the maze layouts located in this [folder](https://github.com/glouppe/info8006-introduction-to-ai/tree/pacman_project/pacman/PacmanGym/layouts) in the *offline setting*. For each run, display the performance in terms of  [final score](#score-function), total computation time and total number of expanded nodes. Then, you should run ONLY your A* agent in the *online setting* in the same maze layouts. For each run, display the performance in terms of [final score](#score-function), and compare them to the performance of your A* agent in the *offline setting*. Finally, conclude your report by a discussion over the performance and the limits of your agent, and possible improvements of your approach.

## Search Agent Against Ghosts (Part 2/3)

Coming soon

## Search Agent Against Ghosts With Blinking Walls (Part 3/3)

Coming soon

## Computation Node Budget

The computation budget of the agent is expressed in terms of number of node expansions. We refer to an *offline* setting when this number is unlimited, and to an *online* setting when this number is limited. When the number of expansions in ```get_action``` exceeds the fixed computation budget, the expansion of any node is not allowed anymore (see [there](#helpers)) . During evaluation process, the following budgets are considered for the *online* setting : *TBD*.
:warning: Do not alter in any way the node budget control during the ```get_action``` call. This is checked and your project won't be graded if this is detected.

## Illegal Moves

You need to ensure that your agent always returns a legal move. If it is not the case, the game engine ignores it and repeat the previous move as long as it remains legal. Otherwise, it just keep getting stuck in the same location.

## Helpers

Implementation examples are provided [there](https://github.com/glouppe/info8006-introduction-to-ai/tree/pacman_project/pacman). In particular, the method ```get_action``` gets the current state ``` s ``` at each turn of the game. Useful methods of the state are specified below :

 - ```s.getLegalActions(agentIndex)``` : Returns a list of legal moves given the state ```s``` and the agent indexed by ```agentIndex```. 0 is always the Pacman agent.
 - ```s.generatePacmanSuccessors()``` : Returns a list of pairs of successor states and moves given the current state ```s``` for the pacman agent.
	* *Must* be called for any node expansion, otherwise your project won't be graded.
	* In the *online setting*, when the number of expansions exceeds the computation budget, ```None``` is always returned.
 - ```s.getPacmanPosition()``` : Returns the Pacman position in a ```(x,y)``` pair.
 - ```s.getScore()``` : Returns the total score of a state, computed from the function described in [final score](#score-function).
 - ```s.getFood()``` : Returns a boolean matrix which gives the position of all food dots.
 - ```s.getWalls()``` : Returns a boolean matrix which gives the position of all walls.
 - ```s.getGhostPositions()``` : Returns the position of all ghosts in the maze.
 - ```s.getCapsules()``` : Returns a list of positions of the remaining capsules in the maze.
 - ```s.isWin()``` : Returns True if the state is in a *winning end*.
 - ```s.isLose()``` : Returns True if the state is in a *losing end*.

## Evaluation

The evaluation of your deliverables is based on the following criteria :

- Clarity of your report
	* Avoid long and vague sentences and be straight to the point. Ideally, the length of each sentence should not exceed a line.
	* Do not hesitate to illustrate with examples.
	* Do not overload your graphics, and write short and clear captions. The reader should understand them in a quick look.
	* Lack of structure leads to lack of clarity. We recommend you to design your report outline on top of the one described in the previous section.
- Clarity and structure of the source code
	* Avoid single-file long code source, and prefers to use a multiple-files modular architecture.
	* Name your variables-attributes-classes according to their usage. Comment your code so that explanations are concise and clear enough to allow the reader to understand the semantics in a quick look.
	* Your source code needs to follow the [PEP-8](https://www.python.org/dev/peps/pep-0008/) conventions.
		- Install and use pycodestyle to check that a given Python script follows PEP-8 conventions :
			```bash
			pip install -U pycodestyle
			pycodestyle <yourscript>.py
			```

These criterions are all importants. We particularly value well written reports and code documentation.

:warning: Plagiarism is checked and sanctioned by a 0 grade.

# Credits

Credits: [UC Berkeley](http://ai.berkeley.edu/project_overview.html)
