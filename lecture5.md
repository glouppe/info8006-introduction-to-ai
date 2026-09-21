class: middle, center, title-slide

# Introduction to Artificial Intelligence

Lecture 5: Probabilistic reasoning

<br><br>
Prof. Gilles Louppe<br>
[g.louppe@uliege.be](mailto:g.louppe@uliege.be)

---

# Today

- Bayesian networks
    - Semantics
    - Construction
    - Independence relations
- Inference
- Parameter learning

.center.width-65[![](figures/lec5/bn-cartoon.png)]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

# Representing uncertain knowledge

---

class: middle

The explicit representation of the joint probability distribution grows exponentially with the number of variables.

.bold[Independence] and .bold[conditional independence] assumptions reduce the number of probabilities that need to be specified. They can be represented explicitly in the form of a .bold[Bayesian network].

---

# Bayesian networks

.grid[
.kol-3-4[

A Bayesian network is a .bold[directed acyclic graph] where
- each .bold[node] corresponds to a random variable;
    - observed or unobserved
    - discrete or continuous
- each .bold[edge] is directed and indicates a direct probabilistic dependency between two variables;
- each node $X_i$ is annotated with a .bold[conditional probability distribution] $$\mathbf{P}(X_i \mid \text{parents}(X_i))$$ that defines the distribution of $X_i$ given its parents in the network.

]
.kol-1-4.width-100[![](figures/lec5/example-d.png)]
]

???

In the simplest case, conditional distributions are represented as conditional probability tables (CPTs).

---

class: middle

.center.width-40[![](figures/lec5/alarm.png)]

## Example 1

- Variables: $\text{Burglar}$, $\text{Earthquake}$, $\text{Alarm}$, $\text{JohnCalls}$, $\text{MaryCalls}$.
- The network topology can be defined from domain knowledge:
    - A burglar can set the alarm off
    - An earthquake can set the alarm off
    - The alarm can cause Mary to call
    - The alarm can cause John to call

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

???

I am at work, neighbor John calls to say my alarm is ringing, but neighbor
Mary does not call. Sometimes it's set off by minor earthquakes.
Is there a burglar?

---

class: middle

.center.width-90[![](figures/lec5/burglary2.svg)]

???

Blackboard: example of calculation, as in the next slide.

---

# Semantics

A Bayesian network implicitly encodes the full joint distribution as a product of local distributions, that is

$$P(x\_1, ..., x\_n) = \prod\_{i=1}^n P(x_i \mid \text{parents}(X_i)).$$

Proof:
- By the chain rule, $P(x\_1, ..., x\_n) = \prod\_{i=1}^n P(x\_i \mid x\_1, ..., x\_{i-1})$.
- Provided that we assume conditional independence of $X\_i$ with its predecessors in the ordering given the parents, and provided $\text{parents}(X\_i) \subseteq \\{ X\_1, ..., X\_{i-1}\\}$, we have
$$P(x\_i \mid x\_1, ..., x\_{i-1}) = P(x\_i \mid \text{parents}(X_i)).$$
- Therefore, $P(x\_1, ..., x\_n) = \prod\_{i=1}^n P(x_i \mid \text{parents}(X_i))$.

---

class: middle

## Example 1 (continued)

$$
\begin{aligned}
P(j, m, a, \lnot b, \lnot e) &= P(j \mid a) P(m \mid a)P(a \mid \lnot b,\lnot e)P(\lnot b)P(\lnot e)\\\\
&= 0.9 \times 0.7 \times 0.001 \times 0.999 \times 0.998 \\\\
&\approx 0.00063
\end{aligned}
$$

---

class: middle

## Example 2

.grid[
.kol-1-2[.width-90[![](figures/lec5/tooth.png)]]
.kol-1-2[.width-100[![](figures/lec5/dentist-network.svg)]]
]

The dentist's scenario can be modeled as a Bayesian network with four variables, as shown on the right.

By construction, the topology of the network encodes conditional independence assertions. Each variable is independent of its non-descendants given its parents:
- $\text{Weather}$ is independent of the other variables.
- $\text{Toothache}$ and $\text{Catch}$ are conditionally independent given $\text{Cavity}$.

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

???

