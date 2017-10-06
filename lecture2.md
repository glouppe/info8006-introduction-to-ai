class: middle, center, title-slide

# Introduction to Artificial Intelligence

Lecture 2: Solving problems by searching

---

# Today

- Agents that plan ahead
- Search problems
- Uninformed search methods
    - Depth-first search
    - Breadth-first search
    - Uniform-cost search
- Informed search methods
    - A*
    - Heuristics

---

# Reflex agents

Reflex agents:
- Select actions on the basis of the current percept.
- May have a model of the world current state.
- Do not consider the future consequences of their actions.
- Consider only **how the world is now**.

<span class="Q">[Q]</span> Can a reflex agent be rational?

.grid[
.col-1-2[
![](figures/lec2/pacman-reflex.png)
]
.col-1-2[
![](figures/lec2/pacman-reflex2.png)
]
]

---

# Problem-solving agents

Assumptions:
- *Observable*, *deterministic* (and *known*) environment.

Problem-solving agents:
- Take decisions based on (hypothesized) consequences of actions.
- Must have a model of how the world evolves in response to actions.
- Formulate a goal.
- Consider **how to world would be**.

.grid[
.col-1-2[
![](figures/lec2/pacman-goal.png)
]
.col-1-2[
![](figures/lec2/pacman-goal2.png)
]
]

---

.stretch[![](figures/lec2/problem-solving-agent.png)]

Notes:
- This is *offline* problem solving. The solution is executed "eyes closed", ignoring the percepts.
- *Online* problem solving involves acting without complete knowledge.

---

# Search problems

A **search problem** consists of the following components:
- The *initial state* of the agent.
- A description of the *actions* available to the agent given a state $s$, denoted $\text{actions}(s)$.
- A *transition model* that returns the state $s' = \text{result}(s, a)$ that results from doing action $a$ in state $s$.
    - We say that $s'$ is a *successor* of $s$ if there is an acceptable action from $s$ to $s'$.

.center[![](figures/lec2/pacman-successor.png)]

---

- Together, the initial state, the actions and the transition model define the *state space* of the problem, i.e. the set of all states reachable from the initial state by any sequence of action.
    - The state space forms a directed graph in which the nodes are states and links between nodes are actions.
    - A path is a sequence of states connected by actions.

.center[![](figures/lec2/pacman-space.png)]

