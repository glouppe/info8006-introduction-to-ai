class: middle, center, title-slide

# Introduction to Artificial Intelligence

Lecture 3: Games

---

# Today

---

class: center

# Ignore the Blonde

<iframe width="560" height="315" src="https://www.youtube.com/embed/LJS7Igvk6ZM" frameborder="0" allowfullscreen></iframe>

---

# Games

- A **game** is a multi-agent environment where agents may have either *conflicting* or *common* interests.
- Opponents may act **arbitrarily**, even if we assume a deterministic fully observable environment.
    - Therefore the solution to a game is a *strategy* specifying a move for every possible opponent reply.
    - This is different from search where a solution is a *fixed* sequence.
- Time **limits**.
    - Branching factor is often very large.
        - In chess, $b\approx 35$ and games usually last for 100 moves. The size of the search tree is $O(35^{100})$.
    - Unlikely to find goal with standard search algorithms, we need to *approximate*.

---

# Types of games

Types of games:
- Deterministic or stochastic?
- One, two or more players?
- Zero-sum game?
- Perfect information?


We assume *deterministic*, *turn-taking*, *two-player* **zero-sum games** of *perfect information*.

---

# Formal definition

A **game** is formally defined as kind of search problem with the following components:
- The *initial state* $s_0$ of the game.
- A function $\text{player}(s)$ that defines which *player* $p \in \\{1, ..., N \\}$ has the move in state $s$.
- A description of the legal *actions* available to a state $s$, denoted $\text{actions}(s)$.
- A *transition model* that returns the state $s' = \text{result}(s, a)$ that results from doing action $a$ in state $s$.
- A *terminal test* which determines whether the game is over.

---

- A *utility function* $\text{utility}(s, p)$ (or payoff) that defines the final numeric value for a game that ends in $s$ for a player $p$.
    - E.g., $1$, $0$ or $\frac{1}{2}$ if the outcome is win, loss or draw.
- Together, the initial state, the $\text{actions}(s)$ function, the $\text{result}(s, a)$ function and the terminal test define the **game tree**.
    - *Nodes* are game states.
    - *Edges* are moves.

---

# Game tree

.width-100[![](figures/lec3/tictactoe.png)]

---

# Zero-sum games

- In a **zero-sum** game, the total payoff to all players is *constant* for all games.
    - E.g., $0+1$, $1+0$ or $\frac{1}{2} + \frac{1}{2}$.
- That is, for two-player games, agents have **opposite** utilities (values and outcomes).
- Equivalently, agents share the same utility function, but one wants to *maximize* it while the other wants to *minimize* it.
- Adversarial, *pure competition*.

.center.width-50[![](figures/lec3/zero-sum-cartoon.png)]

.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

---

# Adversarial search

.grid[
.col-2-3[
- In a search problem, the optimal solution is a sequence of actions leading to a goal state.
    - i.e. a terminal state that is a win.
- In a game, the opponent may react *arbitrarily* to a move.
- Therefore, a player must define a contingent **strategy** which specifies
    - its moves in the initial state,
    - its moves in the states resulting from every possible response by the opponent,
    - its moves in the states resulting from every possible response by the opponent in those states,
    - ...
]
.col-1-3[
![](figures/lec3/adversarial-search-cartoon.png)
]
]

<span class="Q">[Q]</span> What is an optimal strategy? How do we find it?

.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]


---

# Minimax

- Assume a two-player game between players MIN and MAX.
    - MAX maximizes the game's $\text{utility}$ function.
    - MIN minimizes the game's $\text{utility}$ function.
- The **minimax value** $\text{minimax}(s)$ is the largest payoff that MAX can get from state $s$, assuming that MIN plays optimally.

.center.width-100[![](figures/lec3/minimax.png)]

---

# Alpha-beta pruning

---

# Imperfect real-time decisions

---

# Stochastic games

---

# Partially observable games

---

# State-of-the-art game programs

---

# Monte Carlo tree search

---

# Summary

---

# References