Setup:
- Weather: sunny (s) or rainy (r)
- Cavity: cavity (c) or no cavity (¬c)
- Toothache: toothache (t) or no toothache (¬t)
- Catch: catch (h) or no catch (¬h) with dental probe

Assumptions:
- the weather is independent of the other variables (hence the absence of edges from Weather to other nodes);
- toothache and catch are conditionally independent given cavity (hence the absence of edges between Toothache and Catch).

---

class: middle

.grid.center[
.kol-1-3[.width-70[![](figures/lec5/traffic1.png)]]
.kol-2-3[.width-80[![](figures/lec5/traffic2.png)]<br><br>]
]

## Example 3

Edges may correspond to causal relations.

.grid.center[
.kol-1-5[.width-60[![](figures/lec5/traffic1-bn.png)]]
.kol-2-5[
$\mathbf{P}(R)$

| $R$ | $P$ |
| --- | --- |
| $\text{r}$ | $0.25$ |
| $\lnot\text{r}$ | $0.75$ |
]
.kol-2-5[
$\mathbf{P}(T \mid R)$

| $R$ | $T$ | $P$ |
| --- | --- | --- |
| $\text{r}$ | $\text{t}$ | $0.75$ |
| $\text{r}$ | $\lnot\text{t}$ | $0.25$ |
| $\lnot\text{r}$ | $\text{t}$ | $0.5$ |
| $\lnot\text{r}$ | $\lnot\text{t}$ | $0.5$ |
]
]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

???

Causal model: rain causes traffic and the Bayesian network represents this causal relationship.

---

class: middle

.center.width-60[![](figures/lec5/traffic3.png)]

## Example 3 (bis)

... but edges need not be causal!

.grid.center[
.kol-1-5[.width-60[![](figures/lec5/traffic2-bn.png)]]
.kol-2-5[
$\mathbf{P}(T)$

| $T$ | $P$ |
| --- | --- |
| $\text{t}$ | $9/16$ |
| $\lnot\text{t}$ | $7/16$ |
]
.kol-2-5[
$\mathbf{P}(R \mid T)$

| $T$ | $R$ | $P$ |
| --- | --- | --- |
| $\text{t}$ | $\text{r}$ | $1/3$ |
| $\text{t}$ | $\lnot\text{r}$ | $2/3$ |
| $\lnot\text{t}$ | $\text{r}$ | $1/7$ |
| $\lnot\text{t}$ | $\lnot\text{r}$ | $6/7$ |
]
]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

???

Diagnostic model: traffic correlates with rain and the Bayesian network represents this correlation. The edge does not represent a causal relationship.

---

# Construction

Bayesian networks can be constructed in any order, provided that the conditional independence assertions are respected.

## Algorithm

1. Choose some .bold[ordering] of the variables $X\_1, ..., X\_n$.
2. For $i=1$ to $n$:
    1. Add $X\_i$ to the network.
    2. Select a minimal set of parents from $X\_1, ..., X\_{i-1}$ such that $P(x\_i \mid x\_1, ..., x\_{i-1}) = P(x\_i \mid \text{parents}(X_i))$.
    3. For each parent, insert a link from the parent to $X\_i$.
    4. Write down the CPT.

---

class: middle

.center.width-100[
![](figures/lec5/burglary-mess.svg)
]

.question[Do these networks represent the same distribution? Are they as compact?]

???

For the left network:

- P (J|M ) = P (J)? No
- P (A|J, M ) = P (A|J)? P (A|J, M ) = P (A)? No
- P (B|A, J, M ) = P (B|A)? Yes
- P (B|A, J, M ) = P (B)? No
- P (E|B, A, J, M ) = P (E|A)? No
- P (E|B, A, J, M ) = P (E|A, B)? Yes

---

# Independence relations

Since the topology of a Bayesian network encodes conditional independence assertions, it can be used to answer questions about the independence of variables given some evidence.

<br><br><br>

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
    - $P(y \mid x)=1$,
    - $P(z \mid y)=1$,
    - $P(\lnot y \mid \lnot x)=1$,
    - $P(\lnot z \mid \lnot y)=1$
]
.kol-1-2.center[.width-100[![](figures/lec5/cascade.png)]

$X$: low pressure,
$Y$: rain,
$Z$: traffic.

$P(x,y,z)=P(x)P(y \mid x)P(z \mid y)$]
]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

