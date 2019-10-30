
# Project III

## Table of contents

- [Deliverables](#deliverables)
- [Instructions](#instructions)
- [Evaluation](#evaluation)
- [Credits](#credits)

---

## Deliverables

You are requested to deliver a *tar.gz* archive containing:
 - Your report named `report.pdf`.
	 - Your report must be at most **?** pages long.
	 - Fill in the following [template](https://github.com/glouppe/info8006-introduction-to-ai/blob/master/projects/project3/template-project3.tex) to write your report.
	 - In French or English.
 - Your `bayerfilter.py` file containing your implementation of the Bayes Filter algorithm.
	 - Put the class template defined in `beliefstateagent.py` into `bayerfilter.py` and fill in the `forward_pass` function.

:warning: A penalty of **-2 points** on the final grade will be applied if the files are not named based on the instructions above.

---

## Instructions

This part is due by **November 10, 2019 at 23:59**. This is a **hard** deadline.

In this third part of the project, Pacman got tired of these ghosts wandering around him. So he has decided to buy a laser gun which transforms them into cookies. Unfortunately, he didn't know that the gun had the unpleasant side effect to make them invisible at the same time! Fortunately, as it was part of a box that he bought from a flea market, he had also discovered a rusty sensor, which still works but is subject to a measure error which is described in the user manual. 

A lot of confusion arised since Pacman shot them. He has no idea where they can currently be in the maze. However, he knows that the ghosts are confused and should be willing to escape from him.

More precisely, he knows that `aafraid` is more fearful than `afraid` who is more fearful than `confused`.

Your task is to design an intelligent agent based on bayes filtering algorithm (see [Lecture 7](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture7.md)) for localizing all the ghosts in the maze.

You are asked to answer the following questions.

 1. **Filter Components**

	 - 1.a. - **1 point** - Describe the model of the rusty sensor which is implemented inside the method `_getEvidence` of the `BeliefStateAgent` class.
         - 1.b. - **1 point** - Describe the transition model of `aafraid`
         - 1.c. - **1 point** - Describe the transition model of `afraid`
         - 1.d. - **1 point** - Describe the transition model of `confused`
         - 1.e. - **1 point** - Provide a parametrized transition model which is capable to describe `aafraid`, `afraid` and `confused` by only picking a value for the unique, positive parameter.  
         - 1.f. - **1 point** - How does the parameter affects the behavior of the transition model ?

 2. **Implementation**



 3. **Experiment**


---

## Evaluation

In this section, you can find the criteria according to which the different questions will be evaluated, as well as some additional elements of evaluation of your code and report.

For each **implementation question** (?), provide simply references to your code and to your cutoff-tests and evaluation functions in your report. The evaluation of your code will be performed as follows:
 - 100% points: correct implementation of the algorithm and its components.
 - 75% points: correct implementation w.r.t. the pseudo-code but errors related to the search problem.
 - no point: implementation error of any component of the algorithm.

For each **discussion question** ?), the evaluation will be performed as follows:

 - 100% points: complete answer.
 - 50% points: some relevant elements but incomplete and/or incorrect answer.
 - no point: no relevant element or no answer.

Questions implying the inclusion of **plots** (?) in the report will be evaluated considering the following criteria:

 - Presence: your resulting grade will be half the ratio between the provided and expected number of relevant bars.
 - Readability: Each bar that is not clearly readable/identifiable will be considered as not provided.
 - Scale: All the bars on each plot that is not correctly scaled will be considered as not provided.

Besides the questions you're expected to answer, you will also be evaluated according to the following criteria:

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
