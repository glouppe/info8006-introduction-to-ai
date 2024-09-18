# Project 2

## Deliverables

You are requested to deliver:
- A file named `bayesfilter.py` containing your implementation of the Bayes filter algorithm and the agent eating ghosts. Simply modify the provided `bayesfilter.py` file.

## Instructions

In this third part of the project, Pacman got tired of ghosts wandering around him, so he bought a magic gun that make the ghosts edible. But while he shot them, he figured out that the gun also made them invisible. Fortunately, he also got his hands on a rusty distance sensor. The sensor returns a noisy Manhattan distance between pacman and each ghost, which Pacman can use as evidence to find the ghost positions. The noisy distance, denoted $e$, results from the addition of noise to the true Manhattan distance, the noise being sampled from a binomial distribution centered around 0. 

$$e = \text{ManhattanDistance}(\text{Pacman}, \text{Ghost}) + z - np \qquad z \sim \text{Binom}(n, p),$$

where $n=4$ and $p=0.5$.

Pacman knows that the ghosts are afraid of him and are more likely to take actions that makes it move away from him. Their exact action policy of the ghosts (`afraid`, `fearless` and `terrified`) should be deducted from the [ghostAgents.py](pacman_module/ghostAgents.py) file.

Your task is to design an intelligent agent based on the Bayes filter algorithm (see [Lecture 6](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture6.md)) for locating and eating all the ghosts in the maze.

1. Implement the **Bayes filter** algorithm to compute Pacman's belief state of the ghost positions. To do so, fill in the three methods `transition_matrix`, `observation_matrix` and `update` of the `BeliefStateAgent` class. `update` must rely on `transition_matrix` and `observation_matrix`.
2. Implement a Pacman agent whose goal is to eat all the ghosts as fast as possible. However, at each step, the agent only has access to its own position and the current belief state of the ghost positions. To do so, fill in the `_get_action` method of the `PacmanAgent` class.

To get started, download and extract the [archive](../project2.zip?raw=true) of the project in the directory of your choice. Use the following command to run your Bayes filter implementation against a single `afraid` ghost in the `large_filter` layout:
```console
$ python run.py --ghost afraid --nghosts 1 --layout large_filter --seed 42
```
When several ghosts are present in the maze, they all run the same policy (e.g. all `afraid`). The random seed of the game can be changed with the `--seed` option.

## Evaluation
Your project will be evaluated based on the correctness of each of the components (transition_matrix function, observation_matrix function, update (bayes filter) function and pacman controller) and code style. To avoid error propagation, your update function will be evaluated while coupled with our own implementation of transition_matrix and observation_matrix functions. That way any error in the transition_matrix and observation_matrix functions will not impact the correctness of your update function. Public tests only perform sanity checks (correct ouput shape, check if the output is a valid probability distribution, ...). The correctness tests are private and **we encourage you to make your own tests** to test the correctness of your implementation. 

Your project will be evaluated as follow:

- **transition_matrix function** (25%): We evaluate the correctness of the component.
- **observation_matrix function** (25%): We evaluate the correctness of the component.
- **update function** (25%): We evaluate the correctness of the component.
- **Pacman controller** (20%): We evaluate whether you agent is able to eat the ghosts in a reasonable amount of time.
- **Code style** (5%): You are awarded the maximal grade if your code is PEP-8 compliant and no points otherwise. This test is public.
