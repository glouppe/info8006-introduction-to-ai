class: middle, center, title-slide

# Introduction to Artificial Intelligence

Lecture 5: Representing uncertain knowledge

<br><br>
Prof. Gilles Louppe<br>
[g.louppe@uliege.be](mailto:g.louppe@uliege.be)

???

R: move stuff from inference in bn
R: move stuff from learning on parameter estimation (map, mle)

---

# Today

.grid[
.kol-2-5[

- Bayesian networks
- Semantics
- Construction
- Parameter estimation (XXX)
- Inference (XXX)
- Independence

]
.kol-3-5[
.center.width-100[![](figures/lec5/bn-cartoon.png)]
]
]

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

# Representing uncertain knowledge

---

class: middle

## Representing knowledge

- The joint probability distribution can answer any question about the domain.
- However, its representation can become **intractably large** as the number of variable grows.
- *Independence* and *conditional independence* reduce the number of probabilities that need to be specified in order to define the full joint distribution.
- These relationships can be represented explicitly in the form of a **Bayesian network**.

---

# Bayesian networks

A **Bayesian network** is a *directed acyclic graph* (DAG) in which:
- Each *node* corresponds to a *random variable*.
    - Can be observed or unobserved.
    - Can be discrete or continuous.
- Each *edge* indicates dependency relationships.
    - If there is an arrow from node $X$ to node $Y$, $X$ is said to be a *parent* of $Y$.
- Each node $X_i$ is annotated with a **conditional probability distribution** ${\bf P}(X_i | \text{parents}(X_i))$ that quantifies the effect of the parents on the node.

???

In the simplest case, conditional distributions are represented as conditional probability tables (CTPs).

---

class: middle

.center.width-40[![](figures/lec5/alarm.png)]

## Example 1

I am at work, neighbor John calls to say my alarm is ringing, but neighbor
Mary does not call. Sometimes it's set off by minor earthquakes.
Is there a burglar?

- Variables: $\text{Burglar}$, $\text{Earthquake}$, $\text{Alarm}$, $\text{JohnCalls}$, $\text{MaryCalls}$.
- Network topology from "causal" knowledge:
    - A burglar can set the alarm off
    - An earthquake can set the alaram off
    - The alarm can cause Mary to call
    - The alarm can cause John to call

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

.center.width-90[![](figures/lec5/burglary2.svg)]

???

Blackboard: example of calculation, as in the next slide.

---

# Semantics

A Bayesian network implicitly **encodes** the full joint distribution as the product of the local distributions:

$$P(x\_1, ..., x\_n) = \prod\_{i=1}^n P(x_i | \text{parents}(X_i))$$

## Example

$$
\begin{aligned}
P(j, m, a, \lnot b, \lnot e) &= P(j|a) P(m|a)P(a|\lnot b,\lnot e)P(\lnot b)P(\lnot e)\\\\
&= 0.9 \times 0.7 \times 0.001 \times 0.999 \times 0.998 \\\\
&\approx 0.00063
\end{aligned}
$$

---

class: middle

Why does $\prod\_{i=1}^n P(x_i | \text{parents}(X_i))$ result in the proper joint probability?
- By the *chain rule*, $P(x\_1, ..., x\_n) = \prod\_{i=1}^n P(x\_i | x\_1, ..., x\_{i-1})$.
- Provided that we assume **conditional independence** of $X\_i$ with its predecessors in the ordering given the parents, and provided $\text{parents}(X\_i) \subseteq \\{ X\_1, ..., X\_{i-1}\\}$:
$$P(x\_i | x\_1, ..., x\_{i-1}) = P(x\_i | \text{parents}(X_i))$$
- Therefore $P(x\_1, ..., x\_n) = \prod\_{i=1}^n P(x_i | \text{parents}(X_i))$.

---

class: middle

