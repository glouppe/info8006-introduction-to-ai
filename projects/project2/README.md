
# Project II

## Table of contents

- [Deliverables](#deliverables)
- [Instructions](#instructions)
- [Evaluation](#evaluation)
- [Credits](#credits)

---

## Deliverables

You are requested to deliver a *tar.gz* archive containing:
 - Your report named `report.pdf`.
	 - Your report must be at most **5** pages long.
	 - Fill in the following [template](https://github.com/glouppe/info8006-introduction-to-ai/blob/master/projects/project2/template-project2.tex) to write your report.
	 - In French or English.
 - Your `minimax.py` file containing your implementation of the Minimax algorithm.
	 - Put the class template defined in `pacmanagent.py` into `minimax.py` and fill in the `get_action` function.
 - Your `hminimax0.py` which contains your implementation of H-Minimax with your best cut-off/heuristic functions pair.
	 - Put the class template defined in `pacmanagent.py` into each file and fill in the `get_action` function.
 - Your `hminimax1.py` which contains your implementation of H-Minimax with your second best cut-off/heuristic functions pair.
	 - Put the class template defined in `pacmanagent.py` into each file and fill in the `get_action` function.
 - Your `hminimax2.py` which contains your implementation of H-Minimax with your third best cut-off/heuristic functions pair.
	 - Put the class template defined in `pacmanagent.py` into each file and fill in the `get_action` function.


:warning: A penalty of **-2 points** on the final grade will be applied if the files are not named based on the instructions above.

---

## Instructions

This part is due by **November 10, 2019 at 23:59**. This is a **hard** deadline.

In this second part of the project, Pacman can no longer wander peacefully in its maze! He needs to avoid a walking ghost and has no idea of (i) whether the ghost actually wants to kill him and (ii) how smart it is. Pacman only knows that it cannot make a half-turn unless it has no other choice.

The ghost follows one of the following policies, as set through the `--ghostagent` command line option:
 - `dumby`: Rotate on itself in a counterclockwise fashion until it can go on its left.
 - `greedy`: Select the next position that is the closest to Pacman.
 - `smarty`: Select the next position which leads to the shortest path towards Pacman.

Your task is to design an intelligent agent based on adversarial search algorithms (see [Lecture 4](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture4.md)) for eating all the dots as quickly as possible while avoiding the ghost.

You are asked to answer the following questions.

 1. **Problem Statement**

	 - 1.a. - **4 points** - Formalize the game as an **adversarial search problem**. Any **reference to the API** in any component of the problem statement will be considered as **false**.

	 - 1.b. - **1 point** - How would you describe the game of Pacman as a **zero-sum game**? Explain your answer using the game score function.

 2. **Implementation**

 	 - 2.a. - **1 point** - Consider the direct application of Minimax with respect to the problem statement.
	 	 - Discuss its completeness with respect to the game of Pacman.
		 - How to guarantee the completeness of Minimax by adapting the components described in the problem statement, while keeping the same set of optimal strategies?

		 **Hint**: observe the behaviour of the score function at the limits.

	 - 2.b. - **2 points** - Implement the **Minimax** algorithm. This should be done in the `get_action` function of `minimax.py`, following the template of `pacmanagent.py`.
		 - You must **guarantee the completeness** of the algorithm.
		 - Your Minimax agent needs to **provide an optimal strategy in the smaller map** `/pacman_module/layouts/small_adv.lay` against all kinds of ghosts.

	 - 2.c. - **2 points** - Implement the **H-Minimax** algorithm with your own **cutoff-tests** and **evaluation functions**. You are expected to provide 3 cutoff-test/evaluation function pairs, with at least two different evaluation functions. At most two of them might fail against some ghosts/layouts as long as they they are still in correlation with actual chances of winning. We expect you to design winning heuristics while being able to provide possible explanations on failing heuristics.
		 - Each proposed evaluation function needs to differ from the game score function.
		 - Your evaluation functions need to be **fast** to compute and **generalizable**.
		 - Evaluation functions can be built by weighting the different characteristics of the game state, but this is not a constraint.

		 N.B.: Although 3 layouts are provided for this project, you remain free to build your own layouts in order to fit the most general cutoff-test/evaluation function pair as possible. If you do so, discuss it briefly in your report.

	 - 2.d. - **1 point** - Define and describe formally your different cutoff-tests and evaluation functions.

 3. **Experiment**

	- 3.a. - **2 points** - Run your H-Minimax agent against `/pacman_module/layouts/large_adv.lay` layout and all ghosts, using your 3 cutoff-test/evaluation function pairs. Report your results as bar plots in terms of (i) score, (ii) time performances and (iii) number of expanded nodes. 	 
		- As the number of pages of the report is limited, we advise you to minimise the number of plots by combining bars whenever possible
	- 3.b. - **2 points** - **Summarize** the results of your cutoff-test/evaluation function pairs, according to the type of ghosts. **Explain** these results referring to the course.

	- 3.c. - **1 point** - How would you change your implementation in order to handle several ghosts ? Can the game still be described as a **zero-sum** game ? Justify your answer.

---

## Evaluation

In this section, you can find the criteria according to which the different questions will be evaluated, as well as some additional elements of evaluation of your code and report.

For each **implementation question** (2.b, 2.c), provide simply references to your code and to your cutoff-tests and evaluation functions in your report. The evaluation of your code will be performed as follows:
 - 100% points: correct implementation of the algorithm and its components.
 - 75% points: correct implementation w.r.t. the pseudo-code but errors related to the search problem.
 - no point: implementation error of any component of the algorithm.

For each **discussion question** (1.a, 1.b, 2.a, 2.d, 3.b, 3.c, 3.d), the evaluation will be performed as follows:

 - 100% points: complete answer.
 - 50% points: some relevant elements but incomplete and/or incorrect answer.
 - no point: no relevant element or no answer.

Questions implying the inclusion of **plots** (3.a) in the report will be evaluated considering the following criteria:

 - Presence: your resulting grade will be half the ratio between the provided and expected number of relevant bars.
 - Readability: Each bar that is not clearly readable/identifiable will be considered as not provided.
 - Scale: All the bars on each plot that is not correctly scaled will be considered as not provided.

Besides the questions you're expected to answer, you will also be evaluated according to the following criteria:

 - **Code performance** - **2 points** - Your code will be tested on the submission platform machines. After each submission, you will receive a feedback which will contain information about the accuracy of your results and the time performances of your code.  

	 - 2 points: <= 30 seconds
	 - 0 point: > 30 seconds

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

Note that your implementation might be tested on other layouts.

:warning: Plagiarism is checked and sanctioned by a grade of 0. Cases of plagiarism will all be reported to the Faculty.

---

## Credits

The programming projects are adapted from [CS188 (UC Berkeley)](http://ai.berkeley.edu/project_overview.html).
