class: middle, center, title-slide

# Introduction to Artificial Intelligence

Lecture 3: Constraint satisfaction problems

???

R: Have an additional lecture before this one, on MDPs?

---

# Today

- *Constraint satisfaction problems*:
    - Exploiting the representation of a state to accelerate search.
    - Backtracking.
    - Generic heuristics.
- *Logical agents*
    - Propositional logic for reasoning about the world.
    - ... and its connection with CSPs.

.center.width-50[![](figures/lec4/map-cartoon.png)]

.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

---

class: middle, center

# Constraint satisfaction problems

---

# Motivation

- In *standard search problems*:
    - States are evaluated by domain-specific heuristics.
    - States are tested by a domain-specific function to determine if the goal is achieved.
    - From the point of view of the search algorithms however, **states are atomic**.
        - A state is a black box.
- Instead, if states have *a factored representation*, then the structure of states can be exploited to improve the *efficiency of the search*.
- **Constraint satisfaction problem** algorithms *take advantage of this structure* and use *general-purpose* heuristics to solve complex problems.
    - CSPs are specialized to a family of search sub-problems.
- Main idea: eliminate large portions of the search space all at once, by identifying combinations of variable/value that violate constraints.

---

# Constraint satisfaction problems

Formally, a **constraint satisfaction problem** (CSP) consists of three components $X$, $D$ and $C$:

- $X$ is a set of *variables*, $\\{X_1, ..., X_n\\}$,
- $D$ is a set of *domains*, $\\{D_1, ..., D_n\\}$, one for each variable,
- $C$ is a set of *constraints* that specify  allowable combinations of values.

---

# Example: Map coloring

.center.width-80[![](figures/lec4/map-coloring.png)]

---

# Example: Map coloring

.center.width-30[![](figures/lec4/map-coloring.png)]

- Variables: $X = \\{ WA, NT, Q, NSW, V, SA, T \\}$
- Domains: $D_i = \\{ red, green, blue \\}$ for each variable.
- Constraints: $C = \\{ SA \neq WA, SA \neq NT, SA\neq Q, ... \\}$
    - Implicit: $WA \neq NT$
    - Explicit: $(WA, NT) \in \\{ \\{red, green\\}, \\{red, blue\\}, ... \\}$
- Solutions are **assignments** of values to the variables such that constraints are all satisfied.
    - e.g., $\\{ WA=red, NT=green, Q=red, SA=blue,$ $\quad\quad NSW=green, V=red, T=green \\}$

---

# Constraint graph

.center.width-50[![](figures/lec4/csp-graph.png)]

- *Nodes* = variables of the problems
- *Edges* = constraints in the problem involving the variables associated to the end nodes.
- General purpose CSP algorithms **use the graph structure** to speedup search.
    - e.g., Tasmania is an independent subproblem.

---

# Example: Cryptarithmetic

.center.width-60[![](figures/lec4/cryptarithmetic.png)]

- Variables: $\\{ T, W, O, F, U, R, C_1, C_2, C_3\\}$
- Domains: $D_i = \\{ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 \\}$
- Constraints:
    - $\text{alldiff}(T, W, O, F, U, R)$
    - $O+O=R+10\times C_1$
    - $C_1 + W + W = U + 10\times C_2$
    - ...

---

# Example: Sudoku

.center.width-30[![](figures/lec4/sudoku.png)]

- Variables: each (open) square
- Domains: $D_i = \\{ 1, 2, 3, 4, 5, 6, 7, 8, 9 \\}$
- Constraints:
    - 9-way $\text{alldiff}$ for each column
    - 9-way $\text{alldiff}$ for each row
    - 9-way $\text{alldiff}$ for each region
---

# Example: The Waltz algorithm

.center.width-40[![](figures/lec4/waltz.png)]

The Waltz algorithm is a procedure for interpreting 2D line drawings of solid polyhedra as 3D objects. Early example of an AI computation posed as a CSP.

