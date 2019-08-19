# Pacman

<p align="center">
<img src="pacman_game.png" width="50%" />
</p>

The goal of this programming project is to implement intelligent agents for the game of Pacman. The project is divided into three parts:
- **Part 1.** You must implement a Search agent for eating all the food dots as quickly as possible.
- **Part 2.** You must implement a Minimax agent for eating all the food dots as quickly as possible, while avoiding the ghost enemies that are chasing you.
- **Part 3.** You must implement a Bayes filter algorithm for tracking all the non-visible ghosts' positions.


## Table of contents

- [Installation](#installation)
    * [Setup](#setup)
    * [Usage](#usage)
- [Instructions](#instructions)
    * [Part 1: Search agent](#part-1-search-agent)
    * [Part 2: Minimax agent](#part-2-minimax-agent)
    * [Part 3: Reasoning over time](#part-3-reasoning-over-time)
- [FAQ](#helpers)
    * [Game score](#score)
    * [API](#api)
    * [Illegal moves](#illegal-moves)
- [Evaluation criteria](evaluation-criteria)	
- [Evaluation](#evaluation)
- [Typical mistakes and bad practice](#typical-mistakes-and-bad-practice)
- [Credits](#credits)

---

## Installation

The instructions below have been tested under Windows, Linux and MacOS.

We recommend to install a Python (3) environment using the Anaconda distribution. Further instructions can be found on the [Anaconda user guide](https://conda.io/docs/user-guide/install/index.html). Once installed, open the Anaconda prompt (Windows) or a terminal (Linux/MacOS).

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
conda install numpy
```

### Usage

Start the game with a Pacman agent controlled by the keyboard (keys `j`, `l`, `i`, `k` or arrow keys):
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

`--layout`: Start the game with a user-specifed layout for the maze (see the `/pacman_module/layouts/` folder):
```bash
python run.py --layout medium
```

`--nghosts`: Specifies the maximum number of ghosts:
```bash
python run.py --nghosts 1
```

`--hiddenghosts`: Hides the position of the ghost in the layout (relevant only for Project Part 3):
```bash
python run.py --hiddenghosts
```

`--ghostagent`: Start the game with a user-specifed ghost pattern among (`dumby`,`greedy`,`smarty`,`leftrandy`):
```bash
python run.py --ghostagent greedy
```

`--bsagentfile`: Start the game with a Belief State agent following a user-defined ghost positions' belief state update policy (relevant only for Project Part 3):
```bash
python run.py --bsagentfile beliefstateagent.py
```

`--p`: Specifies the 'p' parameter for ghost transition model (only relevant for Project Part 3, see instructions):
```bash
python run.py --p 0.5
```

`--w`: Specifies the 'w' parameter for sonar sensor model (only relevant for Project Part 3, see instructions):
```bash
python run.py --w 1
```

`-h`: For further details, check the command-line help section:
```bash
python run.py -h
```

---

## Instructions

For each part of the project, you must provide the following deliverables:

- The source code of your Pacman agent(s).
- A report in PDF format of 4 pages (at most and in total). A template will be provided for each part of the project in order to set the structure and page layout of the report. This template must be completed without any modification.

The three parts of the project must be carried out in groups of maximum 2 students (with the same group across all parts).

Your deliverables must be submitted as an archive on the [Montefiore submission platform](https://submit.montefiore.ulg.ac.be/teacher/courseDetails/INFO8006/).

**One delay of maximum 24 hours** will be **tolerated** for all parts of the project. For example, if you submit your first part late, no more delay will be allowed for the two other parts. In case of **more than one delay**, the concerned parts will receive a **0/20** grade. 

### Part 1: Search agent

This part is due by **October 13, 2019 at 23:59**. This is a **hard** deadline.

In this first part of the project, only food dots are in the maze. No ghost is present.
Your task is to design an intelligent based on search algorithms (see [Lecture 2](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture2.md)) for eating all the dots as quickly as possible.

To provide you some help, the implementations of Breadth-First Search (BFS) and Depth-First Search (DFS) are available in the corresponding Python files `bfs.py` and `dfs.py`. 

You are asked to implement an agent based on each of the following algorithms:
 - Uniform Cost Search (UCS)
 - A* (and an associated heuristic of your choice).
Each search algorithm should be implemented inside the `get_action` function of the corresponding Python files (`ucs.py`, `astar.py`), following the template of `pacmanagent.py`. Be careful, Uniform Cost Search (UCS) must be provided with its own cost function. 

Your report should be organized into 4 parts:
1. You must formalize the game as a search problem, as seen in [Lecture 2](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture2.md).
2. You should run your agents against the 3 maze layouts located the  `/pacman_module/layouts/` folder.
  For each layout, report as a bar plot the performance of your 2 agents in terms of:
	- a. final score 
	- b. total computation time 
	- c. total number of expanded nodes. 
In total, you should therefore produce 9 bar plots.
3. Answer the following questions:
	- a. (TO DECIDE)
	- b. (TO DECIDE)
4. You're expected to provide a short and constructive feedback about the project. In particular, you should discuss about the experience the project has brought to you and about the difficulties you may have encountered during the project. 
	

### Part 2: Minimax agent

This part is due by **November 23, 2018 at 23:59**. This is a **hard** deadline.

In this second part, Pacman can no longer wander peacefully in its maze. It is chased by a ghost that tries to kill him!

The ghost follows one of the following policies, as set through the `--ghostagent` command line option:
 - `dumby`: Rotate on itself in a counterclockwise fashion until it can go on its left.
 - `greedy`: Select the next position that is the closest to Pacman.
 - `smarty`: Select the next position which leads to the shortest path towards Pacman.

Your task is to design an intelligent agent based on adversarial search algorithms (see [Lecture 4](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture4.md)) for eating all the dots as quickly as possible while avoiding the ghost.

You are asked to implement an agent based on each of these adversarial search algorithms:
 - Minimax.
 - Minimax with alpha-beta pruning.
 - H-Minimax.

Each agent should be implemented as a `PacmanAgent` class. Each should be specified in a different Python file (`minimax.py`, `alphabeta.py` and `hminimax.py`), following the template of `pacmanagent.py`.

Your implementation of Minimax (with or without alpha-beta pruning) should be able to solve the smaller map `small_adv` against all kinds of ghosts. It is not required to be able to solve the larger maps (`medium_adv` and `large_adv`). On the other hand, your implementation of H-Minimax should solve all maps against all ghosts, within reasonable time and with a sufficient level of optimality.

Your report should be organized into 3 parts:
1. You must formalize the game as an adversarial search problem, as seen in [Lecture 4](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture4.md).
2. You should run your 3 Pacman agents on the `small_adv` maze layout against all 3 ghost agents.
  For each ghost agent, report as a bar plot the performance of your 3 Pacman agents in terms of i) final score, ii) total computation time and iii) total number of expanded nodes. In total, you should therefore produce 9 bar plots.
3. Discuss the performance and limitations of your agents, with respect to their search algorithm, the maze layout (`small_adv`, `medium_adv` and `large_adv`) and the ghost agent. Evaluate the impact of your custom evaluation and cutoff functions. Comment on possible improvements.

### Part 3: Reasoning over time

This part is due by **December 22, 2018 at 23:59**. This is a **hard** deadline.

In the last part of the project, ghosts are no longer visible to Pacman! However, Pacman is now equipped with a sonar that indicates the position of each ghost in the maze. Unfortunately Pacman's device is getting rusty and it only gives noisy estimates of the ghost positions.

You are asked to implement a Bayes filter to maintain a belief state about the ghost locations, as if there were no walls on the map.
- The sonar sensor model $P(e_t|x_t)$ follows  a uniform $W \times W$ discrete distribution centered around the unknown position $x_t$ of the ghost, where $W = 2w+1$.
- The transition model $P(x_{t+1}|x_t)$ of a ghost is defined as follows: If `East` is a legal action, then the ghost selects this action with a probability $0 \leq p \leq 1$. If it does not select it, then it follows uniformly at random one of the legal actions (including `East`).
    If `East` is not a legal action, the ghost takes uniformly at random one of the legal actions.
- The initial ghost position follows a uniform distribution over legal positions (i.e., where neither Pacman nor a wall is located).

You should complete the method `updateAndGetBeliefStates(evidences)` method of the `BeliefStateAgent` class of `beliefstateagent.py`. To test your implementation, specify `beliefstateagent.py` for the argument `--bsagentfile` and `rightrandy` for the argument `ghostagent`, along with your `w` and `p` parameters.

Your report should be organized as follows:
1. For the `observer.lay` map, illustrate and discuss the convergence of your belief state with respect to $w \in \{ 1, 3, 5\}$, $p$ and the number of time steps.
2. Discuss how you would improve your agent to take into account measurements that are not physically possible, such as a position that actually corresponds to a wall.

Note: the game engine will keep displaying the ghosts in order for you to compare your belief state to their positions. You can play the game in belief-state mode only by turning on the `--hiddenghosts` flag.


---

## FAQ

### Game score

The score function of the game is computed as follows:

`score = -#time steps + 10*#number of eaten food dots + 200*#number of eaten ghost + (-500 if #losing end) + (500 if #winning end)`.

We ask you to implement an agent that wins the game while maximizing its score.

Note that you should ask yourself if this score function satisfies all the properties of the search algorithms you will implement. If not, you are free to modify it as long as the optimal solutions remain the same.

### API

You must implement your agent as a `PacmanAgent` class, following the template of `pacmanagent.py`.
The core of your algorithm should be implemented or called within the `get_action` method. This method  receives the current state `s` of the game and should return the action to take.

Useful methods of the state are specified below:

 - ```s.generatePacmanSuccessors()``` : Returns a list of pairs of successor states and moves given the current state ```s``` for the pacman agent.
    * This method **must** be called for any node expansion for pacman agent.
 - ```s.generateGhostSuccessors(agentIndex)``` : Returns a list of pairs of successor states and moves given the current state ```s``` for the agent indexed by ```agentIndex>0```.
    * This method **must** be called for any node expansion for ghost agent.
 - ```s.getLegalActions(agentIndex)``` : Returns a list of legal moves given the state ```s``` and the agent indexed by ```agentIndex```. 0 is always the Pacman agent.
 - ```s.getPacmanPosition()``` : Returns the Pacman position in a ```(x,y)``` pair.
 - ```s.getScore()``` : Returns the total score of a state (as defined above).
 - ```s.getFood()``` : Returns a boolean matrix which gives the position of all food dots.
 - ```s.getWalls()``` : Returns a boolean matrix which gives the position of all walls.
 - ```s.getGhostPositions()``` : Returns the position of all ghosts in the maze.
 - ```s.getCapsules()``` : Returns a list of positions of the remaining capsules in the maze.
 - ```s.isWin()``` : Returns True if the state is in a *winning end*.
 - ```s.isLose()``` : Returns True if the state is in a *losing end*.

Implementation examples are provided in `humanagent.py` and `randomagent.py`.

### Illegal moves

You need to ensure that your agent always returns a legal move. If it is not the case, the previous move is repeated if it is still legal. Otherwise, it remains in the same location.

---

## Evaluation criteria

For each part of the project, you will be evaluated according to different criteria. Each criterion is associated to a certain amount of points according to its importance. 

### Part 1: Search agent

**Code** - 10 points
1. **Style** - 2 points
	* **PEP8 compatibility** - 0.8 point: PEP8 guidelines are provided at [Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/).  A script will be executed to check the compatibility of your code. 
		* 0.8 point : the script runs without error.
		* 0 point: otherwise.
	* **Specification** - 0.8 point: correctness of the specification of your functions.
		* 0.8 point : all specifications are correct.
		* 0.6 point : at least 75% correct specifications.
		* 0.4 point: at least 50% correct specifications.
		* 0.2 point: at least 25% correct specifications.
		* 0 point: less than 25% correct specifications.
	 * **Structure & Comments** - 0.4 point - Relevance of the subdivision of your code into functions. See [Typical mistakes and bad practice](#typical-mistakes-and-bad-practice) for more examples.

2. **Algorithms implementations** - 5 points: correctness of the implementation of the different search algorithms.
	* **UCS** - 2.5 points  
		* 2.5 points : correct implementation of UCS and its components (goal test, cost function, ...).
		* 0 point: incorrect implementation of UCS or any of its components.
	* **A*** - 2.5 points 
		* 2.5 points: correct implementation of A* and its components (UCS components + admissible heuristic).
		* 1.25 points: error due to UCS implementation but admissible heuristic.
		* 0 point: not admissible heuristic or implementation error of any component of A*.

3. **Algorithms performances** - 3 points: results accuracy and execution time. 
	* **UCS** - 1 point
	* **A*** - 1 point</br> 
	For each algorithm:
		* 1.5 point : execution time $<$ 2 sec.
		* 1.125 points: exection time between 2 and 5 sec.
		* 0.75 point: exection time between 5 and 10 sec.
		* 0.375 point: inaccurate results and/or execution time $\geq$ 10 sec.
		* 0 point: no result.

4. **Bonus** - 1 point: bonus point for a particularly good code structure.
	* **Factorisation** - 0.5 point: avoiding rewriting several times the same code instructions.
	* **Modularity** - 0.5 point: smart subdivision of the code into different files. 

**Report** - 10 points
1. **Problem statement** - 5 points
	* **State space** - 1 point
	* **Action space** - 1 point
	* **Transition model** - 1 point 
	* **Step cost** - 1 point
	* **Goal test** - 1 point</br>
	For each component of the statement:
		* 1 point : correct component.
		* 0 point: incorrect component.
		
2. **Graphs** - 1 point
	* **Presence** - 0.4 point
		* 0.4 point : graphs present.
		* 0 point: no graph.
	* **Readability** - 0.2 point: ease to understand the information given by the graphs and quality of their descriptions.
	* **Scale** - 0.4 point: consistency of the graphs between each other and ease to compare them visually. 
	
3. **Discussion** - 3 points
	* **Q1 (TO DECIDE)** - 1.2 points
	* **Q2 (TO DECIDE)**  - 1.2 points
	* **Project feedback** - 0.6 point: relevance of the feedback.
		* 3 points: constructive feedback.
		* 0 point: otherwise. 
		
4. **Style** - 1 point
	* **English** - 0.25 point: quality of the writing.
	* **Structure** - 0.5 point: respect of the provided template.
		* 0.5 point: template respected.
		* 0 point: template not respected. 
	* **Length** - 0.25 point
		* 0.25 point: at least 2 pages and at most 4 pages.
		* 0 point: length not respected 

N.B.: For any project, if the total grade (bonus included) is higher than 20, the exceeding points can be transferred to another project.

:warning: Plagiarism is checked and sanctioned by a grade of 0.

---

## Evaluation

The evaluation of your deliverables is based on the following criteria:

- Performance of your intelligent agent (as evaluated by its final score, its total computation time and its total number of expanded nodes). Note that your agents might be evaluated on mazes that are not included within the `/pacman_module/layouts/` folder.
- Quality and clarity of your report.
	* Avoid long and vague sentences and be straight to the point.
	* Follow the structure mentioned in the instructions.

- Quality, clarity and structure of the source code.
	* Avoid single-file long code source, and prefers to use a multiple-files modular architecture.
	* Name your variables-attributes-classes according to their usage.
    * Comment your code so that explanations are concise and clear enough to allow the reader to understand the semantics in a quick look.
	* Your source code must be Python 3 and [PEP8](https://www.python.org/dev/peps/pep-0008/) compatible.

:warning: Plagiarism is checked and sanctioned by a grade of 0.

---
## Typical mistakes and bad practice

**TODO**: Things to add:
1. Good/bad comments
2. Good/bad specifications
3. How do we handle crashes ? (compilation, execution, warnings, ...)


---

## Credits

Credits: [UC Berkeley](http://ai.berkeley.edu/project_overview.html)