.grid[
.kol-1-2[.width-90[![](figures/lec5/tooth.png)]]
.kol-1-2[.width-100[![](figures/lec5/dentist-network.svg)]]
]
<br>

## Example 2

The topology of the network encodes conditional independence assertions:
- $\text{Weather}$ is independent of the other variables.
- $\text{Toothache}$ and $\text{Catch}$ are conditionally independent given $\text{Cavity}$.

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

???

Insist it does *not* encode dependencies!

---

class: middle

.grid.center[
.kol-1-3[.width-80[![](figures/lec5/traffic1.png)]]
.kol-2-3[.width-90[![](figures/lec5/traffic2.png)]<br><br>]
]

## Example 3

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

.grid.center[
.kol-1-5[.width-60[![](figures/lec5/traffic1-bn.png)]]
.kol-2-5[
${\bf P}(R)$

| $R$ | $P$ |
| --- | --- | --- |
| $\text{r}$ | $0.25$ |
| $\lnot\text{r}$ | $0.75$ |
]
.kol-2-5[
${\bf P}(T|R)$

| $R$ | $T$ | $P$ |
| --- | --- | --- |
| $\text{r}$ | $\text{t}$ | $0.75$ |
| $\text{r}$ | $\lnot\text{t}$ | $0.25$ |
| $\lnot\text{r}$ | $\text{t}$ | $0.5$ |
| $\lnot\text{r}$ | $\lnot\text{t}$ | $0.5$ |
]
]

???

Causal model

---

class: middle

.center.width-60[![](figures/lec5/traffic3.png)]

## Example 3 (bis)

.grid.center[
.kol-1-5[.width-60[![](figures/lec5/traffic2-bn.png)]]
.kol-2-5[
${\bf P}(T)$

| $T$ | $P$ |
| --- | --- | --- |
| $\text{t}$ | $9/16$ |
| $\lnot\text{t}$ | $7/16$ |
]
.kol-2-5[
${\bf P}(R|T)$

| $T$ | $R$ | $P$ |
| --- | --- | --- |
| $\text{t}$ | $\text{r}$ | $1/3$ |
| $\text{t}$ | $\lnot\text{r}$ | $2/3$ |
| $\lnot\text{t}$ | $\text{r}$ | $1/7$ |
| $\lnot\text{t}$ | $\lnot\text{r}$ | $6/7$ |
]
]

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

???

Diagnostic model

---

# Construction

Bayesian networks are correct representations of the domain only if each node is conditionally independent of its other predecessors in the node ordering, given its parents.

## Construction algorithm

1. Choose some **ordering** of the variables $X\_1, ..., X\_n$.
2. For $i=1$ to $n$:
    1. Add $X\_i$ to the network.
    2. Select a minimal set of parents from $X\_1, ..., X\_{i-1}$ such that $P(x\_i | x\_1, ..., x\_{i-1}) = P(x\_i | \text{parents}(X_i))$.
    3. For each parent, insert a link from the parent to $X\_i$.
    4. Write down the CPT.

---

class: middle

.center.width-100[
![](figures/lec5/burglary-mess.svg)
]

.exercise[Do these networks represent the same distribution?]

???

For the left network:

- P (J|M ) = P (J)? No
- P (A|J, M ) = P (A|J)? P (A|J, M ) = P (A)? No
- P (B|A, J, M ) = P (B|A)? Yes
- P (B|A, J, M ) = P (B)? No
- P (E|B, A, J, M ) = P (E|A)? No
- P (E|B, A, J, M ) = P (E|A, B)? Yes

---

class: middle

## Compactness

- A CPT for boolean $X_i$ with $k$ boolean parents has $2^k$ rows for the combinations of parent values.
- Each row requires one number $p$ for $X_i = \text{true}$.
    - The number for $X_i=\text{false}$ is just $1-p$.
- If each variable has no more than $k$ parents, the complete network requires $O(n \times 2^k)$ numbers.
    - i.e., grows **linearly with $n$**, vs. $O(2^n)$ for the full joint distribution.