.pull-right.width-70[![](figures/lec4/waltz-inter.png)]
CSP formulation:
- Each intersection is a variable.
- Adjacent intersections impose constraints on each other.
- Solutions are physically realizable 3D objects.


.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

---

# Variations on the CSP formalism

- *Discrete variables*
    - Finite domains
        - Size $d$ means $O(d^n)$ complete assignments.
        - e.g., boolean CSPs, including the SAT boolean satisfiability problem (NP-complete).
    - Infinite domains
        - e.g., job scheduling, variables are start/end days for for each job.
        - need a constraint language, e.g. $start_1 + 5 \leq start_2$.
        - Solvable for linear constraints, undecidable otherwise.
- *Continuous variables*
    - e.g., precise start/end times of experiments.
    - Linear constraints solvable in polynomial time by LP methods.

---

# Variations on the CSP formalism

- *Varieties of constraints*:
    - Unary constraint involve a single variable.
        - Equivalent to reducing the domain, e.g. $SA \neq green$.
    - Binary constraints involve pairs of variables, e.g. $SA \neq WA$.
    - Higher-order constraints involve 3 or more variables.
- *Preferences* (*soft constraints*)
    - e.g., red is better than green.
    - Often representable by a cost for each variable assignment.
    - Results in constraint optimization problems.
    - (We will ignore those for now.)

---

# Real-world examples

.grid[
.col-1-2[
- Assignment problems
    - e.g., who teaches what class
- Timetabling problems
    - e.g., which class is offered when and where?
- Hardware configuration
- Spreadsheets
- Transportation scheduling
- Factory scheduling
- Circuit layout
- ... and many more
]
.col-1-2[
![](figures/lec4/assignments.png)
]
]

Notice that many real-world problems involve real-valued variables.


.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

---

class: middle, center

# Solving CSPs

---

# Standard search formulation

- CSPs can be cast as standard search problems.
    - For which we have solvers, including DFS, BFS or A*.
- States are partial assignments:
    - The *initial state* is the empty assignment $\\{ \\}$.
    - *Actions*: assign a value to an unassigned variable.
    - *Goal test*: the current assignment is complete and satisfies all constraints.
- This algorithm is the same for all CSPs!

---

# Search methods

.center.width-50[![](figures/lec4/csp-graph.png)]

- What would BFS or DFS do? What problems does naive search have?
- For $n$ variables of domain size $d$, $b=(n-l)d$ at depth $l$.
    - We generate a tree with $n!d^n$ leaves even if there are only $d^n$ possible assignments!

???

Simulate the execution on blackboard. Highlight two issues:
- commutativity
- constraints are checked only at the end, by the goal function

---

# Backtracking search

- Backtracking search is the basic uninformed algorithm for solving CSPs.
- Idea 1: **One variable at a time**:
    - The naive application of search algorithms ignore a crucial property: variable assignments are *commutative*. Therefore, fix the ordering.
        - $WA=red$ then $NT=green$ is the same as $NT=green$ then $WA=red$.
    - One only needs to consider assignments to a single variable at each step.
        - $b=d$ and there are $d^n$ leaves.
- Idea 2: **Check constraints as you go**:
    - Consider only values which do not conflict with current partial assignment.
    - Incremental goal test.

---

# Backtracking example

.center.width-80[![](figures/lec4/backtracking-example.png)]

---

# Backtracking search

.center.width-100[![](figures/lec4/backtracking.png)]

- Backtracking = DFS + variable-ordering + fail-on-violation
- What are the choice points?

???

Choice points:
- Ordering the variables
- Ordering the values
- Filtering
- Structure

---

# Improving backtracking

- Can we improve backtracking using **general-purpose** ideas, without domain-specific knowledge?
- *Ordering*:
    - Which variable should be assigned next?
    - In what order should its values be tried?
- *Filtering*: can we detect inevitable failure early?
- *Structure*: can we exploit the problem structure?

---

# Variable ordering

