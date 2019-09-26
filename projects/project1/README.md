# Project I

## Table of contents

- [Deliverables](#deliverables)
- [Instructions](#instructions)
- [Evaluation](#evaluation)
- [Credits](#credits)

---

## Deliverables

You are requested to deliver a *tar.gz* archive containing:
 - Your report named `report.pdf`.
	 - Your report must be at most 5 pages long.
	 - Fill the following [template](https://github.com/glouppe/info8006-introduction-to-ai/blob/master/projects/project1/template-project1.tex) to write your report.
 - Your `astar.py` file containing your implementation of A\* algorithm.
	 - Put the class template defined in `pacmanagent.py` into `astar.py` and fill in the `get_action` function.
 - Your `bfs.py` file containing your implementation of BFS algorithm.
	 - Put the class template defined in `pacmanagent.py` into `bfs.py` and fill in the `get_action` function.
	 - Your implementation of BFS should only differ from A\* by its cost function and heuristic.

:warning: A penalty of **-2 points** on the final grade will be applied if the files are not named based on the instructions above.

---

## Instructions

This part is due by **October 13, 2019 at 23:59**. This is a **hard** deadline.

In this first part of the project, only food dots and Pacman are in the maze.
Your task is to design an intelligent agent based on search algorithms (see [Lecture 2](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture2.md)) for eating all the dots as quickly as possible.

To help you, the implementation of Depth-First Search (DFS) is available in the corresponding Python file `dfs.py`. We warn you that one of the TAs have coded this just after having a hard night trying to submit a journal paper a minute before the deadline. We have fixed most of the bugs but we might have left one of them. Once you have fixed the implementation and activated your Pacman environment (see our [Python tutorial](https://github.com/glouppe/info8006-introduction-to-ai/tree/master/python-tutorial#creating-a-conda-environment)), you can test DFS algorithm using the following commands:
```bash
python run.py --agentfile dfs.py --layout medium
```
When you want to test one of your implementation, just replace the script parameter `dfs.py` by the name of the file of the agent you want to test. Refer to the [usage section](https://github.com/glouppe/info8006-introduction-to-ai/blob/master/projects/README.md#usage) for more details about the game parameters.

Reminder: it is mandatory to use only the [API](https://github.com/glouppe/info8006-introduction-to-ai/tree/master/projects#api) to retrieve game information.

You are asked to answer the following questions:
 1. **Problem statement**
	 - 1.a. - **5 points** - Formalize the game as a **search problem**, i.e. in terms of:

		 - **1 point** - Set of possible states
			 - You should specify the initial state.
		 - **1 point** - Set of legal actions
		 - **1 point** - Transition model
		 - **1 point** - Goal test
		 - **1 point** - Step cost
			 - Must be > 0
			 - Must be derived from the game score function:  <br/>	`score = -#time steps + 10*#number of eaten food dots + 200*#number of eaten ghost + (-500 if #losing end) + (500 if #winning end)`

		Any **reference to the API** in any component of the problem statement will be considered as **wrong**.
 2.  **Implementation**
	  - 2.a. - **0.5 point** - Identify the implementation error in `dfs.py`. Explain its impact and how to fix it. Do not submit the fixed version of DFS.
	  - 2.b. - **3.5 points** - Implement the A\* algorithm with **your own cost function** *g(n)*  and an **admissible heuristic** *h(n)*. The algorithm should be implemented inside the `get_action` function of the corresponding Python file `astar.py`, following the template of `pacmanagent.py`.

		 - You must have *g(n)* different from *depth(n)* where *depth(n)* is the depth of node *n* in the search tree.
		 - You must have *h(n)* different from 0 for all *n*.
		 - You must prevent cycles. A cycle occurs when the same state occurs twice in a given path.
		 - You may want to have a look at the file `/pacman_module/util.py` in order find a suitable data structure for the exploration of the game tree.

	  - 2.c. - **1.0 point** - Define and describe formally your cost function *g(n)* and your heuristic *h(n)*. Explain whether your heuristic *h(n)* guarantees the optimality of your A\* implementation.
	  - 2.d - **0.5 point** - Explain how your choice of *g(n)* preserves the completeness and optimality - with respect to the original score function - of A\* when *h(n)* = 0 for all *n*.
	  - 2.e. - **1.5 points** - Implement Breadth-First Search (BFS) by adapting your A\* implementation using **appropriate cost function** *g(n)*  and **heuristic** *h(n)*. The algorithm should be implemented inside the `get_action` function of the corresponding Python file `bfs.py`, following the template of `pacmanagent.py`. <br/> If your implementation of BFS only differs from A* by *g(n)* and *h(n)* and if there are errors in the implementation of A\*, these will not be penalised for this question.
	  - 2.f. - **0.5 point** - Justify briefly the choice of *g(n)* and *h(n)* for your BFS implementation.
 3. **Experiment 1**
	 - 3.a. - **0.5 point** - Run A\* with your own *g(n)* and *h(n)* and  A\* with your own *g(n)* and *h(n) = 0* for all *n* against the medium maze layout `/pacman_module/layouts/medium.lay`. Report the results as a bar plots in terms of:

		 - Score
		 - Number of expanded nodes

	- 3.b. - **0.5 point** - Describe the differences between the results, in terms of score and number of expanded nodes, of the two versions of A\*.
	- 3.c. - **0.5 point** - Refer to the course in order to justify these differences.
	- 3.d. - **0.5 point** - Which algorithm corresponds to A\* with *h(n) = 0* for all *n* ?
 4. **Experiment 2**
	 - 4.a. - **0.5 point** - Run A\* with your own *g(n)* and *h(n)*, DFS and your implementation of BFS against the medium maze layout `/pacman_module/layouts/medium.lay`. Report the results as a bar plots in terms of:

		 - Score
		 - Number of expanded nodes

	  - 4.b. - **0.5 point** - Describe the differences between the results, in terms of score and number of expanded nodes, of:

		  - A\* and DFS
		  - A\* and BFS

	  - 4.c. - **0.5 point** - Refer to the course in order to justify these differences.

---

## Evaluation

In this section, you can find the criteria according to which the different questions will be evaluated, as well as some additional form evaluations of your code and report.

For each **implementation question** (2.b, 2.e), the evaluation will be performed as follows:
 - 100% points: correct implementation of the algorithm and its components.
 - 75% points: correct implementation w.r.t. the pseudo-code but errors related to the search problem (A\* and BFS) and to the heuristic (A\*).
 - no point: implementation error of any component of the algorithm.

For each **discussion question** (2.a, 2.c, 2.d, 2.f, 3.b, 3.c, 3.d, 4.b, 4.c), the evaluation will be performed as follows:
 - 100% points: complete answer.
 - 50% points: some relevant elements but incomplete and/or incorrect answer.
 - no point: no relevant element or no answer.

Note that any unjustified answer will be considered as incomplete.

Questions implying the inclusion of **plots** (3.a, 4.a) in the report will be evaluated considering the following criteria:

 - Presence: your resulting grade will be half the ratio between the provided and expected number of relevant bars.
 - Readability: Each bar that is not clearly readable/identifiable will be considered as not provided.
 - Scale: All the bars on each plot that is not correctly scaled will be considered as not provided.

Besides the questions you're expected to answer, you will also be evaluated according to the following criteria:

 - **Code performances** - **2 points** - Your code will be tested on the submission platform machines. You will be evaluated with respect to its time performances:

	 - 2 points: fast enough (<3 seconds).
	 - 1 point: satisfying (3-10 seconds).
	 - 0 point: too slow (>10 seconds).

 - **Code style** - **2 points**
	 - **PEP8 compatibility** - **0.8 point** - PEP8 guidelines are provided at [Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/).  A script will be executed to check the compatibility of your code.
		 - 0.8 point : the script runs without error.
		 - 0 point: any error during the execution of the script.
	 - **Specification** - **1.2 point** - correctness of the specification of your functions.
		- 1.2 point : all specifications are correct.
		- 0.9 point : at least 75% correct specifications.
		- 0.6 point : at least 50% correct specifications.
		- 0.3 point : at least 25% correct specifications.
		- 0 point : less than 25% correct specifications.


Take care of providing a clearly structured and commented source code. We reserve the right to refuse to evaluate a source code (i.e. to consider it entirely wrong), which would be difficult to read and understand despite its possible correctness.

In the same way, take care of providing a clearly written report, which fully follows the provided template. We reserve the right to refuse to evaluate a report (i.e. to consider it as not provided) which would be difficult to read and understand. We may also refuse to evaluate discussion blocks that are truly confusing, even if the underlying idea might be right.

We have written a [Typical mistakes and bad practices](https://github.com/glouppe/info8006-introduction-to-ai/blob/master/projects/README.md#typical-mistakes-and-bad-practices) section to help you to provide a working source code of good quality.

Sanctions will be imposed in case of non-respect of the guidelines about the structure and length of the report:

 - Any modification of the template: **-2 points**
 - Only the first 5 pages of the report will be taken into account for the evaluation.


Note that your implementation might be tested on other layouts.

:warning: Plagiarism is checked and sanctioned by a grade of 0. Cases of plagiarism will all be reported to the Faculty.

---

## Credits

The programming projects are adapted from [CS188 (UC Berkeley)](http://ai.berkeley.edu/project_overview.html).
