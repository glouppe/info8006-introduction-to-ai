# Project 1

## Table of contents

- [Instructions](#instructions)
- [Evaluation criteria](#evaluation-criteria)	
- [Credits](#credits)

---

## Instructions

This part is due by **October 13, 2019 at 23:59**. This is a **hard** deadline.

In this first part of the project, only food dots are in the maze. No ghost is present.
Your task is to design an intelligent based on search algorithms (see [Lecture 2](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture2.md)) for eating all the dots as quickly as possible.

To provide you some help, the implementations of Breadth-First Search (BFS) and Depth-First Search (DFS) are available in the corresponding Python files `bfs.py` and `dfs.py`. 

You are asked to answer the following questions:
 1. **Problem statement**
	 - 1.a. **Describe the game** you are asked to solve, within a few lines.
	 - 1.b. Formalize the game as a **search problem**, i.e. in terms of:
		 - Set of all possible states
		 - Set of all possible actions
		 - Transition model
		 - Goal test
		 - Step cost (must be > 0)
 2.  **A\* implementation**
	 - 2.a. Implement A* algorithm with **your own cost function** $g(n)$  and **admissible heuristic** $h(n)$. The algorithm should be implemented inside the `get_action` function of the corresponding Python file `astar.py`, following the template of `pacmanagent.py`.
		 - You must have $g(n)$ different from $depth(n)$
		 - You must have $h(n)$ different from 0 everywhere.
		 - You must prevent cycles. A cycle is a path where a given state occurs at least twice.
	  - 2.b. Define and describe formally your cost function $g(n)$ and your heuristic $h(n)$.
	  - 2.c. **Show** that your $h(n)$ is **admissible**.
 3. **Experiment 1** 
	 - 3.a. Run A* with your own $g(n)$ and $h(n)$ and  A* with your own $g(n)$ and $h(n) = 0$ everywhere against the 3 maze layouts located the  `/pacman_module/layouts/` folder. For each layout, report the results as a bar plot in terms of:
		 - Score
		 - Number of expanded nodes
	- 3.b. Describe the changes between the results of the two runs.
	- 3.c. Justify those changes using the course.
	- 3.d. Which algorithm corresponds A* with $h(n) = 0$ everywhere to ? 
 4. **Experiment 2** 
	 - 4.a. Run A* with your own $g(n)$ and $h(n)$, DFS and BFS against the 3 maze layouts located the  `/pacman_module/layouts/` folder. For each layout, report the results as a bar plot in terms of:
		 - Score
		 - Number of expanded nodes
	  - 4.b. Describe the changes between A* and DFS/BFS. 
	  - 4.c. Justify the changes between A* and DFS/BFS using the course.
 5. **Experiment 3**   
	   - 5.a. Run A* with $g(n) = depth(n)$ and $h(n) = 0$ everywhere against the 3 maze layouts located the  `/pacman_module/layouts/` folder. For each layout, report the results as a bar plot in terms of:
		   - Score
		   - Number of expanded nodes 
	  - 5.b. Describe those results compared to DSF/BFS and justify your observations using the course.
	  - 5.c. Which algorithm corresponds A* with $g(n) = depth(n)$ and $h(n) = 0$ everywhere to ? 
 6. **Project feedback (BONUS)** <br/> You're expected to provide a short and constructive feedback about the project. In particular, you should discuss about the experience the project has brought to you and about the difficulties you may have encountered during the project. 

Your report should the subdivision provided above. A template with a predefined structure will be provided in order to standardize the report for all students. 

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
		* 3 point : execution time $<$ 2 sec.
		* 2.25 points: exection time between 2 and 5 sec.
		* 1.5 point: exection time between 5 and 10 sec.
		* 0.75 point: inaccurate results and/or execution time $>$ 10 sec.
		* 0 point: no result.

**Report** - 10 points

1. **Problem statement** - 5 points
	* **Set of states** - 1 point
	* **Set of actions** - 1 point
	* **Transition model** - 1 point 
	* **Goal test** - 1 point
	* **Step cost** - 1 point</br>
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

## Credits

Credits: [UC Berkeley](http://ai.berkeley.edu/project_overview.html)