.grid[
.kol-1-2[
Is $X$ independent of $Z$, given $Y$? Yes.

$$\begin{aligned}
P(z \mid x,y) &= \frac{P(x,y,z)}{P(x,y)} \\\\
&= \frac{P(x)P(y \mid x)P(z \mid y)}{P(x)P(y \mid x)} \\\\
&= P(z \mid y)
\end{aligned}$$

We say that the evidence along the cascade .bold[blocks] the influence.

]
.kol-1-2.center[.width-100[![](figures/lec5/cascade.png)]

$X$: low pressure,
$Y$: rain,
$Z$: traffic.

$P(x,y,z)=P(x)P(y \mid x)P(z \mid y)$]
]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

.grid[
.kol-1-2[
## Common parent

Is $X$ independent of $Z$? No.

Counter-example:
- Project due causes both forums busy and lab full.
- In numbers:
    - $P(x \mid y)=1$,
    - $P(\lnot x \mid \lnot y)=1$,
    - $P(z \mid y)=1$,
    - $P(\lnot z \mid \lnot y)=1$
]
.kol-1-2.center[.width-80[![](figures/lec5/common-parent.png)]

$X$: forum busy,
$Y$: project due,
$Z$: lab full.

$P(x,y,z)=P(y)P(x \mid y)P(z \mid y)$]
]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

.grid[
.kol-1-2[
Is $X$ independent of $Z$, given $Y$? Yes

$$\begin{aligned}
P(z \mid x,y) &= \frac{P(x,y,z)}{P(x,y)} \\\\
&= \frac{P(y)P(x \mid y)P(z \mid y)}{P(y)P(x \mid y)} \\\\
&= P(z \mid y)
\end{aligned}$$

Observing the parent blocks the influence between the children.
]
.kol-1-2.center[.width-80[![](figures/lec5/common-parent.png)]

$X$: forum busy,
$Y$: project due,
$Z$: lab full.

$P(x,y,z)=P(y)P(x \mid y)P(z \mid y)$]
]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

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
- This is .bold[backwards] from the previous cases. Observing a child node .bold[activates] influence between parents.
]
.kol-1-2.center[.width-80[![](figures/lec5/v-structure.png)]

$X$: rain,
$Y$: ballgame,
$Z$: traffic.

$P(x,y,z)=P(x)P(y)P(z \mid x,y)$]
]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

???

Proof:

$$P(x,y,z) = P(x)P(y)P(z \mid x,y)$$

and

$$P(x,y,z) = P(x,y)P(z \mid x,y)$$

therefore

$$P(x,y) = P(x)P(y)$$

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

A path is .bold[active] if each triple along the path is active:
- Cascade $A \to B \to C$ where $B$ is unobserved (either direction).
- Common parent $A \leftarrow B \rightarrow C$ where $B$ is unobserved.
- v-structure $A \rightarrow B \leftarrow C$ where $B$ or one of its descendants is observed.

]
.kol-1-3.width-100[![](figures/lec5/active-inactive.png)]
]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

