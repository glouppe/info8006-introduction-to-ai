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

- Deterministic or stochastic?
- One, two or more players?
- Zero-sum game?
- Perfect information?

XXX: add table


---

# Formal definition

A **game** is formally defined as kind of search problem with the following components:
- The *initial state* $s_0$ of the game.
- A function $\text{player}(s)$ that defines which *player* $p \in \\{1, ..., N \\}$ has the move in state $s$.
- A description of the legal *actions* (or *moves*) available to a state $s$, denoted $\text{actions}(s)$.
- A *transition model* that returns the state $s' = \text{result}(s, a)$ that results from doing action $a$ in state $s$.
- A *terminal test* which determines whether the game is over.

---

- A *utility function* $\text{utility}(s, p)$ (or payoff) that defines the final numeric value for a game that ends in $s$ for a player $p$.
    - E.g., $1$, $0$ or $\frac{1}{2}$ if the outcome is win, loss or draw.
- Together, the initial state, the $\text{actions}(s)$ function, the $\text{result}(s, a)$ function and the terminal test define the **game tree**.
    - *Nodes* are game states.
    - *Edges* are actions.


## Assumptions

- We assume *deterministic*, *turn-taking*, *two-player* **zero-sum games** of *perfect information*.
- We will call our two players MAX and MIN. MAX moves first.

---

# Game tree

.width-100[![](figures/lec3/tictactoe.png)]

---

# Zero-sum games

- In a **zero-sum** game, the total payoff to all players is *constant* for all games.
    - E.g., $0+1$, $1+0$ or $\frac{1}{2} + \frac{1}{2}$.
- For two-player games, agents share the **same utility** function, but one wants to *maximize* it while the other wants to *minimize* it.
    - MAX maximizes the game's $\text{utility}$ function.
    - MIN minimizes the game's $\text{utility}$ function.
- *Strict competition*.
    - If one wins, the other loses, and vice-versa.

.center.width-50[![](figures/lec3/zero-sum-cartoon.png)]

.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

---

# Adversarial search

.grid[
.col-2-3[
- In a search problem, the optimal solution is a sequence of actions leading to a goal state.
    - i.e. a terminal state where MAX wins.
- In a game, the opponent (MIN) may react *arbitrarily* to a move.
- Therefore, a player (MAX) must define a contingent **strategy** which specifies
    - its moves in the initial state,
    - its moves in the states resulting from every possible response by MIN,
    - its moves in the states resulting from every possible response by MIN in those states,
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

The **minimax value** $\text{minimax}(s)$ is the largest achievable payoff (for MAX) from state $s$, assuming an optimal adversary (MIN).

.center.width-100[![](figures/lec3/minimax.png)]

The **optimal** next move (for MAX) is to take the action that maximizes the minimax value in the resulting state.
- Assuming that MIN is an optimal adversary maximizes the *worst-case outcome* for MAX.
- This is equivalent to not making an assumption about the strength of the opponent.

---

# Minimax example

.width-100[![](figures/lec3/minimax-example.png)]

---

# Properties of Minimax

- *Completeness*:
    - Yes, if tree is finite.
- *Optimal*:
    - Yes, if MIN is an optimal opponent.
    - What if MIN is suboptimal?
        - Show that MAX will do even better.
    - What if MIN is suboptimal and predictable?
        - Other strategies might do better than Minimax. However they will do worse on an optimal opponent.

---

# Minimax efficiency

- Assume $\text{minimax}(s)$ is implemented using its recursive definition.
- How *efficient* is minimax?
    - Time complexity: $O(b^m)$.
    - Space complexity:
        - $O(bm)$, if all actions are generated at once, or
        - $O(m)$, if actions are generated one at a time.
- Example: for chess, $b \approx 35$, $m \approx 100$.
    - Time complexity: $O(35^{100}) = O(10^{154})$
    - Finding the exact solution is **intractable**!

<span class="Q">[Q]</span> Do we need to explore the whole game tree?

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
