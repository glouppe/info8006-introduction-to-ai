class: middle, center, title-slide

# Introduction to Artificial Intelligence

Fall 2017

---

# Organization

## Logistics
- Prof. Gilles Louppe ([g.louppe@ulg.ac.be](mailto:g.louppe@ulg.ac.be))
- Teaching assistant: Samy Aittahar ([saittahar@ulg.ac.be](mailto:saittahar@ulg.ac.be))

.pull-right[![Textbook](./figures/textbook.png)]
## Textbook
Stuart Russel, Peter Norvig. "Artificial Intelligence: A Modern Approach", Third Edition, Global Edition.
(*Strongly recommended*)

Slides are partially adapted from:
- [CS188 Introduction to AI](http://ai.berkeley.edu/lecture_slides.html) (UC Berkeley)
- [CS430 Introduction to AI](http://web.engr.oregonstate.edu/~tgd/classes/430/) (Oregon State University)

---

# Lectures

- Theoretical lectures
- Exercise sessions

---

# Evaluation

- Oral exam (50%)
- Programming project 1 (15%)
- Programming project 2 (35%)

---

# Philosophy

## Thorough and detailed

- Understand the landscape of artificial intelligence.
- Be able to write from scratch, debug and run (some) AI algorithms.

## Well established algorithms and state-of-the-art

- Well-established algorithms for building intelligent agents.
- Introduction to materials new from research ($\leq$ 5 years old).
- Understand some of the open questions and challenges in the field.

## Practical

- Fun and challenging course project.

---

class: middle, center

# Outline

---

# 1. Foundations

-   The foundations, history and state-of-the-art *(Chapter 1)*
-   Intelligent agents: modeling a rational behavior in a complex environment *(Chapter 2)*

---

# 2. Solving problems by searching

-   Basic search methods *(Chapter 3)*

???

-   Local search, non-determinism, partial observability *(Chapter 4)*

---

# 3. Games

-   Games, optimal decisions, stochastic game, partially observable games, ... *(Chapter 5)*
-   *Extra:* Deep Blue, AlphaGo, DeepStack, Starcraft

---

# 4. Constraint satisfaction problems

- CSPs, backtracking, local search, ... *(Chapter 6)*

???

or planning?

---

# 5. Probabilistic reasoning I

-   Quantifying Uncertainty *(Chapter 13)*
-   Probabilistic reasoning *(Chapter 14)*
-   *Extra:* Probabilistic reasoning vs. logic-based reasoning *(Chapters 7-9)*

---

# 6. Probabilistic reasoning II

-   Probabilistic reasoning over time *(Chapter 15)*
-   Learning probabilistic models *(Chapter 20)*
-   *Extra:* Celeste paper; Modern tools for probabilistic models (Stan, etc)

---

# 7. Learning

-   Discussion on the need for learning
-   Overview of various learning paradigms *(Chapters 18, 19, 20, 21)*
-   *Extra:* Deep learning as a promising path towards AI (Bengio)

---

# 8. Communication

-   Natural language processing *(Chapter 22)*.
-   Natural language for communication *(Chapter 23)*.
-   *Extra:* Q&A systems

---

# 9. Perception

-   Computer vision *(Chapter 24)*
-   Attention mechanisms *(Research)*
-   *Extra:* Autonomous vehicles

---

# 10. Artificial General Intelligence

-   Recursive self-improvement, meta learning *(Research)*
-   AIXI *(Research)*

---

# 11. Philosophical foundations and future of AI

-   Philosophical foundations *(Chapter 26)*
-   Future of AI, open challenges, safety *(Chapter 27)*
-   *Extra:*  Probably approximately correct theory

---

class: middle, center

# Projects

---

# Projects

.grid[
.col-2-3[
- Programming project 1 (15%):
    - Implement a simple agent for *tic-tac-toe* (3x3 and larger grids)
- Programming project 2 (35%):
    - Implement an intelligent **Pacman** agent
    - Increasing levels of intelligence
]
.col-1-3[
![](figures/outline/morpion.jpg)
![](figures/outline/pacman.png)
]
]