- **Minimum remaining values**:
Choose the variable *with the fewest legal values left* in its domain.
- Also known as the *fail-first* heuristic.
    - Detecting failures quickly is equivalent to pruning large parts of the search tree.

.center.width-100[![](figures/lec4/ordering-mrv.png)]

---

# Value ordering

- **Least constraining value**: Given a choice of variable, choose the *least constraining value*.
- i.e., the value that rules out the fewest values in the remaining variables.

.center.width-100[![](figures/lec4/ordering-lcv.png)]

<span class="Q">[Q]</span> Why should variable selection be fail-first but value selection be fail-last?

???

We are seeking only one solution. Therefore:
- fail-first variable selection to prune large portions of the tree
- fail-fast value selection to look for the most likely value

---

# Filtering: Forward checking

- Keep *track of remaining legal values* for unassigned variables.
    - Whenever a variable $X$ is assigned, and for each unassigned variable $Y$ that is connected to $X$ by a constraint, delete from $Y$'s domain any value that is inconsistent.
- *Terminate search* when any variable has no legal value left.

.center.width-100[![](figures/lec4/forward-checking.png)]

---

# Filtering: Constraint propagation

Forward checking propagates information assigned to unassigned variables, but does not provide early deteciton for all failures:

.center.width-100[![](figures/lec4/forward-checking-inc.png)]

- $NT$ and $SA$ cannot both be blue!
- **Constraint propagation** repeatedly enforces constraints locally.

---

# Arc consistency

- An arc $X \to Y$ is **consistent** if and only if for every value $x$ in the domain of $X$ there is some value $y$ in the domain of $Y$ that satisfies the associated binary constraint.
- Forward checking $\Leftrightarrow$ enforcing consistency of arcs pointing to each new assignment.
- This principle can be generalized to enforce consistency for **all** arcs.

.center.width-100[![](figures/lec4/arc-consistency.png)]

---

# Arc consistency algorithm

.center.width-100[![](figures/lec4/ac3.png)]

<span class="Q">[Q]</span> When in backtracking shall this procedure be called?

???

- After applying AC3, either every arc is arc-consistent, or some variable has an empty domain, indicating that the CSP cannot be solved.
- This check should be inserted after a new assignment, before the recursive call. If an inconsistency is detected

---

# Structure (1)

.center.width-50[![](figures/lec4/csp-graph.png)]

- Tasmania and mainland are **independent subproblems**.
    - Any solution for the mainland combined with any solution for Tasmania yields a solution for the whole map.
- Independence can be ascertained by finding *connected components* of the constraint graph.

---

# Structure (2)

- Time complexity: Assume each subproblem has $c$ variables out of $n$ in total. Then $O(\frac{n}{c} d^c)$.
    - E.g., $n=80$, $d=2$, $c=20$.
    - $2^{80} =$  4 billion years at 10 million nodes/sec.
    - $4 \times 2^{20} =$ 0.4 seconds at 10 million nodes/sec.

---

# Tree-structured CSPs

.center.width-90[![](figures/lec4/tree-csp-trans.png)]

- Algorithm for tree-structured CSPs:
    - Order: choose a root variable, order variables so that parents precede children (topological sort).
    - Remove backward:
        - for $i=n$ down to $2$, enforce arc consistency of $parent(X_i) \to X_i$.
    - Assign forward:
        - for $i=1$ to $n$, assign $X_i$ consistently with its $parent(X_i)$.
- Time complexity: $O(n d^2)$
    - Compare to general CSPs, where worst-case time is $O(d^n)$.

???

Run the algorithm on the blackboard.

---

# Nearly tree-structured CSPs

- *Conditioning*:  instantiate a variable, prune its neighbors' domains.
- *Cutset conditioning*:
    - Assign (in all ways) a set $S$ of variables such that the remaining constraint graph is a tree.
    - Solve the residual CSPs (tree-structured).
    - If the residual CSP has a solution, return it together with the assignment for $S$.

.center.width-70[![](figures/lec4/cutset.png)]