- For the burglary net, we need $1+1+4+2+2=10$ numbers (vs. $2^5-1=31$).
- Compactness depends on the *node ordering*.

---

# Independence

Important question: Are two nodes independent given certain evidence?
- If yes, this can be proved using algebra (tedious).
- If no, this can be proved with a counter example.

<br>

.center.width-45[![](figures/lec5/xyz.png)]

.center[Example: Are $X$ and $Z$ necessarily independent?]

---

class: middle

## Cascades

.grid[
.kol-1-2[
Is $X$ independent of $Z$? No.

Counter-example:
- Low pressure causes rain causes traffic, high pressure causes no rain causes no traffic.
- In numbers:
    - $P(y|x)=1$,
    - $P(z|y)=1$,
    - $P(\lnot y|\lnot x)=1$,
    - $P(\lnot z|\lnot y)=1$
]
.kol-1-2.center[.width-100[![](figures/lec5/cascade.png)]

$X$: low pressure,
$Y$: rain,
$Z$: traffic.

$P(x,y,z)=P(x)P(y|x)P(z|y)$]
]

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

.grid[
.kol-1-2[
Is $X$ independent of $Z$, given $Y$? Yes.

$$\begin{aligned}
P(z|x,y) &= \frac{P(x,y,z)}{P(x,y)} \\\\
&= \frac{P(x)P(y|x)P(z|y)}{P(x)P(y|x)} \\\\
&= P(z|y)
\end{aligned}$$

We say that the evidence along the cascade **"blocks"** the influence.

]
.kol-1-2.center[.width-100[![](figures/lec5/cascade.png)]

$X$: low pressure,
$Y$: rain,
$Z$: traffic.

$P(x,y,z)=P(x)P(y|x)P(z|y)$]
]

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

.grid[
.kol-1-2[
## Common parent

Is $X$ independent of $Z$? No.

Counter-example:
- Project due causes both forums busy and lab full.
- In numbers:
    - $P(x|y)=1$,
    - $P(\lnot x|\lnot y)=1$,
    - $P(z|y)=1$,
    - $P(\lnot z|\lnot y)=1$
]
.kol-1-2.center[.width-80[![](figures/lec5/common-parent.png)]

$X$: forum busy,
$Y$: project due,
$Z$: lab full.

$P(x,y,z)=P(y)P(x|y)P(z|y)$]
]

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

.grid[
.kol-1-2[
Is $X$ independent of $Z$, given $Y$? Yes

$$\begin{aligned}
P(z|x,y) &= \frac{P(x,y,z)}{P(x,y)} \\\\
&= \frac{P(y)P(x|y)P(z|y)}{P(y)P(x|y)} \\\\
&= P(z|y)
\end{aligned}$$

Observing the parent blocks the influence between the children.
]
.kol-1-2.center[.width-80[![](figures/lec5/common-parent.png)]

$X$: forum busy,
$Y$: project due,
$Z$: lab full.

$P(x,y,z)=P(y)P(x|y)P(z|y)$]
]

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

.grid[
.kol-1-2[
## v-structures

Are $X$ and $Y$ independent? Yes.
- The ballgame and the rain cause traffic, but they are not correlated.
- (Prove it!)

Are $X$ and $Y$ independent given $Z$? No!
- Seeing traffic puts the rain and the ballgame in competition as explanation.
- This is **backwards** from the previous cases. Observing a child node *activates* influence between parents.
]
.kol-1-2.center[.width-80[![](figures/lec5/v-structure.png)]

$X$: rain,
$Y$: ballgame,
$Z$: traffic.

$P(x,y,z)=P(x)P(y)P(z|x,y)$]
]

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]


---

class: middle

## d-separation

Let us assume a complete Bayesian network.
Are $X\_i$ and $X\_j$ conditionally independent given evidence $Z\_1=z\_1, ..., Z\_m=z\_m$?

