
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
	 - Your report must be at most **TBD** pages long.
	 - Fill the following [template](https://github.com/glouppe/info8006-introduction-to-ai/blob/master/projects/project2/template-project2.tex) to write your report.
 - Your `minimax.py` file containing your implementation of Minimax algorithm.
	 - Put the class template defined in `pacmanagent.py` into `minimax.py` and fill in the `get_action` function.
 - Your `hminimax.py` file containing your implementation of H-Minimax algorithm.
	 - Put the class template defined in `pacmanagent.py` into `hminimax.py` and fill in the `get_action` function.

:warning: A penalty of **-2 points** on the final grade will be applied if the files are not named based on the instructions above.

---

## Instructions

This part is due by **November 10, 2019 at 23:59**. This is a **hard** deadline.

In this second part, Pacman can no longer wander peacefully in its maze. It is chased by a ghost that tries to kill him!

The ghost follows one of the following policies, as set through the `--ghostagent` command line option:
 - `dumby`: Rotate on itself in a counterclockwise fashion until it can go on its left.
 - `greedy`: Select the next position that is the closest to Pacman.
 - `smarty`: Select the next position which leads to the shortest path towards Pacman.

Your task is to design an intelligent agent based on adversarial search algorithms (see [Lecture 4](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture4.md)) for eating all the dots as quickly as possible while avoiding the ghost.

You are asked to answer the following questions. For this project, we have deliberately provided less clues in the statement about how you should structure your answers to the different questions. From what has been proposed in project 1 statement and your work on that project, you should now be able to figure this out by yourself.  

 1. **Problem Statement**

	 - 1.a. - **4 points** - Formalize the game as an **adversarial search problem**. Any **reference to the API** in any component of the problem statement will be considered as **false**.
		
	 - 1.b. - **1 point** - Does the environment correspond to a **zero-sum game** ? Justify your answer using the game score function. 

 2. **Implementation**
	 - 2.a. - **2 points** - Implement **Minimax** algorithm. This should be done inside the `get_action` function of the corresponding Python file `minimax.py`, following the template of `pacmanagent.py`.
		 - You must prevent cycles. 
		 - Your Minimax agent should solve the smaller map `small_adv` against all kinds of ghosts.
		 
	 - 2.b. (BONUS ?) - **2 points** - Propose and implement **at least one improvement** for minimax. Justify the contribution of your modification(s) in terms of performances. 

	 - 2.c. - **3 points** - Implement **H-Minimax** algorithm with your own **cutoff-test** and **evaluation function**. You're expected to propose 3 cutoff-test/evaluation function pairs. 
		 - Each proposed evaluation function must differ from the game score function.
		 - The **computation** of your evaluation functions must be **short** and should **generalize** to different layouts.
		 - Generally, evaluation functions can be built by ponderating the different information characterizing the game state. However, feel free to experiment other ways of building your evaluation functions.
		 - Your H-Minimax agent should **solve all maps** against all ghosts with **at least one** of your cutoff-test/evaluation function **pair**, within reasonable time and with a sufficient level of optimality.
		 
		 N.B.: Although 3 layouts are provided for this project, you remain free to build your own layouts in order to fit the most general cutoff-test/evaluation function pair as possible. If you do so, you must discuss about that in your report.
		 
	 - 2.d. - **1 point** - Define and describe formally your different cutoff-tests and evaluation functions.

 3. **Experiment**
 
	 - 3.a - **1 point** - Run your H-Minimax agent against the large adversarial layout `/pacman_module/layouts/large_adv.lay` with ghosts `smarty`, using your different cutoff-test/evaluation function pairs. Report your results as bar plots in terms of (i) score, (ii) time performances and (iii) number of expanded nodes.
	
	- 3.b. - **1 point** - **Compare** these results and **justify** their differences referring to the course.
	
	- 3.c - **2 points** - **Summarize** (no graph is expected) the performances of your cutoff-test/evaluation function pairs, according to the type of ghosts and to the layout. **Justify** these performances. 

---

## Evaluation

In this section, you can find the criteria according to which the different questions will be evaluated, as well as some additional form evaluations of your code and report.

For each **implementation question** (2.a, 2.c), the evaluation will be performed as follows:
 - 100% points: correct implementation of the algorithm and its components.
 - 75% points: correct implementation w.r.t. the pseudo-code but errors related to the search problem (A\* and BFS) and to the heuristic (A\*).
 - no point: implementation error of any component of the algorithm.

For each **discussion question** (1.a, 1.b, 2.d, 3.b, 3.c), the evaluation will be performed as follows:

 - 100% points: complete answer.
 - 50% points: some relevant elements but incomplete and/or incorrect answer.
 - no point: no relevant element or no answer.

Questions implying the inclusion of **plots** (3.a) in the report will be evaluated considering the following criteria:

 - Presence: your resulting grade will be half the ratio between the provided and expected number of relevant bars.
 - Readability: Each bar that is not clearly readable/identifiable will be considered as not provided.
 - Scale: All the bars on each plot that is not correctly scaled will be considered as not provided.

Besides the questions you're expected to answer, you will also be evaluated according to the following criteria:

 - **Code performances** - **3 points** - Your code will be tested on the submission platform machines. After each submission, you will receive a feedback which will contain information about the accuracy of your results and the time performances of your code.  
 
	 - 3 points: fast enough (**TBD**)
	 - 2 points: satisfying (**TBD**)
	 - 1 point: slow (**TBD**)
	 - 0 point: too slow(**TBD**)
 
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
		
:warning: Plagiarism is checked and sanctioned by a grade of 0.

---

## Credits

Credits: [UC Berkeley](http://ai.berkeley.edu/project_overview.html)


