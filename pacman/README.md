# Credits

Credits: [UC Berkeley](http://ai.berkeley.edu/project_overview.html)
         [OpenAI Interface](https://github.com/sohamghosh121/PacmanGym)

# Installation


All the instructions below have been tested under Linux and should work for MacOS.

 - See [Anaconda webpage](https://conda.io/docs/user-guide/install/index.html) for instructions to install Anaconda/Miniconda (recommended).

 - Create your own Anaconda environment and activate it.
```bash
conda create -n <env_name> python=3.6
source activate <env_name>
```

From now, it is assumed that <env_name> is activated. 

 - Install dependencies.
```bash
pip install -U gym numpy stopit argparse pynput pillow
```

 - Install and use pycodestyle to check PEP8 compliance of Python scripts.
```bash
pip install -U pycodestyle
pycodestyle <yourscript>.py
```

 - Install and use autopep8 to rewrite Python scripts into PEP8 format.
```bash
pip install -U autopep8
autopep8 --in-place --aggressive --aggressive <yourscript>.py
```

/!\ Check your file again with pycodestyle.

# Usage

## General

 - Display the command-line help section
```bash
python run.py -h
```

  - Interactive game
```bash
python run.py --agentfile humanagent.py
```
:warning: While it works directly on Linux, root privileges are needed for keyboard access in MacOS. Not tested for Windows.

## Search (1/3)

 - Launches a game with a random agent in default map mediumClassic:
```bash
python run.py
```

 - Launches a game with your Pacman agent class, named PacmanAgent located in `youragentmodule.py`, and with the maze originalClassic (see layout folder).
```bash
python run.py --layout originalClassic --agentfile youragentmodule.py
```
 - Launches a game with the human agent (that is, an interactive game).
```bash
python run.py --layout originalClassic --agentfile humanagent.py
```

- Same configuration as above, but enable the call to `registerInitialState` method.
```bash
python run.py --layout mediumClassic --agentfile youragentmodule.py --registerinitialstate
```


See the help section of the command line for more information about the parameters.

# Scoring

### Search (1/3)

The score function is computed as follows:

`score = -#time steps + 10*#number of food dots eaten + (500 when finished)`

# Instructions

## Introduction 

![Pacman maze example](https://github.com/glouppe/info8006-introduction-to-ai/blob/pacman_project/pacman/pacman_game.png "Pacman maze")

In this classical Pacman game, the player navigates Pacman through a maze filled of food dots. The goal is to collect them all in a minimum amount of time (Part 1/3). Ghosts, which are Pacman's enemies, may also be part of the game. In this configuration, Pacman needs to avoid them while collecting all the food dots (Part 2/3). To help him, Pacman may have access to capsules in the maze, giving him the ability to beat Ghosts, resetting them in their initial positions, in a short amount of time. The game ends if either Pacman have collected all the dots (winning end) or Pacman collides with one of the Ghosts (losing end). Cherry on the cake, some walls on the game may have a particular characteristic. Indeed, they can randomly be crossed or not over time (Part 3/3).

The project is splitted into three parts. Your task is to design a family of searching agents for each part of the project (details are provided in the three next sections below). 

## Searches (Part 1/3)

Before the implementation, you need to formalize the Pacman game as a search problem, as seen in [Lecture 2](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture2.md). Then, implement the following searching algorithms :

 - Depth-First Search (DFS)
 - Breadth-First Search (BFS)
 - Uniform Cost Search (UCS)
 - A* with *your own heuristic*

You need to justify the choice of the heuristic for A* regarding the layout of the map, including the distribution of the food dots, in terms of final score/total computation time.



### Deliverable 1/2 - Implementation

You need to send, at least, a Python 3 source code file, containing the [class template](https://github.com/glouppe/info8006-introduction-to-ai/tree/master/pacman/pacmanagent.py) completed on your own. Include also the other dependencies you have implemented inside a subfolder. Implementation [examples](https://github.com/glouppe/info8006-introduction-to-ai/tree/master/pacman/) are provided. Your source code needs to be formatted in order to follow the [PEP-8](https://www.python.org/dev/peps/pep-0008/) style conventions. Make sure to properly follow the instructions contained in the class template. 

### Deliverable 2/2 - Report

You need to provide a report in PDF format of 4 pages max (not including appendices for results). Your report must (i) contains the formalization of the Part 1 as a search problem, (ii) describes and justify carefully the (admissible) heuristics you have considered, (iii) show and discuss benchmark results, comparing the performance of your agent with the other algorithms you have implemented.

### Deadline

Due to Oct 28,2018. Submit your deliverables [there](https://submit.montefiore.ulg.ac.be/teacher/courseDetails/INFO8006/)

## Ghosts (Part 2/3)

Coming soon

## Blinkwalls (Part 3/3)

Coming soon

## Computation time budget (All parts)

The computation time of the agent is limited on-game. More specifically, the method ```get_action``` of the agent prematurely terminates when the computation time transgress the given `timeout` parameter (fixed to 60 seconds during evaluation process). On the other side, when the option ``` --enable-search-before-game ``` is specified, the method ``` registerInitialState ``` is called before the game starts, enabling computation without any computation time limit. Both configurations are considered during evaluation process.

## Illegal moves (All parts)

You need to ensure that your agent always returns a legal move. If it is not the case, the game engine ignores it and repeat the previous move as long as it remains legal. Otherwise, it just keep getting stuck in the same location.



## Evaluation

The evaluation of your deliverables is based on the following criteria :

- Clarity of your report
	* Avoid long and vague sentences and be straight to the point. Ideally, the length of each sentence should not exceed a line.
	* Do not hesitate to illustrate with examples.
	* Do not overload your graphics, and write short and clear captions. The reader should understand them in a quick look.
	* Lack of structure leads to lack of clarity. We recommend you to design your report outline on top of the one described in the previous section.
- Clarity and structure of the source code
	* Avoid single-file long code source, and prefers to use a multiple-file modular architecture. 
	* Name your variables-attributes-classes according to their usage. Comment your code so that explanations are concise and clear enough to allow the reader to understand the semantics in a quick look.

These criterions are all importants. We particularly value well written reports and code documentation. 

:warning: Plagiarism is checked and sanctioned by a 0 grade. It is fine to reuse external code, as long as (i) it does not cover your whole approach, (ii) you fully understand the principles behind and (iii) you do give credits in your code.
