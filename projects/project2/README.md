
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
	 - In French or English.
 - Your `minimax.py` file containing your implementation of the Minimax algorithm.
	 - Put the class template defined in `pacmanagent.py` into `minimax.py` and fill in the `get_action` function.
 - Your `hminimax0.py`, `hminimax1.py` and `hminimax2.py` files containing your different implementations of the H-Minimax algorithm (more explanation in [Instructions](#instructions) section).
	 - Put the class template defined in `pacmanagent.py` into each file and fill in the `get_action` function.

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

You are asked to answer the following questions. For this project, we have deliberately provided fewer explicit instructions in the statement about how you should structure your answers to the different questions. From what was asked in project 1 statement, you should now be able to figure this out by yourself.  

 1. **Problem Statement**
 
	 - 1.a. - **4 points** - Formalize the game as an **adversarial search problem**. Any **reference to the API** in any component of the problem statement will be considered as **false**.
		
	 - 1.b. - **1 point** - How would you describe the game of Pacman as a **zero-sum game** ? Explain your answer using the game score function. 

 2. **Implementation**
 
 	 - 2.a. - **1 points** - Consider the original implementation of Minimax.
	 	 - Discuss its completeness with respect to the game of Pacman.
		 - How to guarantee the completeness of Minimax by modifying some its components, while keeping the same set of optimal strategies. 
		 
		 **Hint**: observe the behaviour of the score function at the limits. 
		 
	 - 2.b. - **2 points** - Implement the **Minimax** algorithm. This should be done in the `get_action` function of `minimax.py`, following the template of `pacmanagent.py`.
		 - You must **guarantee the completeness** of the algorithm. 
		 - Your Minimax agent should **solve the smaller map** `/pacman_module/layouts/small_adv.lay` against all kinds of ghosts.	

	 - 2.c. - **2 points** - Implement the **H-Minimax** algorithm with your own **cutoff-tests** and **evaluation functions**. You're expected to provide 3 cutoff-test/evaluation function pairs, among which there should be at least 2 different cutoff-tests and 2 different evaluation functions. For this question, you're expected to provide both winning and failing pairs. Indeed, we want you to be able to design good heuristics on the one hand, but also to understand why some bad heuristic would fail on the other hand.  
		 - Each proposed evaluation function must differ from the game score function.
		 - The **computation** of your evaluation functions must be **short** and should **generalize** to different layouts.
		 - Generally, evaluation functions can be built by weighting the different characteristics of the game state. However, feel free to experiment other ways of building your evaluation functions.
		 - Your H-Minimax agent should **solve all maps** against each type of ghost with **at least one** of your cutoff-test/evaluation function **pair**, within reasonable time and with a sufficient level of optimality.
		 - For sake of correction simplicity, you should have one Python file per provided pair. `hminimax0.py` should contain your best pair, while `hminimax1.py` and `hminimax2.py`should contain your other choices. 
		 
		 N.B.: Although 3 layouts are provided for this project, you remain free to build your own layouts in order to fit the most general cutoff-test/evaluation function pair as possible. If you do so, discuss it in your report.
		 
	 - 2.d. - **1 point** - Define and describe formally your different cutoff-tests and evaluation functions.

 3. **Experiment**
 
	 - 3.a - **1 point** - Run your H-Minimax agent against `/pacman_module/layouts/large_adv.lay` layout with ghost `smarty`, using your 3 cutoff-test/evaluation function pairs. Report your results as bar plots in terms of (i) score, (ii) time performances and (iii) number of expanded nodes.
	
	- 3.b. - **1 point** - **Compare** these results and **explain** their differences referring to the course.
	
	- 3.c - **2 points** - **Summarize** (no plot is expected) the results of your cutoff-test/evaluation function pairs, according to the type of ghosts and to the layout. **Explain** these results. 
	
	- 3.d. - **1 point** - Run your best version of H-minimax against `/pacman_module/layouts/several_ghosts_adv.lay` layout with ghost `smarty` in order to analyse the behaviour of your agent in presence of several ghosts. What differences do you observe compared to the single ghost layouts ? How would you improve your implementation in order to handle several ghosts ?  

---

## Evaluation

In this section, you can find the criteria according to which the different questions will be evaluated, as well as some additional form evaluations of your code and report.

For each **implementation question** (2.b, 2.c), the evaluation will be performed as follows:
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

 - **Code performances** - **2 points** - Your code will be tested on the submission platform machines. After each submission, you will receive a feedback which will contain information about the accuracy of your results and the time performances of your code.  
 
	 - 2 points: <= 1 minute
	 - 0 point: > 1 minute
 
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


