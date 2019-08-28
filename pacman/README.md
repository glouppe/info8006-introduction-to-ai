

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
- [Typical mistakes and bad practices](#typical-mistakes-and-bad-practices)
- [Evaluation criteria](#evaluation-criteria)	
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

You are asked to answer the following questions:
 1. **Problem statement**
	 - 1.a. **Describe the game** you are asked to solve, within a few lines.
	 - 1.b. Formalize the game as a **search problem**, i.e. in terms of:
		 - Set of possible states <br/> :warning: Unnesseary to specify the initial state as it depends on the layout.
		 - Set of legal actions
		 - Transition model
		 - Goal test
		 - Step cost (must be > 0)
 2.  **A\* implementation**
	 - 2.a. Implement A* algorithm with **your own cost function** *g(n)*  and **admissible heuristic** *h(n)*. The algorithm should be implemented inside the `get_action` function of the corresponding Python file `astar.py`, following the template of `pacmanagent.py`.
		 - You must have *g(n)* different from *depth(n)*
		 - You must have *h(n)* different from 0 everywhere.
		 - You must prevent cycles. A cycle is a path where a given state occurs at least twice.
	  - 2.b. Define and describe formally your cost function *g(n)* and your heuristic *h(n)*.
	  - 2.c. **Show** that your *h(n)* is **admissible**.
 3. **Experiment 1** 
	 - 3.a. Run A* with your own *g(n)* and *h(n)* and  A* with your own *g(n)* and *h(n) = 0* everywhere against the 3 maze layouts located the  `/pacman_module/layouts/` folder. For each layout, report the results as a bar plot in terms of:
		 - Score
		 - Number of expanded nodes
	- 3.b. Describe the differences between the results of the two versions of A*.
	- 3.c. Refer to the course in order to justify these differences.
	- 3.d. Which algorithm corresponds A* with *h(n) = 0* everywhere to ? 
 4. **Experiment 2** 
	 - 4.a. Run A* with your own *g(n)* and *h(n)*, DFS and BFS against the 3 maze layouts located the  `/pacman_module/layouts/` folder. For each layout, report the results as a bar plot in terms of:
		 - Score
		 - Number of expanded nodes
	  - 4.b. Describe the differences between: 
		  - A* and DFS
		  - A* and BFS
	  - 4.c. Refer to the course in order to justify these differences.
 5. **Experiment 3**   
	   - 5.a. Run A* with *g(n) = depth(n)* and *h(n) = 0* everywhere against the 3 maze layouts located the  `/pacman_module/layouts/` folder. For each layout, report the results as a bar plot in terms of:
		   - Score
		   - Number of expanded nodes 
	  - 5.b. Describe these results compared to DSF and BFS and refer to the course in order to justify these observations.
	  - 5.c. Which algorithm corresponds A* with *g(n) = depth(n)* and *h(n) = 0* everywhere to ? 
 6. **Project feedback (BONUS)** <br/> You're invited to provide a short and constructive feedback about the project. In particular, you should discuss about the experience the project has brought to you and about the difficulties you may have encountered during the project. 

Your report has to follow the subdivision provided above. To do so, a template is provided. (ADD LINK TO TEMPLATE) 	

### Part 2: Minimax agent

This part is due by **November 10, 2018 at 23:59**. This is a **hard** deadline.

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

2. **Algorithms implementations** - 5 points: correctness of the implementation of A* algorithm.
	* **A*** - 5 points 
		* 5 points: correct implementation of A* and its components ( goal test, cost function, admissible heuristic, etc...).
		* 0 point: implementation error of any component of A*.

3. **Algorithms performances** - 3 points: results accuracy and execution time.
	* **A*** - 3 points
		* 3 point : execution time < 2 sec.
		* 2.25 points: exection time between 2 and 5 sec.
		* 1.5 point: exection time between 5 and 10 sec.
		* 0.75 point: inaccurate results and/or execution time > 10 sec.
		* 0 point: no result.

**Report** - 10 points

1. **Problem statement** - 5 points
	* **Set of states** - 1 point
	* **Set of actions** - 1 point
	* **Transition model** - 1 point 
	* **Goal test** - 1 point
	* **Step cost** - 1 point<br/> For each component of the statement:
		* 1 point : correct component.
		* 0 point: incorrect component.
		
2. **Graphs** - 1 point
	* **Presence** - 0.4 point
		* 0.4 point : graphs present.
		* 0 point: no graph.
	* **Readability** - 0.2 point: ease to understand the information given by the graphs and quality of their descriptions.
	* **Scale** - 0.4 point: consistency of the graphs between each other and ease to compare them visually. 
	
3. **Discussion** - 3 points
	* **Question 1** - 0.3 point
		* Q1.a. Description of the game - 0.3 point
	* **Question 2** - 0.6 point
		* Q2.b. Definition of the cost function and of the heuristic - 0.3 point
		* Q2.c. Admissibility of the heuristic - 0.3 point
	* **Question 3** - 0.9 point
		* Q3.b. Description of the results - 0.3 point
		* Q3.c. Justification of the results - 0.3 point
		* Q3.d. Relation to existing algorithm - 0.3 point
	* **Question 4** - 0.6 point
		* Q4.b. Description of the results - 0.3 point
		* Q4.c. Justification of the results - 0.3 point
	* **Question 5** - 0.6 point
		* Q4.b. Description and justification of the results - 0.3 point
		* Q4.c. Relation to existing algorithm - 0.3 point
		
4. **Style** - 1 point
	* **English** - 0.25 point: quality of the writing.
	* **Structure** - 0.5 point: respect of the provided template.
		* 0.5 point: template respected.
		* 0 point: template not respected. 
	* **Length** - 0.25 point
		* 0.25 point: at least 2 pages and at most 4 pages.
		* 0 point: length not respected
		
5. **Feedback (BONUS)** - 1 point
	* 1 point: constructive feedback.
	* 0 point: irrelevant feedback.   

N.B.: For any project, if the total grade (bonus included) is higher than 20, the exceeding points can be transferred to another project.

:warning: Plagiarism is checked and sanctioned by a grade of 0.

---


## Typical mistakes and bad practices

We show through this section a list of common mistakes and bad practices that we have observed through past projects. Although this section is non exhaustive and thus is subject to regular updates, we hope that the following list will help you to avoid many pitfalls that can hurt the quality of your project. 

### Report

- **Formalism**
	* Reference to an implemented function/method to describe any component of a problem statement. A formal description of a problem statement is **always** independent of its implementation.
	* Missing variables in state/action spaces. This error always jeopardizes the formal description of the problem, and often jeopardizes the whole project.
	* Variables not taken into account in the transition model. Transitions must include **all** the variables, even if some of them might stay idle.
	
- **Graphics**
	* Unreadable legend/axis, e.g., tiny font, flash coloured text, mixing text and plots. Not only this is annoying for the readers, but it also might slow you down in your working progress, if not interfere with the quality of your discussion on results.   
	* Variables with different scales on the same graphics. When in presence of large variables values, others variable with small scales can literally vanish out of the graphics. You should often instead separate them. [Logarithmic scale](https://en.wikipedia.org/wiki/Logarithmic_scale) might also be considered when including two variables with different scales in the same graphics is relevant to the discussion.
	
	
### Code

- **Style/Documentation**
	* Source code is not PEP8-compliant. Fulfilling the required specifications help to the readability of your source code. You can use dedicated [scripts](https://pypi.org/project/pep8/) to check PEP8-compliance of your source code.
	* Function specifications are either wrong or missing. They must be present and they must **formally** describe the function out of ambiguity. Its purpose is to provide an easier-to-understand description of the function than the code itself. An example of a correct specification is provided below : 
	
	```python
	   def nth_fibonacci(n):
           """
           Computes the n-th member of the Fibonacci sequence.
           Recursive definition: f(0)=0, f(1)=1,
                                 f(n)=f(n-1) + f(n-2) for n > 1

           Arguments:
           ----------
           - `n (integer): Positive index of the Fibonacci sequence.

           Return:
           -------
           - The n-th member of the Fibonacci sequence.
           """
           if n == 0:
               return 0
           if n == 1:
               return 1
           return nth_fibonacci(n-1) + nth_fibonacci(n-2)
	```
	* Variables and functions are not named accordingly to their meanings. A source code in which names are based on target meanings is easier to read and might need less comments to be readable.
	* Comments are either uninformative, too verbose or missing. They are important to structure the code and to provide high-level insights on how each part of code interacts with each other, and how the source code is actually behaving (useful for optimization among other benefits). They must contains few words and be straight to the point. 
	
- **Implementation**
	* Incorrect implementation of the algorithms. This is often due to the violation of any specification of the algorithms, or to an incorrect implementation of the problem statement, e.g., a wrong goal test is provided to the algorithm. Be sure to understand the problem statement you need to describe and the algorithms you are required to implement. 
	* Over confidence on implementation correctness by testing on a small subset of problem instances. While tests are useful to spot implementation errors, they cannot discard all of them. Even if your implementation "works" on some instances of the problem statement, and even if you are encouraged to do such tests, you need to carefully verify your implementation. This includes 1) the correctness of the inputs given to your algorithms with respect to the problem statement and 2) the fullfilment of the algorithms specifications in your implementation.
	* Inefficiency during execution. Only a few seconds is necessary in the worst case to solve each instance of the problem statement we provide in the projects. While you should first have a working version of your implementation, you should also be careful to limit the computation time below these few seconds.
	* Import and edge-cases errors, e.g. index out of bounds. While a typo in import sections does not jeopardize the implementation correctness - as long as the required files are present -, it is often difficult for the reader to decide if edge-cases error are either typos or part of the incorrect implementation. The safest policy being the latter, we refer to it when evaluating your work.  
       
---
## Credits

Credits: [UC Berkeley](http://ai.berkeley.edu/project_overview.html)
