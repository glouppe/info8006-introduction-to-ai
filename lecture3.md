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
    - Unlikely to find goal with standard search algorithms, we need to *approximate*.

---

# Types of games

- **Deterministic** or *stochastic*?
- **Perfect** or *imperfect* information?
- **One**, *two or more* players?


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
- Together, the initial state, the $\text{actions}(s)$ function and the $\text{result}(s, a)$ function define the **game tree**.
    - *Nodes* are game states.
    - *Edges* are actions.


## Assumptions

- We assume *deterministic*, *turn-taking*, *two-player* **zero-sum games** of *perfect information*.
- We will call our two players **MAX** and *MIN*. **MAX** moves first.

.center.width-50[![](figures/lec3/tictactoe-cartoon.png)]

.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

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

.center.width-40[![](figures/lec3/zero-sum-cartoon.png)]

.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

---

# Adversarial search

.grid[
.col-2-3[
- In a search problem, the optimal solution is a sequence of actions leading to a goal state.
    - i.e., a terminal state where MAX wins.
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
- *Optimality*:
    - Yes, if MIN is an optimal opponent.
    - What if MIN is suboptimal?
        - Show that MAX will do even better.
    - What if MIN is suboptimal and predictable?
        - Other strategies might do better than Minimax. However they will do worse on an optimal opponent.

---

# Minimax efficiency

- Assume $\text{minimax}(s)$ is implemented using its recursive definition.
- How *efficient* is minimax?
    - Time complexity: same as DFS, i.e., $O(b^m)$.
    - Space complexity:
        - $O(bm)$, if all actions are generated at once, or
        - $O(m)$, if actions are generated one at a time.

<span class="Q">[Q]</span> Do we need to explore the whole game tree?

---

# Pruning

.center.width-80[![](figures/lec3/minimax-incomplete-tree.png)]

.width-100[![](figures/lec3/minimax-incomplete-formula.png)]

Therefore, it is possible to compute the **correct** minimax decision *without looking at every node* in the tree.

---

# Pruning

.center.width-80[![](figures/lec3/minimax-incomplete-stepbystep.png)]

---

class: smaller

# $\alpha$-$\beta$  pruning

We want to compute $v = \text{minimax}(n)$ (for MIN).
- We loop over $n$'s children.
- The minimax values are being computed one at a time and $v$ is updated iteratively.
- Let $\alpha$ be the best value that MAX can get, at any choice point along the current path from root.
- If $v$ becomes lower than $\alpha$, then **MAX will avoid it**.
- Therefore, we can *stop iterating* over the remaining $n$'s other children.

.center.width-30[![](figures/lec3/alpha-beta.png)]

---

# $\alpha$-$\beta$  search

.width-90[![](figures/lec3/alpha-beta-impl.png)]

---

# Properties of $\alpha$-$\beta$ search

- Pruning has **no effect** on the minimax values. Therefore, *completeness* and *optimality* are preserved from Minimax.
- *Time complexity*:
    - The effectiveness depends on the order in which the states are examined.
    - If states could be examined in *perfect order*, then $\alpha-\beta$ search examines only $O(b^{m/2})$ nodes to pick the best move, vs. $O(b^m)$ for minimax.
        - $\alpha-\beta$ can solve a tree twice as deep as minimax can in the same amount of time.
        - Equivalent to have an effective branching factor $\sqrt{b}$.
- *Space complexity*: $O(m)$, as for Minimax.

---

# Game tree size

.center.width-30[![](figures/lec3/chess.jpg)]

Chess:
- $b \approx 35$ (approximate average branching factor)
- $d \approx 100$ (depth of a game tree for typical games)
- $b^d \approx 35^{100} \approx 10^{154}$.
- For $\alpha-\beta$ search and perfect ordering, we get $b^{d/2} \approx 35^{50} = 10^{77}$.

Finding the exact solution is completely **infeasible**.

---

# Imperfect real-time decisions

- Under *time constraints*, searching for the exact solution is not feasible in most realistic games.
- Solution: cut the search earlier.
    - Replace the $\text{utility}(s)$ function with a heuristic **evaluation function** $\text{eval}(s)$ that estimates the state utility.
    - Replace the terminal test by a **cutoff test** that decides when to stop expanding a state.

.center.width-100[![](figures/lec3/hminimax.png)]

<span class="Q">[Q]</span> Can $\alpha-\beta$ search  be adapted to implement H-Minimax?

---

# Evaluation functions

- An evaluation function returns an **estimate** of the expected utility of the game from a given position.
- The computation *must be short* (that is the whole point to search faster).
- Ideally, the evaluation should *order* states in the same way as in Minimax.
- In non-terminal states, the evaluation function should be strongly *correlated with the actual chances of winning*.
- Like for heuristics in search, evaluation functions can be  *learned* using machine learning algorithms.

---

# Quiescence

.center.width-70[![](figures/lec3/chess-eval.png)]

- These states only differ in the position of the rook at lower right.
- However, Black has advantage in (a), but not in (b).
- If the search stops in (b), Black will not see that White's next move is to capture its Queen, gaining advantage.
- A sophisticated cutoff test should favor positions that are **quiescent**.
    - i.e., states that are unlikely to exhibit wild swings in value in the near future.


---

# The horizon effect

- Evaluations functions are **always imperfect**.
- Often, the deeper in the tree the evaluation function is buried, the less the quality of the evaluation function matters.

---

.center[
<video controls>
  <source src="figures/lec3/depth2.mp4" type="video/mp4">
</video>

Cutoff at depth 2, evaluation larger as Pacman is closer to the dot.]

.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

---

.center[
<video controls>
  <source src="figures/lec3/depth10.mp4" type="video/mp4">
</video>

Cutoff at depth 10, evaluation larger as Pacman is closer to the dot.]

.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

---

# Stochastic games

expectimax
videos

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
