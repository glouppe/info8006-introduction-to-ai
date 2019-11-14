
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
	 - Put the class template defined in `beliefstateagent.py` into `bayesfilter.py` and fill in the `update_belief_state` function.

:warning: A penalty of **-2 points** on the final grade will be applied if the files are not named based on the instructions above.

---

## Instructions

This part is due by **December 8, 2019 at 23:59**. This is a **hard** deadline.

In this third part of the project, Pacman got tired of ghosts wandering around him. So he decided to buy a laser gun and kill them. But while he shot them, he figured out that the gun has instead turned them into invisible but edible ghosts! Fortunately, as it was part of a box that he bought from a flea market, he also got his hands on a rusty sensor, which still works but is subject to measurement errors which are described in the user manual.

A lot of confusion arose since Pacman shot the ghosts: he has no idea where they currently are in the maze! However, he knows that the ghosts are confused and should be willing to escape from him.
More precisely, he knows that `scared` is more fearful than `afraid` who is more fearful than `confused`.

Your task is to design an intelligent agent based on the Bayes filter algorithm (see [Lecture 7](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture7.md)) for locating all the ghosts in the maze.

You may use the following command line to start a game where the sole eadible `scared` ghost wanders around the maze while Pacman tries to locate him with a (very) rusty sensor:
```bash
python run.py --bsagent beliefstateagent.py --ghostagent scared --nghosts 1 --seed -1
```
Change the value of `seed` - for random number generator - to a positive value to ease reproducibility of your experiments.

You are asked to answer the following questions:

 1. **Bayes filter**
	- 1.a. - **1 point** - Describe the sensor model of the rusty sensor, as implemented in `_get_evidence` of the `BeliefStateAgent` class.
	- 1.b. - **2 points** - Provide a unified parametrized transition model from which the ghosts `scared`, `afraid` and `confused` can be derived. Derive this model from the ghost implementations found in `/pacman_module/ghostAgents.py`. Your model should specify a single free parameter.

    Answers to the previous questions should not make any reference to the API nor include pseudo-code.

 2. **Implementation**
 	- 2.a. - **5 points** - Implement the **Bayes filter** algorithm to compute Pacman's belief state. This should be done in the `update_belief_state` function of `bayesfilter.py`, following the template of `beliefstateagent.py`.
		 - Your implementation must work with multiple ghosts (all running the same policy).
		 - Pacman's belief state should eventually converge to an uncertainty area for each ghost.
		 - Your filter should consider the Pacman position.

 3. **Experiment**
 	- 3.a. - **1 point** - Provide a measure which summarizes Pacman's belief state (i.e., its uncertainty).
	- 3.b. - **1 point** - Provide a measure of the quality of the belief state(s). You may assume access to the ground truth.
	- 3.c. - **4 points** - Run your filter implementation on the `/pacman_module/layouts/large_filter.lay` and the `/pacman_module/layouts/large_filter_walls.lay` layouts, against each type of ghost. Report your results graphically.
		 - Record your measures (see `_record_metrics` function in `beliefstateagent.py`) over several trials.
		 - Your results should come with error bars.
		 - The number of trials must be high enough and their duration long enough so that the measures have converged.
	- 3.d. - **2 points** - Discuss the effect of the ghost transition model parameter on its own behavior and on Pacman's belief state. Consider the two provided layouts. Motivate your answer by using your measures and the model itself. Use the default sensor variance.
	- 3.e. - **2 points** - Discuss the effect of the sensor variance (as set through the `--sensorvariance` command line argument) on Pacman's belief state.
	- 3.f. - **2 points** - How would you implement a stochastic Pacman controller to eat ghosts using only its current position, the set of legal actions and its current belief state?


---

## Evaluation

In this section, you can find the criteria according to which the different questions will be evaluated, as well as some additional elements of evaluation of your code and report.

For each **implementation question** (2.a), provide simply references to your code in your report. The evaluation of your code will be performed as follows:
 - 100% points: correct implementation of the algorithm and its components.
 - 50% points: correct implementation w.r.t. the pseudo-code but errors related to the search problem.
 - no point: implementation error of any component of the algorithm.

For each **discussion question** (1.a, 1.b, 2.b, 3.a, 3.b, 3.d, 3.e, 3.f), the evaluation will be performed as follows:

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
