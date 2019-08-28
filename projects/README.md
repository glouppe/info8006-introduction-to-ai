# Projects - Pacman

<p align="center">
<img src="pacman_game.png" width="50%" />
</p>

The goal of this programming project is to implement intelligent agents for the game of Pacman. The project is divided into three parts:
- **Project 1.** You must implement a Search agent for eating all the food dots as quickly as possible.
 </br> &#8594; **Add link to project 1 here**
- **Project 2.** You must implement a Minimax agent for eating all the food dots as quickly as possible, while avoiding the ghost enemies that are chasing you.
 </br> &#8594; **Add link to project 2 here**
- **Project 3.** You must implement a Bayes filter algorithm for tracking all the non-visible ghosts' positions.
 </br> &#8594; **Add link to project 3 here**
 
--

## Table of contents

- [Installation](#installation)
    * [Setup](#setup)
    * [Usage](#usage)
- [Instructions](#instructions)
- [FAQ](#helpers)
    * [Game score](#score)
    * [API](#api)
    * [Illegal moves](#illegal-moves)	
- [Credits](#credits)
 
--

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

--

## Instructions

For each part of the project, you must provide the following deliverables:

- The source code of your Pacman agent(s).
- A report in PDF format of 4 pages (at most and in total). A template will be provided for each part of the project in order to set the structure and page layout of the report. This template must be completed without any modification.

The three parts of the project must be carried out in groups of maximum 2 students (with the same group across all parts).

Your deliverables must be submitted as an archive on the [Montefiore submission platform](https://submit.montefiore.ulg.ac.be/teacher/courseDetails/INFO8006/).

**One delay of maximum 24 hours** will be **tolerated** for all parts of the project. For example, if you submit your first part late, no more delay will be allowed for the two other parts. In case of **more than one delay**, the concerned parts will receive a **0/20** grade. 

--

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

## Credits

Credits: [UC Berkeley](http://ai.berkeley.edu/project_overview.html)

