# Pacman

<p align="center">
<img src="http://github.com/glouppe/info8006-introduction-to-ai/blob/pacman_project/pacman/pacman_game.png" width="50%" />
</p>

The goal of this programming project is to implement intelligent agents for the game of Pacman. The project is divided into three parts:
- **Part 1.** You must implement a Search agent for eating all the food dots as quickly as possible.
- **Part 2.** You must implement a Minimax agent for eating all the food dots as quickly as possible, while avoiding the ghost enemies that are chasing you.
- **Part 3.** You must implement a MDP agent for eating all the food dots as quickly as possible, while avoiding the ghost enemies that are chasing you. In addition, some of the walls appear and disappear at random.


## Table of contents

- [Installation](#installation)
    * Setup
    * Install
- [Instructions](#instructions)
    * [Part 1: Search agent](#search-agent--part-1-3-)
    * [Part 2: Minimax agent](#search-agent-against-ghosts--part-2-3-)
    * [Part 3: MDP agent](#search-agent-against-ghosts-with-blinking-walls--part-3-3-)
- [FAQ](#helpers)
    * Score
    * API
    * Illegal moves
- [Evaluation](#evaluation)
- [Credits](#credits)

---

## Installation

The instructions below have been tested under Windows, Linux and MacOS.

We recommend to install a Python environment using the Anaconda distribution. Further instructions can be found on the [Anaconda user guide](https://conda.io/docs/user-guide/install/index.html). Once installed, open the Anaconda prompt (Windows) or a terminal (Linux/MacOS).

### Setup

(Linux/MacOS) Create a `pacman` environment and activate it:
```bash
conda create -n pacman python=3.6
source activate pacman
```

(Windows) Create a `pacman` environment and activate it:
```bash
conda create -n pacman python=3.6
activate pacman
```

From now, it is assumed that `pacman` is activated.

Dependencies should be installed through `conda`:
```bash
conda install numpy XXXXXXXX
```

### Usage

Start the game with a Pacman agent controlled by the keyboad (keys `j`, `l`, `i`, `k`):
```bash
python run.py
```

**Options**:

`--agentfile`: Start the game with a Pacman agent following a user-defined control policy:
```bash
python run.py  --agentfile randomagent.py
```

`--silentdisplay`: Disable the graphical user interface:
```bash
python run.py --silentdisplay
```

`--layout`: Start the game with a user-specifed layout for the maze (see the `/layouts/` folder):
```bash
python run.py --layout originalClassic
```

`-h`: For further details, check the command-line help section:
```bash
python run.py -h
```

---

## Instructions

For each part of the project, you must provide the following deliverables:

- The source code of your intelligent agent(s).  
- A report in PDF format of 4 pages max.

The whole project must be carried out in groups of 2 students (with the same group across all parts).

You deliverables must be submitted as an archive on the [Montefiore submission platform](https://submit.montefiore.ulg.ac.be/teacher/courseDetails/INFO8006/).

### Part 1: Search agent

This part is due on **October 28, 2018 at 23:59**.

In this first part of the project, only food dots are included in the maze. No ghost is present.
Your task is to design an intelligent based on search algorithms (see [Lecture 2](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture2.md)) for eating all the dots as quickly as possible.

You are asked to implement an agent based on each of these search algorithms:
 - Depth-First Search (DFS)
 - Breadth-First Search (BFS)
 - Uniform Cost Search (UCS)
 - A* (and an associated heuristic of your choice).

Each agent should be implemented as a `PacmanAgent` class. Each should be specified in a different Python file (`dfs.py`, `bfs.py`, `ucs.py`, `astar.py`), following the template of `pacmanagent.py`.

Your report should be organized into 3 parts:
1. You must formalize the game as a search problem, as seen in [Lecture 2](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture2.md).
2. You should run your agents against the 3 maze layouts located the  `/layouts/` folder.
  For each layout, report as a bar plot the performance of your 4 agents in terms of i) final score, ii) total computation time and iii) total number of expanded nodes. In total, you should therefore produce 9 bar plots.
3. Discuss the performance and limitations of your agents, and possible improvements of your approach.

## Part 2: Minimax agent

TBD.

## Part 3: MDP agent

TBD.

---

## FAQ

### Score

The score function of the game is computed as follows:

`score = -#time steps + 10*#number of eaten food dots + 200*#number of eaten ghost + (-500 if #losing end) + (500 if #winning end)`.

We ask you to implement an agent that maximizes this function.

### API

Implementation examples are provided [there](https://github.com/glouppe/info8006-introduction-to-ai/tree/pacman_project/pacman). In particular, the method ```get_action``` of the `PacmanAgent` class gets the current state ``` s ``` at each turn of the game.

Useful methods of the state are specified below:

 - ```s.getLegalActions(agentIndex)``` : Returns a list of legal moves given the state ```s``` and the agent indexed by ```agentIndex```. 0 is always the Pacman agent.
 - ```s.generatePacmanSuccessors()``` : Returns a list of pairs of successor states and moves given the current state ```s``` for the pacman agent.
	* This method **must** be called for any node expansion, otherwise your project will not be graded.
 - ```s.getPacmanPosition()``` : Returns the Pacman position in a ```(x,y)``` pair.
 - ```s.getScore()``` : Returns the total score of a state, computed from the function described in [final score](#score-function).
 - ```s.getFood()``` : Returns a boolean matrix which gives the position of all food dots.
 - ```s.getWalls()``` : Returns a boolean matrix which gives the position of all walls.
 - ```s.getGhostPositions()``` : Returns the position of all ghosts in the maze.
 - ```s.getCapsules()``` : Returns a list of positions of the remaining capsules in the maze.
 - ```s.isWin()``` : Returns True if the state is in a *winning end*.
 - ```s.isLose()``` : Returns True if the state is in a *losing end*.

### Illegal moves

You need to ensure that your agent always returns a legal move. If it is not the case, the game engine ignores it and repeat the previous move as long as it remains legal. Otherwise, it just keep getting stuck in the same location.

---

## Evaluation

The evaluation of your deliverables is based on the following criteria:

- Clarity of your report
	* Avoid long and vague sentences and be straight to the point.
	* Illustrate with examples.
	* Follow the structure mentioned in the instructions.

- Clarity and structure of the source code
	* Avoid single-file long code source, and prefers to use a multiple-files modular architecture.
	* Name your variables-attributes-classes according to their usage.
    * Comment your code so that explanations are concise and clear enough to allow the reader to understand the semantics in a quick look.
	* Your source code must be [PEP8](https://www.python.org/dev/peps/pep-0008/) compatible.
        - You can check this using `pycodestyle`.

These criteria are all important.

:warning: Plagiarism is checked and sanctioned by a grade of 0.

---

## Credits

Credits: [UC Berkeley](http://ai.berkeley.edu/project_overview.html)