Consider all (undirected) paths from $X\_i$ to $X\_j$:
- If one or more active path, then independence is not guaranteed.
- Otherwise (i.e., all paths are inactive), then independence is guaranteed.


---

class: middle

.grid[
.kol-2-3[

A path is **active** if each triple along the path is active:
- Cascade $A \to B \to C$ where $B$ is unobserved (either direction).
- Common parent $A \leftarrow B \rightarrow C$ where $B$ is unobserved.
- v-structure $A \rightarrow B \leftarrow C$ where $B$ or one of its descendents is observed.

]
.kol-1-3.width-100[![](figures/lec5/active-inactive.png)]
]

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

.grid[
.kol-1-2[
## Example

- $L \perp T' | T$?
- $L \perp B$?
- $L \perp B|T$?
- $L \perp B|T'$?
- $L \perp B|T, R$?

]
.kol-1-2.width-80.center[![](figures/lec5/example-d.png)]
]

???

- Yes
- Yes
- (maybe)
- (maybe)
- Yes

---

exclude: true
class: middle

## Local semantics

.center.width-60[![](figures/lec5/nondescendants.svg)]

A node $X$ is conditionally independent to its non-descendants (the $Z_{ij}$) given its parents (the $U_i$).

---

exclude: true
class: middle

## Global semantics

.center.width-60[![](figures/lec5/markov-blanket.svg)]

A node $X$ is conditionally independent of all other nodes in the network given its Markov blanket.

---

# Causality?

- When the network reflects the true causal patterns:
    - Often more compact (nodes have fewer parents).
    - Often easier to think about.
    - Often easier to elicit from experts.
- But, Bayesian networks **need not be causal**.
    - Sometimes no causal network exists over the domain (e.g., if variables are missing).
    - Edges reflect **correlation**, not causation.
- What do the edges really mean then?
    - Topology *may* happen to encode causal structure.
    - **Topology really encodes conditional independence.**

.center.width-50[![](figures/lec5/causality.png)]

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

.grid[
.kol-3-4[<br>
- Correlation does not imply causation.
- Causes cannot be expressed in the language of probability theory.
]
.kol-1-4[.circle.width-100[![](figures/lec5/pearl.jpg)].center[Judea Pearl]]
]

---

class: middle

Philosophers have tried to define causation in terms of probability: $X=x$ causes $Y=y$ if $X=x$ raises the probability of $Y=y$.

However, the inequality
$$P(y|x) > P(y)$$
fails to capture the intuition behind "probability raising", which is fundamentally a causal concept connoting a causal influence of $X=x$ over $Y=y$.

???

- Instead, the expression means that if we observe $X=x$, then the probability of $Y=y$ increases.
- But this increase may come about for other reasons!

---

class: middle

The correct formulation should read
$$P(y|\text{do}(X=x)) > P(y),$$
where $\text{do}(X=x)$ stands for an external intervention where $X$ is **set to** the value $x$ instead of being observed.

---

class: middle

## Observing vs. intervening

- The reading in barometer is useful to predict rain.
$$P(\text{rain}|\text{Barometer}=\text{high}) > P(\text{rain}|\text{Barometer}=\text{low})$$
- But hacking a barometer will not cause rain!
$$P(\text{rain}|\text{Barometer hacked to high}) = P(\text{rain}|\text{Barometer hacked to low})$$

---

# Summary

- Uncertainty arises because of laziness and ignorance. It is **inescapable** in complex non-deterministic or partially observable environments.
- Probabilistic reasoning provides a framework for managing our knowledge and *beliefs*, with the Bayes' rule acting as the workhorse for inference.
- A **Bayesian Network** specifies a full joint distribution. They are often exponentially smaller than an explicitly enumerated joint distribution.
- The structure of a Bayesian network encodes conditional independence assumptions between random variables.


---

class: end-slide, center
count: false

The end.
