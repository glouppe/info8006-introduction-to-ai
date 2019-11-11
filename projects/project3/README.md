
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
	 - Your report must be at most **5** pages long.
	 - Fill in the following [template](https://github.com/glouppe/info8006-introduction-to-ai/blob/master/projects/project3/template-project3.tex) to write your report.
	 - In French or English.
 - A file named `bayesfilter.py` containing your implementation of the Bayes filter algorithm.
	 - Put the class template defined in `beliefstateagent.py` into `bayerfilter.py` and fill in the `update_belief_state` function.

:warning: A penalty of **-2 points** on the final grade will be applied if the files are not named based on the instructions above.

---

## Instructions

This part is due by **December 8, 2019 at 23:59**. This is a **hard** deadline.

In this third part of the project, Pacman got tired of ghosts wandering around him. So he has decided to buy a laser gun and kill them. But while he shot them, he figured out that the gun has instead turned them into invisible but edible ghosts! Fortunately, as it was part of a box that he bought from a flea market, he had also discovered a rusty sensor, which still works but is subject to measurement errors which are described in the user manual.

A lot of confusion arose since Pacman shot them. He has no idea where they can currently be in the maze. However, he knows that the ghosts are confused and should be willing to escape from him.
More precisely, he knows that `scared` is more fearful than `afraid` who is more fearful than `confused`.

Your task is to design an intelligent agent based on the Bayes filter algorithm (see [Lecture 7](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture7.md)) for locating all the ghosts in the maze.

You may the following command line which launchs a game where the sole, eadible and invisible `scared` ghost wanders around the maze while Pacman tries to locate him with a (very) rusty sensor:
```bash
python run.py --bsagent beliefstateagent.py --ghostagent scared --nghosts 1 --edibleGhosts --hiddenghosts --lmbda 100 --seed -1
```
Change the value of `seed` - for random number generator - to a positive value to ease reproducibility of your experiments.

You are asked to answer the following questions:

 1. **Filter Components**

	- 1.a. - **1 point** - Describe the parametrized model of the rusty sensor (see `_get_evidence` of the `BeliefStateAgent` class).
	- 1.b. - **1 point** - Describe the belief state structure related to the ghost position.
	- 1.c. - **1 point** - Describe the transition model of `scared` (see `/pacman_module/ghostAgents.py`).
	- 1.d. - **1 point** - Describe the transition model of `afraid` (see `/pacman_module/ghostAgents.py`).
	- 1.e. - **1 point** - Describe the transition model of `confused` (see `/pacman_module/ghostAgents.py`).
	- 1.f. - **1 point** - Provide a single parametrized transition model which describes `scared`, `afraid` and `confused` by only picking a value for the unique parameter.  


 2. **Implementation**
 	- 2.a. - **3 points** - Implement the **Bayes filter** algorithm. This should be done in the `update_belief_state` function of `bayesfilter.py`, following the template of `beliefstateagent.py`.
		 - Your implementation must work with multiple ghosts. You may assume that the multiple ghosts are actually copycats of one of the abovementioned ghosts. 
		 - The belief state updated by your implementation must eventually converge to an uncertainty area for each ghost.
		 - You may assume access to the Pacman's position.
	- 2.b. - **1 point** - Might the sensor return abnormal data? If so, how does it affect the behavior of your filter implementation? Motivate your answer.

 3. **Experiment**
 	- 3.a. - **2 points** - Provide a measure of the uncertainty of the belief state(s).
	- 3.b. - **2 points** - Provide a measure of the quality of the belief state(s). You may assume access to the ground truth.
	- 3.c. - **3 points** - Run your filter implementation several times on the `/pacman_module/layouts/large_filter.lay` layout, against all ghosts and 5 carefully chosen parameters of the rusty sensor.
		 - Record the two aforementioned measures (see `_record_metrics` function in `beliefstateagent.py`) over trials and time.
		 - As the number of pages of the report is limited, we advise you to minimise the number of plots by combining curves whenever possible.
		 - You need to mention the 5 parameters that you have chosen for the rusty sensor. Otherwise, your curves will be considered as not provided.
		 - Each curve that does not correctly plot a mean and a variance through several simulations will be considered as not provided.
		 - Your number of simulations needs to be high enough and their duration long enough so that the two aforementioned measures have eventually converged, in terms of mean and variance, over time and for each timestep.
			 - Each curve that does not fulfill the abovementioned condition will be considered as not provided.   
	- 3.d. - **1 point** - How does the ghost transition model parameter affect its behavior and impact the belief state updates? Motivate your answer by using your measures and the model itself.
	- 3.e. - **1 point** - How does the rusty sensor parameter affect its behavior and impact the belief state updates? Motivate your answer by using your measures and the model itself.
	- 3.f. - **1 point** - How would you implement a stochastic Pacman controller eager to eat ghosts using only its current position, the set of legal actions and the current belief state?
		- You do not need to provide a pseudo-code algorithm, just explain intuitively and in a few lines your implementation strategy.


---

## Evaluation

In this section, you can find the criteria according to which the different questions will be evaluated, as well as some additional elements of evaluation of your code and report.

For each **implementation question** (2.a), provide simply references to your code in your report. The evaluation of your code will be performed as follows:
 - 100% points: correct implementation of the algorithm and its components.
 - 75% points: correct implementation w.r.t. the pseudo-code but errors related to the search problem.
 - no point: implementation error of any component of the algorithm.

For each **discussion question** (1.a, 1.b, 1.c, 1.d, 1.e, 1.f, 2.b, 3.a, 3.b, 3.d, 3.e, 3.f), the evaluation will be performed as follows:

 - 100% points: complete answer.
 - 50% points: some relevant elements but incomplete and/or incorrect answer.
 - no point: no relevant element or no answer.

Questions implying the inclusion of **plots** (3.c) in the report will be evaluated considering the following criteria:

 - Presence: your resulting grade will be half the ratio between the provided and expected number of relevant curves.
 - Readability: Each curve that is not clearly readable/identifiable will be considered as not provided.
 - Scale: All the curves on each plot that is not correctly scaled will be considered as not provided.

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
