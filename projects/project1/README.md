# Project I

## Table of contents

- [Deliverables](#deliverables)
- [Instructions](#instructions)
- [Evaluation](#evaluation)
- [Credits](#credits)

---

## Deliverables

You are requested to deliver a *tar.gz* archive containing:
 1. Your report named `report.pdf`.
     - Your report must be at most **5** pages long.
     - Fill in the following [template](./template-project1.tex) to write your report.
     - In French or English.
     
 2. Your `minimax.py` file that implements the Minimax algorithm.

 3. Your `hminimax0.py` file that implements the H-Minimax algorithm with your best cut-off/heuristic functions pair.

 4. Your `hminimax1.py` file that implements the H-Minimax algorithm with your second best cut-off/heuristic functions pair.

 5. Your `hminimax2.py` file that implements the H-Minimax algorithm with your third best cut-off/heuristic functions pair.

  Put the template defined in `pacmanagent.py` into each of the `*.py` files and fill in the `get_action` function differently for each file.

:warning: A penalty of **-2 points** on the final grade will be applied if the files are not named based on the instructions above.

---

## Instructions

This part is due by **October 28, 2021 at 23:59**. This is a **hard** deadline.

In [project 0](../project0), Pacman could wander peacefully in its maze. In this *project 1*, he needs to avoid a walking ghost that would kill it if it reached his position. And Pacman has not idea of (i) what is the objective of the ghost (whether the ghost wants to kill him or not) and (ii) if it is playing optimally for achieving its goal. Pacman only knows that the ghost cannot make a half-turn unless it has no other choice.

The ghost follows one of the following policies, as set through the `--ghostagent` command line option:
 - `dumby`: Rotate on itself in a counterclockwise fashion until it can go on its left.
 - `greedy`: Select the next position that is the closest to Pacman.
 - `smarty`: Select the next position which leads to the shortest path towards Pacman.

:warning: But as specified above, Pacman is not aware of the policy that the ghost follows.

Your task is to design an intelligent agent based on adversarial search algorithms (see [Lecture 3](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture3.md)) for maximizing the score. In this project, we will not consider layouts with capsules, but you may take them into account if you feel motivated. You can start by downloading the [archive](../project1.tar.gz) of the project. In order to run you code, you can use the following command (replacing `humanagent.py` by `minimax.py` for example):

```
python3 run.py --agentfile humanagent.py --ghost dumby --layout small_adv
```

You are asked to answer the following questions.

 1. **Problem Statement -- 4.5 points**
    
     - 1.a. - **4 points** - Formalize the game as an **adversarial search problem** by proposing a definition of the following elements **for this particular problem**:
       
        - The *set of states* of this game
            - You must specify the initial state
        - The function `player(s)` that defines which player has the move (1 for Pacman, 0 for Ghost) in state `s`
        - The function `action(s)` that defines the legal actions available in state `s`
        - The transition model that returns the state `s' = result(s, a)` that results from taking action `a` in state `s`
        - The terminal test `terminal(s)` that determines whether state `s` is terminal (1 for terminal, 0 for non terminal)
        - The utility function `utility(s, p)` that defines the final numerical value for a game that ends in state `s` for player `p`.
            - You should define it for player `p = Pacman` only
            - Remember for game one that the game score function is defined as:
            ```
            score = -#time steps + 10*#number of eaten food dots - 5*#number of eaten capsules + 200*#number of eaten ghost + (-500 if #losing end) + (500 if #winning end)
            ```

        Any **reference to the API** in any component of the problem statement will be considered as **false** (i.e. you can not use function or variables defined in the code in your formalization).

     - 1.b. - **0.5 points** - How would you define `utility(s, p)` for `p = Ghost`, if the game was a zero-sum game.

 2. **Implementation -- 9 points**

     - 2.a. - **1 point** - Consider the direct application of Minimax with respect to the problem statement, by assuming that the game is a zero-sum game.

        - Discuss its completeness with respect to the game of Pacman.

        - From the point of view of Pacman, by looking at the utility function, is there an advantage in going through a cycle (i.e., going back to an already visited state `s`)?

        - In view of that, discuss how you could guarantee the completeness of Minimax by adapting the components described in the problem statement, while keeping the same set of optimal strategies.
        
     - 2.b. - **4 points** - Implement the **Minimax** algorithm as specified in section [Deliverables](#deliverables) in `minimax.py`.
       
         - You must **guarantee the completeness** of the algorithm.

         - Your Minimax agent needs to **provide an optimal strategy in the smaller map** `./pacman_module/layouts/small_adv.lay` against all kinds of ghosts.

         - In your report, just refer your code.
         
     - 2.c. - **4 points** - Implement the **H-Minimax** algorithm with your own **cutoff-tests** and **evaluation functions** in `hminimax0.py`, `hminimax1.py` and `hminimax2.py`. You are expected to provide **3 cutoff-test/evaluation function pairs**, with **at least two different evaluation functions**. At most two of them might fail against some ghosts/layouts as long as the heuristics do still make sense. We expect you to design winning heuristics while being able to provide possible explanations on failing heuristics.
       
         - Each proposed evaluation function needs to differ from the game score function.
         
         - Your evaluation functions need to be **fast** to compute and **generalizable**.
         
         - Evaluation functions can be built by weighting the different characteristics of the game state, but this is not a constraint.
         
         - Your different evaluation/cut-off functions must be significantly different (changing the value of a parameter is not sufficient)
         
         - In your report, refer your codes and the describe formally your different cutoff-tests and evaluation functions.
         
           N.B.: Although 3 layouts are provided for this project, you remain free to build your own layouts in order to fit the most general cutoff-test/evaluation function pair as possible. If you do so, discuss it briefly in your report.
     
 3. **Experiment -- 4 points**

    - 3.a. - **2 points** - Run your H-Minimax agent against `./pacman_module/layouts/large_adv.lay` layout and all ghosts, using your 3 cutoff-test/evaluation function pairs. Report your 9 results as bar plots in terms of (i) score, (ii) time performances and (iii) number of expanded nodes.      

        - As the number of pages of the report is limited, we advise you to minimise the number of plots by combining bars whenever possible

        - Pay attention to the clarity of your plots (e.g. by labelling the axes, adding a legend, and puting a caption in your LaTeX report).

    - 3.b. - **2 points** - **Summarize** the results of your cutoff-test/evaluation function pairs, according to the type of ghosts. **Explain** these results, notably by referring to the course.
    
    NB: there are additional evaluation criteria that you can find in section [Evaluation](#evaluation).

---

## Evaluation

Besides the questions you're expected to answer, you will also be evaluated according to the following criteria:
 - **Code performance** - **2 points** - Your code will be tested on the submission platform machines. After each submission, you will receive a feedback which will contain information about the accuracy of your results and the time performances of your code.  
     - 2 points: <= 30 seconds
     - 0 point: > 30 seconds

 - **Code style** - **2 points**
     - **PEP8 compatibility** - **0.8 point** - PEP8 guidelines are provided at [Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/). A script will be executed to check the compatibility of your code.
         - 0.8 point : the script runs without error.
         - 0 point: any error during the execution of the script.
     - **Specification** - **1.2 point** - correctness of the specification of your functions.
        - 1.2 point : all specifications are correct.
        - 0.9 point : at least 75% correct specifications.
        - 0.6 point : at least 50% correct specifications.
        - 0.3 point : at least 25% correct specifications.
        - 0 point : less than 25% correct specifications.

Note that your implementation might be tested on other layouts.

:warning: Take care of providing a clearly written report, which fully follows the provided template. We reserve the right to refuse to evaluate a report (i.e. to consider it as not provided) which would be difficult to read and understand. We may also refuse to evaluate discussion blocks that are truly confusing, even if the underlying idea might be right. Sanctions will be imposed in case of non-respect of the guidelines about the structure and length of the report:

 - Any modification of the template: **- 2 points**
 - Only the first 5 pages of the report will be taken into account for the evaluation.

:warning: Plagiarism is checked and sanctioned by a grade of 0. Cases of plagiarism will all be reported to the Faculty.

---

## Credits

The programming projects are adapted from [CS188 (UC Berkeley)](http://ai.berkeley.edu/project_overview.html).
