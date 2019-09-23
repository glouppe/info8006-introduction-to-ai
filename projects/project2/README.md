
# Project II

## Table of contents

- [Instructions and Evaluation](#instructions-and-evaluation)
- [Deliverables](#deliverables)
- [Credits](#credits)

---

## Instructions and Evaluation

This part is due by **November 10, 2019 at 23:59**. This is a **hard** deadline.

In this second part, Pacman can no longer wander peacefully in its maze. It is chased by a ghost that tries to kill him!

The ghost follows one of the following policies, as set through the `--ghostagent` command line option:
 - `dumby`: Rotate on itself in a counterclockwise fashion until it can go on its left.
 - `greedy`: Select the next position that is the closest to Pacman.
 - `smarty`: Select the next position which leads to the shortest path towards Pacman.

Your task is to design an intelligent agent based on adversarial search algorithms (see [Lecture 4](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture4.md)) for eating all the dots as quickly as possible while avoiding the ghost.

You are asked to answer the following questions:

 1. **Problem Statement**

	 - 1.a. - **4 points** - Formalize the game as an **adversarial search problem**, i.e. in terms of:

		 - **0.66 point** - Initial state
		 - **0.66 point** - Function player 
		 - **0.66 point** - Set of legal actions
		 - **0.66 point** - Transition model 
		 - **0.66 point** - Terminal test
		 - **0.66 point** - Utility function
			 - Must take cycles into account.
			 - Should be derived from game score function: <br/>	`score = -#time steps + 10*#number of eaten food dots + 200*#number of eaten ghost + (-500 if #losing end) + (500 if #winning end)`
	
		Any **reference to the API** in any component of the problem statement will be considered as **false**.
		
	 - 1.b. - **1 point** - Does the environment correspond to a **zero-sum game** ? Justify your answer using the game score function. 

 2. **Implementation**
	 - 2.a. - **2 points** - Implement **Minimax** algorithm. This should be done inside the `get_action` function of the corresponding Python file `minimax.py`, following the template of `pacmanagent.py`.

		 - You must prevent cycles. To do so, you should use a list of visisted states for each expanded node.
		 - Your Minimax agent should solve the smaller map `small_adv` against all kinds of ghosts.
	
	 - 2.b. - **1 point** - Define and describe formally your cutoff-test and your evaluation function.
	 - 2.c. (BONUS ?) - **2 points** - Propose and implement **at least one improvement** for minimax. Justify the contribution of your modification(s) in terms of performances. 

	 - 2.d. - **3 points** - Implement **H-Minimax** algorithm with your own **cutoff-test** and **evaluation function**. You're expected to propose 3 cutoff-test/evaluation function pairs. 
		 - Each proposed evaluation function must differ from game score function.
		 - Your H-Minimax agent should solve all maps against all ghosts, within reasonable time and with a sufficient level of optimality.

 3. **Experiment**
	 - 3.a - **1 point** - Run the following versions  of H-Minimax against the `large_adv` layout with all types of ghosts:
		 - Your own implementation with each proposed  cutoff-test/evaluation function pair.
		 - H-Minimax version 1 TBD
		 - H-Minimax version 2 TBD
		 - H-Minimax version 3 TBD
		 
		Report your results as bar plots in terms of (i) score, (ii) time performances and (iii) number of expanded nodes.
	- 3.b. - **2 points** - **Compare** these results and **justify** their differences referring to the course.

For each **discussion question** (1.b, 2.b, 2.c, 3.b), the evaluation will be performed as follows:
 - 100% points: complete answer.
 - 50% points: some relevant elements but incomplete answer.
 - no point: no relevant element or no answer.

Questions implying the inclusion of **plots** (3.a) in the report will be evaluated considering the following criteria:

 - Presence
 - Readability: ease to understand the information given by the graphs and quality of their descriptions.
 - Scale: consistency of the graphs between each other and ease to compare them visually.

Your report has to follow the subdivision provided above. To do so, a template is provided. (ADD LINK TO TEMPLATE) 	

Besides the questions you're expected to answer, you will also be evaluated according to the following criteria:

 - **Code performances** - **3 points** - Your code will be tested on the submission platform machines. After each submission, you will receive a feedback which will contain information about the accuracy of your results and the time performances of your code.  
 TODO: ADD CONFIGURATION OF SUBMISSION MACHINES
 
	 - 3 points: TBD
	 - 2.25 points: TBD
	 - 1.5 points: TBD
	 - 0.75 points: TBD
	 - 0 point: TBD
 
 - **Code style** - **2 points**
	 - **PEP8 compatibility** - **0.8 point** - PEP8 guidelines are provided at [Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/).  A script will be executed to check the compatibility of your code. 
		 - 0.8 point : the script runs without error.
		 - 0 point: any error during the execution of the script.
	 - **Specification** - **0.8 point** - correctness of the specification of your functions.
		- 0.8 point : all specifications are correct.
		- 0.6 point : at least 75% correct specifications.
		- 0.4 point : at least 50% correct specifications.
		- 0.2 point : at least 25% correct specifications.
		- 0 point : less than 25% correct specifications.
	 - **Structure & Comments** - **0.4 point** - Relevance of the subdivision of your code into functions. See [Typical mistakes and bad practices](https://glouppe.github.io/info8006-introduction-to-ai/projects#typical-mistakes-and-bad-practices) for more examples.
 - **Report style** - **1 point**
	 - **English** - 0.25 point: quality of the writing.
	 - **Structure** - 0.5 point: respect of the provided template.
		* 0.5 point: template respected.
		* 0 point: template not respected. 
	 - **Length** - 0.25 point
		* 0.25 point: at least 2 pages and at most 4 pages.
		* 0 point: length not respected

	
Note that your implementation might be tested on other layouts. 
		
:warning: Plagiarism is checked and sanctioned by a grade of 0.

## Deliverables

You're expected to produce the following deliverables: a *tar.gz* archive containing:
 - Your report named `report.pdf`.
 - Your `minimax.py` file containing your implementation of minimax algorithm.
 - Your `hminimax.py` file containing your implementation of h-minimax algorithm and each proposed cutoff-test and evaluation function.


---

## Credits

Credits: [UC Berkeley](http://ai.berkeley.edu/project_overview.html)