---

class: middle, center

# Logical agents

---

# The Wumpus world

.center.width-70[![](figures/lec4/wumpus-world.png)]

---

class: smaller

# PEAS description

- *Performance measure*:
    - +1000 for climbing out of the cave with gold;
    - -1000 for falling into a pit or being eaten by the wumpus;
    - -1 per step.
- *Environment*:
    - $4 \times 4$ grid of rooms;
    - The agent starts in the lower left square labeled $[1,1]$, facing right;
    - Locations for gold, the wumpus and pits are chosen randomly from squares other than the start square.
- *Actuators*:
    - Forward, Turn left by $90$° or Turn right by $90$°.
- *Sensors*:
    - Squares adjacent to wumpus are *smelly*;
    - Squares adjacent to pit are *breezy*;
    - *Glitter* if gold is in the same square;
        - Gold is picked up by reflex, and cannot be dropped.
    - You *bump* if you walk into a wall.
    - The agent program receives the percept $[Stench, Breeze, Glitter, Bump]$.

---

# Wumpus world characterization

- *Deterministic*: Yes, outcomes are exactly specified.
- *Static*: Yes, Wumpus and pits dot not move.
- *Discrete*: Yes.
- *Single-agent*: Yes, Wumpus is essential a natural feature.
- **Fully observable**: No, only *local* perception.
- **Episodic**: No, what was observed before is very useful.

The agent need to maintain a model of the world and to update this model upon percepts.

We will use **logical reasoning** to overcome the initial ignorance of the agent.

---

# Exploring the Wumpus world (1)

.center.width-100[![](figures/lec4/wumpus-exploration1.png)]

(a) Percept = $[None, None, None, None]$

(b) Percept = $[None, Breeze, None, None]$

---

# Exploring the Wumpus world (2)

.center.width-100[![](figures/lec4/wumpus-exploration2.png)]

(a) Percept = $[Stench, None, None, None]$

(b) Percept = $[Stench, Breeze, Glitter, None]$

---

# Logical agents

- Most useful in non-episodic, partially observable environments.
- **Logic (knowledge-based) agents** combine:
    - A *knowledge base* ($KB$): a list of facts that are known to the agent.
    - Current *percepts*.
- Hidden aspects of the current state are **inferred** using rules of inference.
- **Logic** provides a good formal language for both   
    - Facts encoded as *axioms*.
    - Rules of *inference*.

.center.width-80[![](figures/lec4/kb-agent.png)]

---

# Propositional logic: Syntax

The **syntax** of propositional logic defines allowable *sentences*.

.center.width-80[![](figures/lec4/syntax.png)]

---

# Propositional logic: Semantics

- In propositional logic, a *model* is an assignment of  truth values for every proposition symbol.
    - E.g., if the sentences of the knowledge base make use of the symbols $P_1$, $P_2$ and $P_3$, then one possible model is $m=\\{ P_1=false, P_2=true, P_3=true\\}$.
- The **semantics** for propositional logic specifies how to (recursively) evaluate the *truth value* of any complex sentence, with respect to a model $m$, as follows:
    - The truth value of a proposition symbol is specified in $m$.
    - $\lnot P$ is true iff $P$ is false;
    - $P \wedge Q$ is true iff $P$ and $Q$ are true;
    - $P \lor Q$ is true iff either $P$ or $Q$ is true;
    - $P \Rightarrow Q$ is true unless $P$ is true and $Q$ is false;
    - $P \Leftrightarrow Q$ is true iff $P$ and $Q$ are both true of both false.


---

# Wumpus world sentences

