
# Project 3

## Table of contents

- [Deliverables](#deliverables)
- [Instructions](#instructions)
- [Evaluation](#evaluation)
- [Credits](#credits)

---

## Deliverables

You are requested to deliver:
- A `report.pdf` file, based on the `report.tex` template.
- A file named `bayesfilter.py` containing your implementation of the Bayes filter algorithm and the agent eating ghosts.
     - Simply modify the provided `bayesfilter.py` file.
	 - :warning: Do not change the class names.

## Instructions

In this third part of the project, Pacman got tired of ghosts wandering around him. So he decided to buy a laser gun and kill them. But while he shot them, he figured out that the gun has instead turned them into invisible but edible ghosts! Fortunately, as it was part of a box that he bought from a flea market, he also got his hands on a rusty sensor, which still works but is subject to measurement errors which are described in the user manual.

A lot of confusion arose since Pacman shot the ghosts: he has no idea where they currently are in the maze! However, he knows that the ghosts are confused and should be willing to escape from him.
More precisely, he knows that the first ghost, named `terrified`, is more fearful than the second ghost, named `afraid`, who is more fearful than the third ghost, named `fearless`.

Your task is to design an intelligent agent based on the Bayes filter algorithm (see [Lecture 6](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture6.md)) for locating all the ghosts in the maze.

You may use the following command line to start a game where the sole eadible `afraid` ghost wanders around the maze while Pacman, controlled by the `humanagent.py` policy, tries to locate him with a (very) rusty sensor:
```bash
python run.py  --agent bayesfilter --ghost afraid --nghosts 1 --seed -1 --layout large_filter
```
Note that when you use multiple ghosts, they all run the same policy (e.g., all `afraid`). Change the value of `seed` - for random number generator - to a positive value to ease reproducibility of your experiments.

## Implementation

1. Implement the **Bayes filter** algorithm to compute Pacman's belief state. This should be done in the `_get_updated_belief` function of `bayesfilter.py`. Your function `_get_updated_belief` should use the functions `_get_sensor_model` and `_get_transition_model` that you should also define yourself.

 	 * Your implementation must work with multiple ghosts (all running the same policy).
 	 * Pacman's belief state should eventually converge to an uncertainty area for each ghost.
 	 * Your filter should consider the Pacman position, as Pacman may wander freely in the maze.

2. implement a Pacman controller to eat ghosts using only its current position, the set of legal actions and its current belief state

## Report

In addition to `bayesfilter.py` and `pacmanagent.py`, you are asked to submit a short (2 pages) report.

1. Describe mathematically the sensor model of the rusty sensor, as implemented in `_get_evidence` of the `BeliefStateAgent` class.

2. Provide a unified parametrized transition model from which the ghosts `scared`, `afraid` and `confused` can be derived. Derive this model from the ghost implementations found in `/pacman_module/ghostAgents.py` (functions `getDistribution`). Your model should specify a single free parameter.
     
     :warning: Be aware that in project 2, the ghosts are now able to go move backward, on the contrary to project 1.

    Answers to the previous questions should not make any reference to the API nor include pseudo-code.

## Evaluation

Your project will be evaluated as follow:

- **Report** : We evaluate the correctness and precision of your answers.
- **Transition model** : We evaluate the correctness.
- **Sensor model** : We evaluate the correctness.
- **Bayes filter model** : We evaluate the correctness.
- **Pacman controller**: We evaluate whether you agent is able to eat the ghosts.
- **Code style** (5%): No points are awarded if your code is not PEP-8 compliant.

## Credits

The programming projects are adapted from [CS188 (UC Berkeley)](http://ai.berkeley.edu/project_overview.html).