.grid[
.kol-1-2[
## Example

- $L \perp T' \mid T$?
- $L \perp B$?
- $L \perp B \mid T$?
- $L \perp B \mid T'$?
- $L \perp B \mid T, R$?

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

class: middle

# Inference

---

class: middle

Inference is concerned with the problem of .bold[computing a marginal and/or a conditional probability distribution] from a joint probability distribution:

.grid[
.kol-1-3.center[Simple queries:]
.kol-2-3[$\mathbf{P}(X\_i \mid e)$]
]
.grid[
.kol-1-3.center[Conjunctive queries:]
.kol-2-3[$\mathbf{P}(X\_i,X\_j \mid e)=\mathbf{P}(X\_i \mid e)\mathbf{P}(X\_j \mid X\_i,e)$]
]
.grid[
.kol-1-3.center[Most likely explanation:]
.kol-2-3[$\arg \max_q P(q \mid e)$]
]
.grid[
.kol-1-3.center[Optimal decisions:]
.kol-2-3[$\arg \max\\\_a \mathbb{E}\_{p(s' \mid s,a)} \left[ V(s') \right]$]
]

.center.width-30[![](figures/lec5/query-cartoon.png)]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

???

Explain what $\arg \max$ means.

Insist on the importance of inference. Inference <=> reasoning.

---

# Inference by enumeration

Start from the joint distribution $\mathbf{P}(Q, E\_1, ..., E\_k, H\_1, ..., H\_r)$.

1. Select the entries consistent with the evidence  $E_1, ..., E_k = e_1, ..., e_k$.
2. Marginalize out the hidden variables to obtain the joint of the query and the evidence variables:
$$\mathbf{P}(Q,e\_1,...,e\_k) = \sum\_{h\_1, ..., h\_r} \mathbf{P}(Q, h\_1, ..., h\_r, e\_1, ..., e\_k).$$
3. Normalize:
<br>
$$\begin{aligned}
Z &= \sum_q P(q,e_1,...,e_k) \\\\
\mathbf{P}(Q \mid e_1, ..., e_k) &= \frac{1}{Z} \mathbf{P}(Q,e_1,...,e_k)
\end{aligned}$$

---

class: middle

.width-25.center[![](figures/lec5/bn-alarm.svg)]

Consider the alarm network and the query $\mathbf{P}(B \mid j,m)$. We have
$$\begin{aligned}
\mathbf{P}(B \mid j,m) &= \frac{1}{Z} \sum\_e \sum\_a \mathbf{P}(B,j,m,e,a) \\\\
&\propto \sum\_e \sum\_a \mathbf{P}(B,j,m,e,a).
\end{aligned}$$
Using the Bayesian network, the full joint entries can be rewritten as the product of CPT entries 
$$\begin{aligned}
\mathbf{P}(B \mid j,m) &\propto \sum\_e \sum\_a \mathbf{P}(B)P(e)\mathbf{P}(a \mid B,e)P(j \mid a)P(m \mid a).
\end{aligned}$$

???

&\propto P(B) \sum\_e P(e) \sum\_a P(a|B,e)P(j|a)P(m|a)

---

class: middle

.center.width-80[![](figures/lec5/enumeration.png)]

Inference by enumeration is slow because the whole joint distribution is joined up before summing out the hidden variables.

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

Factors that do not depend on the variables in the summations can be factored out, which means that marginalization does not necessarily have to be done at the end, hence saving some computations.

For the alarm network, we have
$$\begin{aligned}
\mathbf{P}(B \mid j,m) &\propto \sum\_e \sum\_a \mathbf{P}(B)P(e)\mathbf{P}(a \mid B,e)P(j \mid a)P(m \mid a) \\\\
&= \mathbf{P}(B) \sum\_e P(e) \sum\_a \mathbf{P}(a \mid B,e)P(j \mid a)P(m \mid a).
\end{aligned}$$

---

class: middle

.center.width-100[![](figures/lec5/inference-enumeration.png)]

Same complexity as DFS: $O(n)$ in space, $O(d^n)$ in time.

???

- $n$ is the number of variables.
- $d$ is the size of their domain.

Note that this assumes that variables are enumerated in topological order.

---

class: middle

## Evaluation tree for $P(b \mid j,m)$

.center.width-80[![](figures/lec5/enumeration-tree.png)]

Despite the factorization, inference by enumeration is still .bold[inefficient]. There are repeated computations!
- e.g., $P(j \mid a)P(m \mid a)$ is computed twice, once for $e$ and once for $\lnot e$.
- These can be avoided by storing .bold[intermediate results].

???

Inefficient because the product is evaluated left-to-right, in a DFS manner.

---

# Inference by variable elimination

The .bold[Variable Elimination] algorithm carries out summations right-to-left and stores intermediate factors to avoid recomputations.
The algorithm interleaves:
- Joining sub-tables
- Eliminating hidden variables

<br>
.center.width-80[![](figures/lec5/elimination.png)]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

## Variable Elimination

Query: $\mathbf{P}(Q \mid e\_1, ..., e\_k)$.

1. Start with the initial factors (the local CPTs, instantiated by the evidence).
2. While there are still hidden variables:
    1. Pick a hidden variable $H$
    2. Join all factors mentioning $H$
    3. Eliminate H
3. Join all remaining factors
4. Normalize

---

class: middle

## Factors

- Each .bold[factor] $\mathbf{f}_i$ is a multi-dimensional array indexed by the values of its argument variables. E.g.:
.grid[
.kol-1-2[
$$
\begin{aligned}
\mathbf{f}\_4 &= \mathbf{f}\_4(A) = \left(\begin{matrix}
P(j \mid a) \\\\
P(j \mid \lnot a) \end{matrix}\right)
= \left(\begin{matrix}
0.90 \\\\
0.05 \end{matrix}\right) \\\\
\mathbf{f}\_4(a) &= 0.90 \\\\
\mathbf{f}\_4(\lnot a) &= 0.05
\end{aligned}$$
]
]
- Factors are initialized with the CPTs annotating the nodes of the Bayesian network, conditioned on the evidence.

---

class: middle

## Join

The .bold[pointwise product] $\times$, or .bold[join], of two factors $\mathbf{f}_1$ and $\mathbf{f}_2$ yields a new factor $\mathbf{f}\_3$.
- Exactly like a .bold[database join]!
- The variables of $\mathbf{f}\_3$ are the .bold[union] of the variables in $\mathbf{f}_1$ and $\mathbf{f}_2$.
- The elements of $\mathbf{f}\_3$ are given by the product of the corresponding elements in $\mathbf{f}_1$ and $\mathbf{f}_2$.

.center.width-100[![](figures/lec5/ve-product.png)]

---

class: middle

## Elimination

.bold[Summing out], or .bold[eliminating], a variable from a factor is done by adding up the sub-arrays formed by fixing the variable to each of its values in turn.

For example, to sum out $A$ from $\mathbf{f}\_3(A, B, C)$, we write:

$$\begin{aligned}
\mathbf{f}(B,C) &= \sum\_a \mathbf{f}\_3(a, B, C) = \mathbf{f}\_3(a, B, C) + \mathbf{f}\_3(\lnot a, B, C) \\\\
&= \left(\begin{matrix}
0.06 & 0.24 \\\\
0.42 & 0.28
\end{matrix}\right) + \left(\begin{matrix}
0.18 & 0.72 \\\\
0.06 & 0.04
\end{matrix}\right) = \left(\begin{matrix}
0.24 & 0.96 \\\\
0.48 & 0.32
\end{matrix}\right)
\end{aligned}$$

---

class: middle

.center.width-35[![](figures/lec5/bn-alarm.svg)]

<br>

.question[Run the variable elimination algorithm for the query $\mathbf{P}(B \mid j,m)$.]

---

class: middle


## Relevance

Consider the query $\mathbf{P}(J \mid b)$:
$$\mathbf{P}(J \mid b) \propto P(b) \sum_e P(e) \sum\_a P(a \mid b,e) \mathbf{P}(J \mid a) \sum\_m P(m \mid a)$$
- $\sum_m P(m \mid a) = 1$, therefore $M$ is .bold[irrelevant] for the query.
- In other words, $\mathbf{P}(J \mid b)$ remains unchanged if we remove $M$ from the network.

.italic[Theorem.] $H$ is irrelevant for $\mathbf{P}(Q \mid e)$ unless $H \in \text{ancestors}(\\{Q\\} \cup E)$.

---

class: middle

## Complexity

.center.width-50[![](figures/lec5/ve-ordering.png)]

Consider the query $\mathbf{P}(X\_n \mid y\_1,...,y\_n)$.

Work through the two elimination orderings:
- $Z, X\_1, ..., X\_{n-1}$
- $X\_1, ..., X\_{n-1}, Z$

What is the size of the maximum factor generated for each of the orderings?
- Answer: $2^{n+1}$ vs. $2^2$ (assuming boolean values)

---

class: middle

The computational and space complexity of variable elimination is determined by the largest factor.
- The elimination .bold[ordering] can greatly affect the size of the largest factor.
- The optimal ordering is .bold[NP-hard] to find. There is no known polynomial-time algorithm to find it.

---

# Approximate inference

Exact inference is .bold[intractable] for most probabilistic models of practical interest.
(e.g., involving many variables, continuous and discrete, undirected cycles, etc).

We must resort to .bold[approximate] inference algorithms:
- Sampling methods: produce answers by repeatedly generating random numbers from a distribution of interest.
- Variational methods: formulate inference as an optimization problem.
- Belief propagation methods: formulate inference as a message-passing algorithm.
- Machine learning methods: learn an approximation of the target distribution from training examples.

---

class: middle

# Parameter learning

---

class: middle

When modeling a domain, we can choose a probabilistic model specified as a Bayesian network. However, specifying the individual probability values is often difficult. 

A workaround is to use a .bold[parameterized] family $\mathbf{P}(X \mid \theta)$ (sometimes also noted $\mathbf{P}\_\theta(X)$) of models, and .bold[estimate] the parameters $\theta$ from data.

???

Connect back to the Kolmogorov axioms: we have upgraded $P$ to a family of distributions $P_\theta$.

---

class: middle

.center.width-100[![](figures/lec5/parameterized-bn.png)]

???

Use the box of chalks example:

Assume a Bernoulli distribution of parameter $\theta$ for the binary variable denoting the color of a chalk:
- Red chalk with probability $1-\theta$.
- White chalk with probability $\theta$.
We draw $N$ chalks i.i.d. and observe $c$ white chalks and $l=N-c$ red chalks. How to estimate $\theta$?

---

# Maximum likelihood estimation

Suppose we have a set of $N$ i.i.d. observations $\mathbf{d} = \\{x\_1, ..., x\_N\\}$.

The .bold[likelihood] of the parameters $\theta$ is the probability of the data given the parameters
$$P(\mathbf{d} \mid \theta) = \prod\_{j=1}^N P(x\_j \mid \theta).$$

The .bold[maximum likelihood estimate] (MLE) $\theta^\*$  of the parameters is the value of $\theta$ that maximizes the likelihood
$$\theta^\* = \arg \max\_\theta P(\mathbf{d} \mid \theta).$$

---

class: middle

When possible analytically,
1. Write down the log-likelihood $L(\theta) = \log P(\mathbf{d} \mid \theta)$ of the parameters $\theta$.
2. Write down the derivative $\frac{\partial L}{\partial \theta}$ of the log-likelihood of the parameters $\theta$.
3. Find the parameter values $\theta^\*$ such that the derivatives are zero (and check whether the Hessian is negative definite).

???

Note that:
- evaluating the likelihood may require summing over hidden variables, i.e., inference.
- finding $\theta^\*$ may be hard; modern optimization techniques help.

---

class: middle

## Case (a)

What is the fraction $\theta$ of cherry candies?

Suppose we unwrap $N$ candies, and get $c$ cherries and $l=N-c$ limes.
These are i.i.d. observations, therefore
$$P(\mathbf{d} \mid \theta) = \prod\_{j=1}^N P(x\_j \mid \theta) = \theta^c (1-\theta)^l.$$
Maximize this w.r.t. $\theta$, which is easier for the log-likelihood and leads to
$$\begin{aligned}
L(\mathbf{d} \mid \theta) &= \log P(\mathbf{d} \mid \theta) = c \log \theta + l \log(1-\theta) \\\\
\frac{\partial L(\mathbf{d} \mid \theta)}{\partial \theta} &= \frac{c}{\theta} - \frac{l}{1-\theta}=0.
\end{aligned}$$
Hence $\theta=\frac{c}{N}$.

---

class: middle

## Case (b)

Red and green wrappers depend probabilistically on flavor.
E.g., the likelihood for a cherry candy in green wrapper is
$$\begin{aligned}
&P(\text{cherry}, \text{green} \mid \theta,\theta\_1, \theta\_2) \\\\
&= P(\text{cherry} \mid \theta,\theta\_1, \theta\_2) P(\text{green} \mid \text{cherry}, \theta,\theta\_1, \theta\_2) \\\\
&= \theta (1-\theta\_1).
\end{aligned}$$

The likelihood for the parameters, given $N$ candies, $r\_c$ red-wrapped cherries, $g\_c$ green-wrapped cherries, etc., is
$$\begin{aligned}
P(\mathbf{d} \mid \theta,\theta\_1, \theta\_2) =&\,\, \theta^c (1-\theta)^l \theta\_1^{r\_c}(1-\theta\_1)^{g\_c} \theta\_2^{r\_l} (1-\theta\_2)^{g\_l} \\\\
L =&\,\, c \log \theta + l \log(1-\theta)  +  \\\\
   &\,\, r\_c \log \theta\_1 + g\_c \log(1-\theta\_1) + \\\\
   &\,\, r\_l \log \theta\_2 + g\_l \log(1-\theta\_2).
\end{aligned}$$

---

class: middle

The derivatives of $L$ yield 
$$\begin{aligned}
\frac{\partial L}{\partial \theta} &= \frac{c}{\theta} - \frac{l}{1-\theta} = 0 \Rightarrow \theta = \frac{c}{c+l} \\\\
\frac{\partial L}{\partial \theta\_1} &= \frac{r\_c}{\theta\_1} - \frac{g\_c}{1-\theta\_1} = 0 \Rightarrow \theta\_1 = \frac{r\_c}{r\_c + g\_c} \\\\
\frac{\partial L}{\partial \theta\_2} &= \frac{r\_l}{\theta\_2} - \frac{g\_l}{1-\theta\_2} = 0 \Rightarrow \theta\_2 = \frac{r\_l}{r\_l + g\_l}.
\end{aligned}$$

???

Again, results coincide with intuition.

---

class: middle

.question[In case (a), if we unwrap 1 candy and get 1 cherry, what is the MLE? How confident are we in this estimate?]

- With small datasets, maximum likelihood estimation can lead to overfitting. 
- The MLE does not provide a measure of uncertainty about the parameters.

---

# Bayesian parameter learning

We can treat parameter learning as a .bold[Bayesian inference] problem:
- Make the parameters $\theta$ random variables and treat them as hidden variables.
- Specify a .bold[prior] distribution $\mathbf{P}(\theta)$ over the parameters.
- Then, as data arrives, update our beliefs about the parameters to obtain the .bold[posterior] distribution $\mathbf{P}(\theta \mid \mathbf{d})$.

.question[How should the network of case (a) be updated?]

---

class: middle

## Case (a)

What is the fraction $\theta$ of cherry candies?

We assume a Beta prior $$P(\theta) = \text{Beta}(\theta \mid a,b) = \frac{1}{Z} \theta^{a-1} (1-\theta)^{b-1}$$
where $Z$ is a normalization constant. 

Then, observing a cherry candy yields the posterior
$$\begin{aligned}
P(\theta \mid \text{cherry}) &\propto P(\text{cherry} \mid \theta) P(\theta) \\\\
&= \theta \text{Beta}(\theta \mid a,b) \\\\
&= \theta \theta^{a-1} (1-\theta)^{b-1} \\\\
&= \theta^a (1-\theta)^{b-1} \\\\
&= \text{Beta}(\theta \mid a+1,b).
\end{aligned}$$

???

Intuition: a Beta prior encodes a belief on the fraction of cherry candies. Observing a cherry candy increases this, observing a lime candy decreases it.

---

class: middle

## Case (b)

.center.width-100[![](figures/lec5/caseb-bayesian.png)]

---

class: middle

## Maximum a posteriori estimation

When the posterior cannot be computed analytically, we can use .bold[maximum a posteriori] (MAP) estimation, which consists in approximating the posterior with the point estimate $\theta^\*$ that maximizes the posterior distribution, i.e.,
$$\theta^\* = \arg \max\_\theta P(\theta \mid \mathbf{d}) = \arg \max\_\theta P(\mathbf{d} \mid \theta) P(\theta).$$

---

class: middle, center

(Step-by-step code example)

---

# Summary

- A Bayesian network specifies a full joint distribution. Bayesian networks are often exponentially smaller than an explicitly enumerated joint distribution.
- The topology of a Bayesian network encodes conditional independence assumptions between random variables.
- Inference is the problem of computing a marginal and/or a conditional probability distribution from a joint probability distribution.
    - Exact inference is possible for simple Bayesian networks, but is intractable for most probabilistic models of practical interest.
    - Approximate inference algorithms are used in practice.
- Parameters of a Bayesian network can be learned from data using maximum likelihood estimation or Bayesian inference.

---

class: end-slide, center
count: false

The end.