- A *goal test* which determines whether the solution of the problem is achieved in state $s$.
- A *path cost* that assigns a numeric value to each path.
  - We may also assume that the path cost corresponds to a sum of positive *step costs* $c(s,a,s')$  associated to the action $a$ in $s$ leading to $s'$.

---

A **solution** to a problem is an action sequence that leads from the initial state to a goal state.
- A solution quality is measured by the path cost function.
- An *optimal solution* has the lowest path cost
among all solutions.

<span class="Q">[Q]</span> What if the environment is partially observable? non-deterministic?

---

# Search problems are models

.stretch[![](figures/lec2/search-problems-models.png)]

.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

---

# Example: Traveling in Romania

.center[![](figures/lec2/romania.png)]

- Initial state = the city we start in.
    - $s_0 = \text{in}(\text{Arad})$
- Actions = Going from the current city to the cities that are directly connected to it.
    - $\text{actions}(s_0) = \\{ \text{go}(\text{Sibiu}), \text{go}(\text{Timisoara}), \text{go}(\text{Zerind}) \\}$

---

- Transition model = The city we arrive in after driving to it.
    - $\text{result}(\text{in}(Arad), \text{go}(Zerind)) = \text{in}(Zerind)$
- Goal test: whether we are in Bucharest.
    - $s \in \\{ \text{in}(\text{Bucharest}) \\}$
- Step cost: distances between cities.

---

# Selecting a state space

- Real world is absurdly complex.
    - The *world state* includes every last detail of the environment.
    - State space must be abstracted for problem solving.
- A *search state* keeps only the details needed for planning.
    - Example: eat-all-dots
        - States: $\\{ (x, y), \text{dot booleans}\\}$
        - Actions: NSEW
        - Transition: update location and possibly a dot boolean
        - Goal test: dots all false

.stretch[![](figures/lec2/pacman-world.png)]

---

# State space size

.grid[
.col-1-2[
- *World state*:
    - Agent positions: 120
    - Found count: 30
    - Ghost positions: 12
    - Agent facing: NSEW
- *How many?*
    - World states?
        - $120 \times 2^{30} \times 12^2 \times 4$
    - States for eat-all-dots?
        - $120 \times 2^{30}$
]
.col-1-2[
![](figures/lec2/pacman-size.png)
]
]

---

# Search trees

The set of possible acceptable sequences starting at the initial state form a **search tree**:
- Nodes correspond to states in the state space, where the initial state is the root node.
- Branches correspond to applicable actions.
    - Child nodes correspond to successors.
- **For most problems, we can never actually build the whole tree**.

.center[![](figures/lec2/pacman-tree.png)]

---

# Tree search algorithms

.stretch[![](figures/lec2/tree-search.png)]

Important ideas:
- *Fringe* (or *frontier*) of partial plans under consideration
- *Expansion*
- *Exploration*

<span class="Q">[Q]</span> Which fringe nodes to explore? How to expand as few nodes as possible, while achieving the goal?

---

# Tree search example

.center[![](figures/lec2/search-map.png)]

---

# Uninformed search strategies

**Uninformed** search strategies use only the information available in the problem definition.

- Depth-first search
- Breadth-first search
- Uniform-cost search
- Iterative deepening

---

# Depth-first search

.stretch[![](figures/lec2/dfs-cartoon.png)]

.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

---

# Depth-first search

- *Strategy*: expand the deepest node in the fringe.
- *Implementation*: fringe is a **LIFO stack**.

.center[![](figures/lec2/dfs-progress.png)]

---

class: smaller

# Properties of search strategies

- A strategy is defined by picking the **order of expansion**.
- Strategies are evaluated along the following dimensions:
    - *Completeness*: does it always find a solution if one exists?
    - *Optimality*: does it always find the least-cost solution?
    - *Time complexity*: how long does it take to find a solution?
    - *Space complexity*: how much memory is needed to perform the search?
- Time and complexity are measured in terms of
    - $b$: maximum branching factor of the search tree
    - $d$: depth of the least-cost solution
    - $m$: maximum length of any path in the state space (may be $\infty$)

<span class="Q">[Q]</span> Number of nodes in a tree?

.center.width-50[![](figures/lec2/search-properties.png)]

---

class: smaller

# Properties of DFS

- *Completeness*:
    - $m$ could be infinite, so only if we prevent cycles.
- *Optimality*:
    - No, DFS finds the leftmost solution, regardless of depth or cost.
- *Time complexity*:
    - May generate the whole tree (or a good part of it, regardless of $d$).
      Therefore $O(b^m)$, which might much greater than the size of the state space!
- *Space complexity*:
    - Only store siblings on path to root, therefore $O(bm)$.

.center.width-50[![](figures/lec2/dfs-properties.png)]

---

# Breadth-first search

.stretch[![](figures/lec2/bfs-cartoon.png)]

.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

---

# Breadth-first search

- *Strategy*: expand the shallowest node in the fringe.
- *Implementation*: fringe is a **FIFO queue**.

.center[![](figures/lec2/bfs-progress.png)]

---

class: smaller

# Properties of BFS

- *Completeness*:
    - If the shallowest goal node is at some finite depth $d$, BFS will eventually find it after generating all shallower nodes (provided $b$ is finite).
- *Optimality*:
    - The shallowest goal is not necessarily the optimal one.
    - BFS is optimal only if the path cost is a non-decreasing function of the depth of the node.
- *Time complexity*:
    - If the solution is a depth $d$, then the total number of nodes generated before finding this node is $b+b^2+b^3+...+b^d = O(b^d)$
- *Space complexity*:
    - The number of nodes to maintain in memory is the size of the fringe, which will be the largest at the last tier. That is $O(b^d)$

.center.width-50[![](figures/lec2/bfs-properties.png)]

---

# Uniform-cost search

.stretch[![](figures/lec2/ucs-cartoon.png)]

.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

---

# Uniform-cost search

- *Strategy*: expand the cheapest node in the fringe.
- *Implementation*: fringe is a **priority queue**, using the cumulative cost $g(n)$ as priority.

---

class: smaller

# Properties of UCS

- *Completeness*:
    - Yes, if step cost $\geq \epsilon > 0$.
- *Optimality*:
    - Yes, sinces UCS expands nodes in order of their optimal path cost.
- *Time complexity*:
     - Assume $C^\*$ is the cost of the optimal solution and that step costs are all $\geq \epsilon$.
     - The "effective depth" is then roughly $C^\*/\epsilon$.
     - The worst-case time complexity is $O(b^{C^\*/\epsilon})$.
- *Space complexity*:
     - The number of nodes to maintain is the size of the fringe, so as many as in the last tier $O(b^{C^\*/\epsilon})$.

.center.width-40[![](figures/lec2/ucs-properties.png)]

---

# Iterative deepening

- Idea: get DFS's space advantages with BFS's time/shallow solution advantages.
    - Run DFS with depth limit 1.
    - If no solution, run DFS with depth limit 2.
    - If no solution, run DFS with depth limit 3.
    - ...


.grid[
.col-2-3[
<span class="Q">[Q]</span> What are the properties of iterative deepening?

<span class="Q">[Q]</span> Isn't this process wastefully redundant?
]
.col-1-4[
![](figures/lec2/id-properties.png)
]
]

---

# Redundant paths

The failure to detect **repeated states** can turn a linear problem into an exponential one!

.stretch[![](figures/lec2/redundant.png)]

---

# Graph search

Redundant paths and cycles can be avoided by **keeping track** of the states that have been *explored*.
This amounts to grow a tree directly on the state-space graph.

.stretch[![](figures/lec2/graph-search.png)]

<span class="Q">[Q]</span> What are the properties of DFS/GFS based on graph search?

---

# Informed search strategies

- Greedy search
- A*

---

# Heuristic functions

- learning heuristic from experience

---

# Summary

---

# References