.grid[
.col-2-3[
- Let $P_{i,j}$ be true if there is a pit in $[i,j]$.
- Let $B_{i,j}$ be true if there is a breeze in $[i,j]$.

Examples:
- There is not pit in $[1,1]$:
    - $R\\\_1: \lnot P\\\_{1,1}.$
- Pits cause breezes in adjacent squares:
    - $R\\\_2: B\\\_{1,1} \Leftrightarrow (P\\\_{1,2} \lor P\\\_{2,1}).$
    - $R\\\_3: B\\\_{2,1} \Leftrightarrow (P\\\_{1,1} \lor P\\\_{2,2} \lor P\\\_{3,1}).$
- Breeze percept for the first two squares:
    - $R\\\_4: \lnot B\\\_{1,1}.$
    - $R\\\_5: B\\\_{2,1}.$

]
.col-1-3[![](figures/lec4/wumpus-world.png)]
]

---

# Entailment

- We say a model $m$ *satisfies* a sentence $\alpha$ if $\alpha$ is true in $m$.
    - $M(\alpha)$ is the set of all models that satisfy $\alpha$.
- $\alpha \vDash \beta$ iff $M(\alpha) \subseteq M(\beta)$.
    - We say that the sentence $\alpha$ **entails** the sentence $\beta$.
    - $\beta$ is true in all models where $\alpha$ is true.
    - That is, $\beta$ *follows logically* from $\alpha$.

---

# Wumpus models (1)

.center.width-30[![](figures/lec4/wumpus-simple.png)]

- Let consider possible models for $KB$ assuming only pits and a reduced Wumpus world with only 5 squares and pits.
- Situation after:
    - detecting nothing in $[1,1]$,
    - moving right, breeze in $[2,1]$.

<span class="Q">[Q]</span> How many models are there?

???

3 binary variables $P\_{1,2}$, $P\_{2,2}$, $P\_{3,1}$, hence $2^3=8$ models.

---

# Wumpus models (2)

.center.width-60[![](figures/lec4/wumpus-kb.png)]

- All 8 possible models in the reduced Wumpus world.
- The knowledge base $KB$ contains all possible Wumpus worlds consistent with the observations and the physics of the  world.

---

# Entailments (1)

.center.width-60[![](figures/lec4/wumpus-entailment.png)]

- $\alpha_1$ = "$[1,2]$ is safe". Does $KB$ entails $\alpha_1$?
- $KB \vDash \alpha_1$ since $M(KB)  \subseteq M(\alpha_1)$.
    - This proof is called *model checking* because it *enumerates* all possible models to check whether $\alpha_1$ is true in all models where $KB$ is true.
- Entailment can be used to carry out **logical inference**.

---

# Entailments (2)

.center.width-60[![](figures/lec4/wumpus-noentailment.png)]

- $\alpha_2$ = "$[2,2]$ is safe". Does $KB$ entails $\alpha_2$?
- $KB \nvDash \alpha_2$ since $M(KB)  \nsubseteq M(\alpha_2)$.
- We **cannot** conclude whether $[2,2]$ is safe (it may or may not).

---

# Unsatisfiability theorem

$$\alpha \vDash \beta \text{ iff } (\alpha \wedge \lnot \beta) \text{ is unsatisfiable}$$

- $\alpha$ is unsatisfiable iff $M(\alpha) = \\{ \\}$.
    - i.e., there is no assignment of truth values such that $\alpha$ is true.
- Proving $\alpha \vDash \beta$ by checking the unsatisfiability of $\alpha \wedge \lnot \beta$ corresponds to the proof technique of reductio ad absurdum.
- Checking the satisfiability of a sentence $\alpha$ can be cast as CSP!
    - More efficient than enumerating all models.
    - But remains NP-complete.
    - See also SAT solvers, tailored for this specific problem.


---

# Summary

- Constraint satisfaction problems:
    - States are represented by a set of variable/value pairs.
    - Backtracking, a form of depth-first search, is commonly used for solving CSPs.
    - The complexity of solving a CSP is strongly related to the structure of its constraint graph.
- Logical agents:
    - Intelligent agents need knowledge about the world in order to reach good decisions.
    - Logical inference can be used as tool to reason about the world.
        - The inference problem can be cast as the problem of determining the unsatisfiability of a formula.
        - This in turn can be cast as a CSP.
