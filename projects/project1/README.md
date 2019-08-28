
# Project 1

## Table of contents

- [Instructions & Evaluation](#instructions&evaluation)
- [Credits](#credits)

---

## Instructions & Evaluation

This part is due by **October 13, 2019 at 23:59**. This is a **hard** deadline.

In this first part of the project, only food dots are in the maze. No ghost is present.
Your task is to design an intelligent based on search algorithms (see [Lecture 2](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture2.md)) for eating all the dots as quickly as possible.

To provide you some help, the implementations of Depth-First Search (DFS) are available in the corresponding Python file `dfs.py`. 

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
			 
		Any **reference to the API** in any component of the problem statement will be considered as **false**.
 2.  **Implementation**
	 -  2.a. - **3 points** - Implement A* algorithm with **your own cost function** *g(n)*  and **admissible heuristic** *h(n)*. The algorithm should be implemented inside the `get_action` function of the corresponding Python file `astar.py`, following the template of `pacmanagent.py`.
	 
		 - You must have *g(n)* different from *depth(n)* where *depth(n)* is the depth of node *n* in the search tree.
		 - You must have *h(n)* different from 0 for all *n*.
		 - You must prevent cycles. A cycle occurs when the same state occurs twice in a given path.
	
		These conditions are necessary for a correct implementation but not sufficient. There are other components required for A* (e.g. goal test, cost function, admissible heuristic, ...).
		
	  - 2.b. - **0.375 point** - Define and describe formally your cost function *g(n)* and your heuristic *h(n)*.
	  - 2.c. - **0.375 point** - **Show** that your *h(n)* is **admissible**.
	  - 2.d. - **2 points** - Implement Breadth-First Search (BFS) from your A* implementation using **appropriate cost function** *g(n)*  and **heuristic** *h(n)*. The algorithm should be implemented inside the `get_action` function of the corresponding Python file `bfs.py`, following the template of `pacmanagent.py`. <br/> If implementation errors are due to the implementation of A*, these will not be taken into account for this question.
	  - 2.e. - **0.375 point** - Justify briefly the choice of *g(n)* and *h(n)*.
 3. **Experiment 1** 
	 - 3.a. - **0.5 point** - Run A* with your own *g(n)* and *h(n)* and  A* with your own *g(n)* and *h(n) = 0* for all *n* against the medium maze layout located in the  `/pacman_module/layouts/` directory. Report the results as a bar plot in terms of:
	 
		 - Score
		 - Number of expanded nodes
		 
	- 3.b. - **0.375 point** - Describe the differences between the results of the two versions of A*.
	- 3.c. - **0.375 point** - Refer to the course in order to justify these differences.
	- 3.d. - **0.375 point** - Which algorithm corresponds to A* with *h(n) = 0* for all *n* ? 
 4. **Experiment 2** 
	 - 4.a. - **0.5 point** - Run A* with your own *g(n)* and *h(n)*, DFS and your implementation of BFS against the medium maze layout located in the  `/pacman_module/layouts/` directory. Report the results as a bar plot in terms of:
	 
		 - Score
		 - Number of expanded nodes
		 
	  - 4.b. - **0.375 point** - Describe the differences between the results of: 
	  
		  - A* and DFS
		  - A* and BFS
		 
	  - 4.c. - **0.375 point** - Refer to the course in order to justify these differences.

For each **discussion question** (2.b, 2.c, 2.e, 3.b, 3.c, 3.d, 4.b, 4.c), the evaluation will be performed as follows:
 - 100% points: complete answer.
 - 50% points: some relevant elements but incomplete answer.
 - no point: no relevant element or no answer.

Questions implying the inclusion of **plots** (3.a, 4.a) in the report will be evaluated considering the following criteria:

 - Presence
 - Readability: ease to understand the information given by the graphs and quality of their descriptions.
 - Scale: consistency of the graphs between each other and ease to compare them visually.

Your report has to follow the subdivision provided above. To do so, a template is provided. (ADD LINK TO TEMPLATE) 	

Besides the questions you're expected to answer, you will also be evaluated according to the following criteria:

 - **Code performances** - **3 points** - Your code will be tested on the submission platform machines. After each submission, you will receive a feedback which will contain information about the accuracy of your results and the time performances of your code.  
 
	 - 3 points: TBD
	 - 2.25 points: TBD
	 - 1.5 points: TBD
	 - 0.75 points: TBD
	 - 0 point: TBD
 
 - **Code style** - **2 points**
	 - **PEP8 compatibility** - 0.8 point - PEP8 guidelines are provided at [Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/).  A script will be executed to check the compatibility of your code. 
		 - 0.8 point : the script runs without error.
		 - 0 point: any error during the execution of the script.
	- **Specification** - 0.8 point - correctness of the specification of your functions.
		- 0.8 point : all specifications are correct.
		- 0.6 point : at least 75% correct specifications.
		- 0.4 point : at least 50% correct specifications.
		- 0.2 point : at least 25% correct specifications.
		- 0 point : less than 25% correct specifications.
	- **Structure & Comments** - 0.4 point - Relevance of the subdivision of your code into functions. See ADD LINK TO BAD PRACTICE for more examples.
 - **Report style** - **1 point**
	 * **English** - 0.25 point: quality of the writing.
	 * **Structure** - 0.5 point: respect of the provided template.
		* 0.5 point: template respected.
		* 0 point: template not respected. 
	* **Length** - 0.25 point
		* 0.25 point: at least 2 pages and at most 4 pages.
		* 0 point: length not respected
		
:warning: Plagiarism is checked and sanctioned by a grade of 0.

---
<!--

## Evaluation criteria

**Code** - 10 points
1. **Algorithms implementations** - 5 points: correctness of the implementation of A* algorithm.
	* **A\*** - 3 points 
		* 5 points: correct implementation of A* and its components ( goal test, cost function, admissible heuristic, etc...).
		* 0 point: implementation error of any component of A*.
	* **BFS** - 2 points 
		* 2 points: correct implementation of BFS and its components.
		* 1 point: implementation error due to a component of A*
		* 0 point: implementation error of any other component of BFS.

2. **Algorithms performances** - 3 points: results accuracy and execution time. 
	* 3 point : execution time < 2 sec.
	* 2.25 points: exection time between 2 and 5 sec.
	* 1.5 point: exection time between 5 and 10 sec.
	* 0.75 point: inaccurate results and/or execution time > 10 sec.
	* 0 point: no result. <br/> TODO: Set realistic benchmarks with submission platform machine. 

3. **Style** - 2 points
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

**Report** - 10 points

1. **Problem statement** - 5 points
	* **Set of states** - 1 point
		* The initial state must be specified
	* **Set of actions** - 1 point
	* **Transition model** - 1 point 
	* **Goal test** - 1 point
	* **Step cost** - 1 point<br/> For each component of the statement:
		* 1 point : correct component.
		* 0 point: incorrect component.
	
2. **Discussion** - 3 points
	* **Question 2** - 1.125 points
		* Q2.b. Definition of the cost function and of the heuristic - 0.375 point
		* Q2.c. Admissibility of the heuristic - 0.375 point
		* Q2.d. Justification of BFS components - 0.375 point
	* **Question 3** - 1.125 points
		* Q3.b. Description of the results - 0.375 point
		* Q3.c. Justification of the results - 0.375 point
		* Q3.d. Relation to existing algorithm - 0.375 point
	* **Question 4** - 0.75 point
		* Q4.b. Description of the results - 0.375 point
		* Q4.c. Justification of the results - 0.375 point

3. **Plots** - 1 point
	* **Presence** - 0.4 point
		* 0.4 point : graphs present.
		* 0 point: no graph.
	* **Readability** - 0.2 point: ease to understand the information given by the graphs and quality of their descriptions.
	* **Scale** - 0.4 point: consistency of the graphs between each other and ease to compare them visually. 
		
4. **Style** - 1 point
	* **English** - 0.25 point: quality of the writing.
	* **Structure** - 0.5 point: respect of the provided template.
		* 0.5 point: template respected.
		* 0 point: template not respected. 
	* **Length** - 0.25 point
		* 0.25 point: at least 2 pages and at most 4 pages.
		* 0 point: length not respected
-->

## Credits

Credits: [UC Berkeley](http://ai.berkeley.edu/project_overview.html)
