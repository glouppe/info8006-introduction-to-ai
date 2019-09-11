class: middle, center, title-slide

# Introduction to Artificial Intelligence

Lecture 6: Inference in Bayesian networks

<br><br>
Prof. Gilles Louppe<br>
[g.louppe@uliege.be](mailto:g.louppe@uliege.be)

???

R: draw the BN's with draw.io to have a consistent style.

---

# Today

.grid[
.kol-1-2[
- Exact inference
    - Inference by enumeration
    - Inference by variable elimination
- Continuous variables
- Approximate inference
    - Ancestral sampling
    - Rejection sampling
    - Likelihood weighting
    - Gibbs sampling
]
.kol-1-2[
<br><br>
.width-100[![](figures/lec6/bn-cartoon.png)]
]
]

.footnote[Image credits: [CS188](http://ai.berkeley.edu/lecture_slides.html), UC Berkeley.]

---

# Bayesian networks

.grid[
.kol-2-3[
A Bayesian network is a *directed acyclic graph* in which:
- Each node corresponds to a *random variable* $X\_i$.
- Each node $X\_i$ is annotated with a **conditional probability distribution** $P(X\_i | \text{parents}(X\_i))$ that quantifies the effect of the parents on the node.

A Bayesian network implicitly **encodes** the full joint distribution as the product of the local distributions:
    $$P(x\_1, ..., x\_n) = \prod\_{i=1}^n P(x_i | \text{parents}(X_i))$$
]
.kol-1-3.center[.width-100[![](figures/lec6/bn-cartoon2.png)]

<br>

.width-70[![](figures/lec6/bn-cartoon3.png)]]
]

.footnote[Image credits: [CS188](http://ai.berkeley.edu/lecture_slides.html), UC Berkeley.]

---

class: middle

.grid[
.kol-3-4[.center.width-100[![](figures/lec5/burglary2.svg)]]
.kol-1-4[.center.width-100[![](figures/lec5/alarm.png)]]
]

<br>
$$
\begin{aligned}
P(b,\lnot e, a, \lnot j, m) &= P(b)P(\lnot e)P(a|b, \lnot e)P(\lnot j|a)P(m, a) \\\\
&= 0.001 \times 0.998 \times 0.94 \times 0.1 \times 0.7
\end{aligned}$$

---

class: middle

# Exact inference

---

# Inference

Inference is concerned with the problem **computing a marginal and/or conditional probability** from a joint probability distribution:

.grid[
.kol-1-3.center[Simple queries:]
.kol-2-3[$P(X\_i|e)$]
]
.grid[
.kol-1-3.center[Conjunctive queries:]
.kol-2-3[$P(X\_i,X\_j|e)=P(X\_i|e)P(X\_j|X\_i,e)$]
]
.grid[
.kol-1-3.center[Most likely explanation:]
.kol-2-3[$\arg \max_q P(q|e)$]
]
.grid[
.kol-1-3.center[Optimal decisions:]
.kol-2-3[$\arg \max\\\_a \mathbb{E}\_{p(s'|s,a)} \left[ V(s') \right]$]
]

.center.width-30[![](figures/lec6/query-cartoon.png)]

.footnote[Image credits: [CS188](http://ai.berkeley.edu/lecture_slides.html), UC Berkeley.]

---

# Inference by enumeration

Start from the joint distribution $P(Q, E\_1, ..., E\_k, H\_1, ..., H\_r)$.

1. Select the entries consistent with the evidence  $E_1, ..., E_k = e_1, ..., e_k$.
2. Marginalize out the hidden variables to obtain the joint of the query and the evidence variables:
$$P(Q,e\_1,...,e\_k) = \sum\_{h\_1, ..., h\_r} P(Q, h\_1, ..., h\_r, e\_1, ..., e\_k).$$
3. Normalize:
<br>
$$\begin{aligned}
Z &= \sum_q P(q,e_1,...,e_k) \\\\
P(Q|e_1, ..., e_k) &= \frac{1}{Z} P(Q,e_1,...,e_k)
\end{aligned}$$

---

class: middle

.pull-right[![](figures/lec6/bn-burglar.png)]

Consider the alarm network and the query $P(B|j,m)$:<br><br>
$\begin{aligned}
P(B|j,m) &= \frac{1}{Z} \sum\_e \sum\_a P(B,j,m,e,a) \\\\
&\propto \sum\_e \sum\_a P(B,j,m,e,a)
\end{aligned}$

Using the Bayesian network, the full joint entries can be rewritten as the product of CPT entries:<br><br>
$\begin{aligned}
P(B|j,m) &\propto \sum\_e \sum\_a P(B)P(e)P(a|B,e)P(j|a)P(m|a)
\end{aligned}$

???

&\propto P(B) \sum\_e P(e) \sum\_a P(a|B,e)P(j|a)P(m|a)

---

class: middle

.center.width-80[![](figures/lec6/enumeration.png)]

Inference by enumeration is slow because the whole joint distribution is joined up before summing out the hidden variables.

.footnote[Image credits: [CS188](http://ai.berkeley.edu/lecture_slides.html), UC Berkeley.]

---

class: middle

Notice that factors that do not depend on the variables in the summations can be factored out, which means that marginalization does not necessarily have to be done at the end:

$$\begin{aligned}
P(B|j,m) &\propto \sum\_e \sum\_a P(B)P(e)P(a|B,e)P(j|a)P(m|a) \\\\
&= P(B) \sum\_e P(e) \sum\_a P(a|B,e)P(j|a)P(m|a)
\end{aligned}$$

---

class: middle

.center.width-100[![](figures/lec6/inference-enumeration.png)]

Same complexity as DFS: $O(n)$ in space, $O(d^n)$ in time.

---

class: middle

## Evaluation tree for $P(b|j,m)$

.center.width-80[![](figures/lec6/enumeration-tree.png)]

Enumeration is still **inefficient**: there are repeated computations!
- e.g., $P(j|a)P(m|a)$ is computed twice, once for $e$ and once for $\lnot e$.
- These can be avoided by *storing intermediate results*.

---

# Inference by variable elimination

The **variable elimination** (VE) algorithm carries out summations right-to-left and *stores intermediate results* (called **factors**) to avoid recomputations.
The algorithm interleaves:
- Joining sub-tables
- Eliminating hidden variables

.center.width-80[![](figures/lec6/elimination.png)]

.footnote[Image credits: [CS188](http://ai.berkeley.edu/lecture_slides.html), UC Berkeley.]

---

class: middle

.center.width-30[![](figures/lec6/bn-burglar.png)]

## Example

$$\begin{aligned}
P(B|j, m) &\propto P(B,j,m) \\\\
&= P(B) \sum\_e P(e) \sum\_a P(a|B,e)P(j|a)P(m|a) \\\\
&= \mathbf{f}\_1(B) \times \sum\_e \mathbf{f}\_2(e) \times \sum\_a \mathbf{f}\_3(a,B,e) \times \mathbf{f}\_4(a) \times \mathbf{f}\_5(a) \\\\
&= \mathbf{f}\_1(B) \times \sum\_e \mathbf{f}\_2(e) \times \mathbf{f}\_6(B,e) \quad\text{ (sum out } A\text{)} \\\\
&= \mathbf{f}\_1(B) \times \mathbf{f}\_7(B) \quad\text{ (sum out } E\text{)} \\\\
\end{aligned}$$

---

class: middle

## Factors

- Each **factor $\mathbf{f}_i$** is a multi-dimensional array indexed by the values of its argument variables. E.g.:
.grid[
.kol-1-2[
$$
\begin{aligned}
\mathbf{f}\_4 &= \mathbf{f}\_4(A) = \left(\begin{matrix}
P(j|a) \\\\
P(j|\lnot a) \end{matrix}\right)
= \left(\begin{matrix}
0.90 \\\\
0.05 \end{matrix}\right) \\\\
\mathbf{f}\_4(a) &= 0.90 \\\\
\mathbf{f}\_4(\lnot a) &= 0.5
\end{aligned}$$
]
]
- Factors are initialized with the CPTs annotating the nodes of the Bayesian network, conditioned on the evidence.

---

class: middle

## Join

The *pointwise product* $\times$, or **join**, of two factors $\mathbf{f}_1$ and $\mathbf{f}_2$ yields a new factor $\mathbf{f}\_3$.
- Exactly like a **database join**!
- The variables of $\mathbf{f}\_3$ are the *union* of the variables in $\mathbf{f}_1$ and $\mathbf{f}_2$.
- The elements of $\mathbf{f}\_3$ are given by the product of the corresponding elements in $\mathbf{f}_1$ and $\mathbf{f}_2$.

.center.width-100[![](figures/lec6/ve-product.png)]

---

class: middle

## Elimination

*Summing out*, or **eliminating**, a variable from a factor is done by adding up the submatrices formed by fixing the variable to each of its values in turn.

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

## General Variable Elimination algorithm

- Query: $P(Q|e\_1, ..., e\_k)$.
- Start with the initial factors.
    - The local CPTs, instantiated by the evidence.
- While there are still hidden variables:
    - Pick a hidden variable $H$
    - Join all factors mentioning $H$
    - Eliminate H
- Join all remaining factors
- Normalize

---

class: middle

## Example

(blackboard example)

???

Prepare this for $P(B|j,m)$.

---

# Relevance

Consider the query $P(J|b)$:
$$P(J|b) \propto P(b) \sum_e P(e) \sum\_a P(a|b,e) P(J|a) \sum\_m P(m|a)$$
- $\sum_m P(m|a) = 1$, therefore $M$ is **irrelevant** for the query.
- In other words, $P(J|b)$ remains unchanged if we remove $M$ from the network.

.pull-right[![](figures/lec6/bn-burglar.png)]
## Theorem

$H$ is irrelevant for $P(Q|e)$ unless $H \in \text{ancestors}(\\\{Q\\\} \cup E)$.

---

# Complexity

.center.width-50[![](figures/lec6/ve-ordering.png)]

Consider the query $P(X\_n|y\_1,...,y\_n)$.
Work through the two elimination orderings:
- $Z, X\_1, ..., X\_{n-1}$
- $X\_1, ..., X\_{n-1}, Z$

What is the size of the maximum factor generated for each of the orderings?
- Answer: $2^{n+1}$ vs. $2^2$ (assuming boolean values)

???

R: prepare that

---

class: middle

The computational and space complexity of variable elimination is determined by **the largest factor**.
- The elimination *ordering* can greatly affect the size of the largest factor.
- Does there always exist an ordering that only results in small factors? **No!**
- Singly connected networks (polytrees):
    - Any two nodes are connected by at most one (undirected path).
    - For these networks, time and space complexity of variable elimination are $O(nd^k)$.

---

# Worst-case complexity?

.center.width-80[![](figures/lec6/3sat.png)]

3SAT is a special case of inference:
- CSP: $(u\_1 \lor u\_2 \lor u\_3) \wedge (\lnot u\_1 \lor \lnot u\_2 \lor u\_3) \wedge (u\_2 \lor \lnot u\_3 \lor u\_4)$
- $P(U\_i=0)=P(U\_i=1)=0.5$
- $C\_1 = U\_1 \lor U\_2 \lor U\_3$; $C\_2 = \lnot U\_1 \lor \lnot  U\_2 \lor U\_3$; $C\_3 = U\_2 \lor \lnot  U\_3 \lor U\_4$
- $D\_1 = C\_1$; $D\_2 = D\_1 \wedge C\_2$
- $Y = D\_2 \wedge C\_3$

---

class: middle

If we can answer whether $P(Y=1)>0$, then we answer whether 3SAT has a solution.
- By reduction, inference in Bayesian networks is therefore **NP-complete**.
- There is no known efficient probabilistic inference algorithm in general.

???

R: explain what is reduction (oral)

---

class: middle

# Continuous variables

---

# Random variables

Let $X: \Omega \to D\_X$ be a random variable.
- When $D\_X$ is finite or countably infinite, $X$ is called a discrete random variable.
- Its probability distribution is described by a probability mass function that assigns a probability to each value $x \in D\_X$.
- When $D\_X$ is uncountably infinite (e.g., $D\_X = \mathbb{R}$), $X$ is called a *continuous random variable*.
- If $X$ is absolutely continuous, its probability distribution is described by a **density function** $p$ that assigns a probability to any interval $[a,b] \subseteq D\_X$ such that
$$P(a < X \leq b) = \int\_a^b p(x) dx,$$
where $p$ is non-negative piecewise continuous and such that $\int\_{D\_X} p(x)dx=1$.

???

RVs and densities are a layer of abstraction
http://ai.stanford.edu/~paskin/gm-short-course/lec1.pdf

---

# Uniform

.center.width-60[![](figures/lec6/uniform.png)]

The uniform distribution $\mathcal{U}(a,b)$ is described by the density function
$$
p(x) = \begin{cases}
\frac{1}{b-a} & \text{if } x \in \[a,b\]\\\\
0 & \text{otherwise}
\end{cases}$$
where $a \in \mathbb{R}$ and $b \in \mathbb{R}$ are the bounds of its support.


---

# Normal

.center.width-60[![](figures/lec6/normal.png)]

The normal (or Gaussian) distribution $\mathcal{N}(\mu,\sigma)$ is described by the density function
$$p(x) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$$
where $\mu \in \mathbb{R}$ and $\sigma \in \mathbb{R}^+$ are its mean and standard deviation parameters.

---

# Multivariate normal

.center.width-60[![](figures/lec6/mvn.png)]

The multivariate normal distribution generalizes to $N$ random variables. Its (joint) density function is defined as
$$p(\mathbf{x}=x\_1, ..., x\_n) = \frac{1}{\sqrt{(2\pi)^n|\Sigma|}} \exp\left(-\frac{1}{2} (\mathbf{x}-\mathbf{\mu})^T \Sigma^{-1} (\mathbf{x}-\mu) \right) $$
where $\mu \in \mathbb{R}^n$ and $\Sigma \in \mathbb{R}^{n\times n}$ is positive semi-definite.

---

class: middle

- The (multivariate) Normal density is the only density for real random variables that is
**closed under marginalization and multiplication**.
- Also, a linear (or affine) function of a Normal random variable is
Normal; and, a sum of Normal variables is Normal.
- For these reasons, the algorithms we will discuss will be tractable only for
finite random variables or Normal random variables.

???

Be more precise and cite Bishop pg 93?

---

# Hybrid Bayesian networks

<br><br>
.center.width-60[![](figures/lec6/continuous-net.png)]

What if we have both *discrete* (e.g., $\text{Subsidy}$ and $\text{Buys}$) and *continuous*
variables (e.g., $\text{Harvest}$ and $\text{Cost}$) in a same Bayesian network?

---

class: middle

## Options

- Discretization: transform continuous variables into discrete variables.
    - Issues: possibly large errors due to precision loss, large CPTs.
- Define the conditional distribution with a **finitely parameterized** canonical distribution.
    - e.g., assume it is a Gaussian distribution.
- Use a non-parametric representation.

---

class: middle

## Continuous child variables

- We need to specify a conditional density function for each continuous child variable
given continuous parents, for each possible assignment to discrete parents.
    - e.g., we need to specify both $p(c|h,s)$ and $p(c|h,\lnot s)$
- Common choice: the **linear Gaussian model** (LG):
    - $p(c|h,s) = \mathcal{N}(c|a\_th+b\_t, \sigma_t^2)$
    - $p(c|h,\lnot s) = \mathcal{N}(c|a\_fh+b\_f, \sigma_f^2)$

.center.width-90[![](figures/lec6/joint-density.png)]

---

class: middle

## Conditional Gaussian network

- The joint distribution of an all-continuous network with linear Gaussian distributions
is a multivariate Gaussian.
- The joint distribution of a network with discrete or linear Gaussian continuous variables is
a **conditional Gaussian network**.
    - i.e., a multivariate Gaussian over all continuous variables for each combination of the discrete variable values.

---

class: middle

## Discrete child variables, with continuous parents

- We need to specify a conditional distribution for each discrete child variable,
given continuous parents.
- It is often reasonable to assume that the probability values of the discrete outcomes are almost piece-wise constant but *vary smoothly in intermediate regions*.

---

class: middle

For example, if $B$ is binary, $P(b|c)$ could be a "soft" threshold, such as the **probit distribution** for which
$$P(b | c) = \Phi((c - \mu) / \sigma),$$
where $\Phi$ is the cumulative distribution function of the (standard) normal distribution.

.center.width-60[![](figures/lec6/probit.png)]

---

# Variable elimination

Variable elimination in hybrid Bayesian networks can be conducted similarly as in the discrete case,
by replacing **summations with integrations**.
- Exact inference remains possible *under some assumptions*.
    - e.g., for linear Gaussian models, queries can all be derived analytically.
- However, this often **does not scale** to arbitrary continuous distributions.
    - e.g., numerical approximations of integrals amount to discretize continuous variables.

---

class: middle

# Approximate inference

a.k.a. Monte Carlo methods

---

class: middle

Exact inference is **intractable** for most probabilistic models of practical interest.
(e.g., involving many variables, continuous and discrete, undirected cycles, etc).

## Solution

Abandon exact inference and develop  **approximate** but *faster* inference algorithms:
- *Sampling methods*: produce answers by repeatedly generating random numbers from a distribution of interest.
- *Variational methods*: formulate inference as an optimization problem.
- *Belief propagation methods*: formulate inference as a message-passing algorithm.

---

# Sampling methods

Basic idea:
- Draw $N$ samples from a sampling distribution $S$.
- Compute an approximate posterior probability $\hat{P}$.
- Show this approximate converges to the true probability distribution $P$.

## Why sampling?

Generating samples is often much faster than computing the right answer (e.g., with variable elimination).

.center.width-70[![](figures/lec6/sampling-cartoon.png)]

.footnote[Image credits: [CS188](http://ai.berkeley.edu/lecture_slides.html), UC Berkeley.]

---

# Sampling

How to sample from the distribution of a discrete variable $X$?
- Assume $k$ discrete outcomes $x_1, ..., x_k$ with probability $P(x_i)$.
- Assume sampling from $\mathcal{U}(0,1)$ is possible.
    - e.g., as enabled by a standard `rand()` function.
- Divide the $[0,1]$ interval into $k$ regions, with region $i$ having size $P(x_i)$.
- Sample $u \sim \mathcal{U}(0,1)$ and return the value associated to the region in which $u$ falls.

<br>
.center.width-60[![](figures/lec6/sampling.png)]

---

class: middle

.grid[
.kol-1-3.center[
$P(C)$

| $C$ | $P$ |
| --- | --- |
| $\text{red}$ | $0.6$ |
| $\text{green}$ | $0.1$ |
| $\text{blue}$ | $0.3$ |
]
.kol-2-3[<br>
$$\begin{aligned}
0 \leq u < 0.6 &\to C = \text{red} \\\\
0.6 \leq u < 0.7 &\to C = \text{green} \\\\
0.7 \leq u < 1 &\to C = \text{blue} \\\\
\end{aligned}$$
]
]

.center.width-70[![](figures/lec6/sampling-colors.png)]

.footnote[Image credits: [CS188](http://ai.berkeley.edu/lecture_slides.html), UC Berkeley.]

---

class: middle

The same algorithm extends to continuous variables, assuming access to the **inverse cumulative distribution function** $F^{-1}$.
- for $u \in [0,1]$, $F^{-1}(u) = b$ such that $F(b)=u$, where $F$ is the cumulative distribution function
$$F(b) = P(X < b)= \int\_0^b p(x)dx.$$
- $F^{-1}$ is known analytically for most canonical distributions.

<span class="Q">[Q]</span> How to extend to arbitrary multivariate distributions?

???

R: make plot?
Draw the situation for the continuous case.

---

# Prior sampling

Sampling from a Bayesian network, *without observed evidence*:
- Sample each variable in turn, **in topological order**.
- The probability distribution from which the value is sampled is conditioned on the values already assigned to the variable's parents.

---

class: middle

.center.width-100[![](figures/lec6/ancestral-sampling.png)]

<br>

.center.width-100[![](figures/lec6/ancestral-sampling-cartoon.png)]

.footnote[Image credits: [CS188](http://ai.berkeley.edu/lecture_slides.html), UC Berkeley.]

---

class: middle

.center.width-90[![](figures/lec6/as1.png)]

---

class: middle
count: false

.center.width-90[![](figures/lec6/as2.png)]

---

class: middle
count: false

.center.width-90[![](figures/lec6/as3.png)]

---

class: middle
count: false

.center.width-90[![](figures/lec6/as4.png)]

---

class: middle
count: false

.center.width-90[![](figures/lec6/as5.png)]

---

class: middle
count: false

.center.width-90[![](figures/lec6/as6.png)]

---

class: middle
count: false

.center.width-90[![](figures/lec6/as7.png)]

---

class: middle

## Example

We will collect a bunch of samples from the Bayesian network:

$c, \lnot s, r, w$<br>
$c, s, r, w$<br>
$\lnot c, s, r, \lnot w$<br>
$c, \lnot s, r, w$<br>
$\lnot c, \lnot s, \lnot r, w$

If we want to know $P(W)$:
- We have counts $\langle w:4, \lnot w:1 \rangle$
- Normalize to obtain $\hat{P}(W) = \langle w:0.8, \lnot w:0.2 \rangle$
- This will get closer to the true distribution $P(W)$ as we collect more samples.

---

class: middle

## Analysis

The probability that prior sampling generates a particular event is
$$S\_{PS}(x\_1, ..., x\_n) = \prod\_{i=1}^n P(x\_i | \text{parents}(X\_i)) = P(x\_1,...,x\_n)$$
i.e., the Bayesian network's joint probability.

Let $N\_{PS}(x\_1, ..., x\_n)$ denote the number of samples of an event. We
define the probability **estimate** $$\hat{P}(x\_1, ..., x\_n) = N\_{PS}(x\_1, ..., x\_n) / N.$$

---

class: middle

Then,
$$\begin{aligned}
\lim\_{N \to \infty} \hat{P}(x\_1,...,x\_n) &= \lim\_{N \to \infty} N\_{PS}(x\_1, ..., x\_n) / N \\\\
&= S\_{PS}(x\_1, ..., x\_n) \\\\
&= P(x\_1, ..., x\_n)
\end{aligned}$$
Therefore, prior sampling is consistent:
$$P(x\_1, ..., x\_n) \approx N\_{PS}(x\_1, ..., x\_n) / N$$

---

# Rejection sampling

Using prior sampling, an estimate $\hat{P}(x|e)$ can be formed from the proportion of samples $x$ *agreeing with the evidence* $e$ among all samples agreeing with the evidence.

<br><br><br>
.center.width-100[![](figures/lec6/rejection-sampling-cartoon.png)]

.footnote[Image credits: [CS188](http://ai.berkeley.edu/lecture_slides.html), UC Berkeley.]

---

class: middle

.center.width-100[![](figures/lec6/rejection-sampling.png)]

---

class: middle


## Analysis

Let consider the posterior probability estimate $\hat{P}(x|e)$ formed by rejection sampling:

$$\begin{aligned}
\hat{P}(x|e) &= N\_{PS}(x,e) / N\_{PS}(e) \\\\
&= \frac{N\_{PS}(x,e)}{N} / \frac{N\_{PS}(e)}{N} \\\\
&\approx P(x,e) / P(e) \\\\
&= P(x|e)
\end{aligned}$$

Therefore, rejection sampling returns *consistent* posterior estimates.

- The standard deviation of the error in each probability is $O(1/\sqrt{n})$.
- **Problem**: many samples are rejected!
    - Hopelessly expensive if the evidence is unlikely, i.e. if $P(e)$ is small.
    - Evidence is not exploited when sampling.

---

# Likelihood weighting

Idea: *clamp* the evidence variables, sample the rest.
- Problem: the resulting sampling distribution is not consisent.
- Solution: **weight** by probability of evidence given parents.

<br><br><br>
.center.width-100[![](figures/lec6/likelihood-weighting-cartoon.png)]

.footnote[Image credits: [CS188](http://ai.berkeley.edu/lecture_slides.html), UC Berkeley.]

---

class: middle

.center.width-100[![](figures/lec6/importance-sampling.png)]

---

class: middle

.center.width-100[![](figures/lec6/lw1.png)]

---

class: middle
count: false

.center.width-100[![](figures/lec6/lw2.png)]

---

class: middle
count: false

.center.width-100[![](figures/lec6/lw3.png)]

---

class: middle
count: false

.center.width-100[![](figures/lec6/lw4.png)]

---

class: middle
count: false

.center.width-100[![](figures/lec6/lw5.png)]

---

class: middle

## Analysis

The sampling probability for an event with likelihood weighting is
$$S\_{WS}(x,e) = \prod\_{i=1}^l P(x\_i|\text{parents}(X\_i)),$$
where the product is over the non-evidence variables.
The weight for a given sample $x,e$ is
$$w(x,e) = \prod\_{i=1}^m P(e\_i|\text{parents}(E\_i)),$$
where the product is over the evidence variables.

The weighted sampling probability is
$$
\begin{aligned}
S\_{WS}(x,e) w(x,e) &= \prod\_{i=1}^l P(x\_i|\text{parents}(X\_i)) \prod\_{i=1}^m P(e\_i|\text{parents}(E\_i)) \\\\
&= P(x,e)
\end{aligned}
$$

???

R: improve the description of how probability estimates are built.

---

class: middle



The estimated joint probability is computed as follows:

$$\begin{aligned}
\hat{P}(x,e) &= N\_{WS}(x,e) w(x,e) / N \\\\
&\approx S\_{WS}(x,e) w(x,e) \\\\
&= P(x,e)
\end{aligned}$$

From this, the estimated posterior probability is given by:
$$\begin{aligned}
\hat{P}(x|e) &= \hat{P}(x,e) / \hat{P}(e) \\\\
&\approx P(x,e) / P(e) = P(x|e)
\end{aligned}$$

Hence likelihood weighting returns *consistent* estimates.
- Performance **still degrades** with many evidence variables.
- A few samples have nearly all the total weight.

---

class: middle

## Comments

- Likelihood weighting is *good*:
    - The evidence is taken into account to generate a sample.
    - More of the samples will reflect the state of the world suggested by the evidence.
- Likelihood weighting **does not solve all problems**:
    - The evidence influences the choice of downstream variables, but not upstream ones.
- We would like to consider evidence when we sample *every variable*.

---

# Gibbs sampling

## Procedure
- Keep track of a full instance $x\_1, ..., x\_n$.
- Start with an arbitrary instance consistent with the evidence.
- Sample one variable at a time, conditioned on all the rest, but keep the evidence fixed.
- Keep repeating this for a long time.

The sampling process settles into a **dynamic equilibrium** in which the long-run fraction of time spent in each state is exactly proportional to its posterior probability.

---

class: middle

.center.width-100[![](figures/lec6/gibbs-sampling.png)]
<br>

## Rationale
- Both upstream and downstream variables condition on evidence.
- In contrast, likelihood weighting only conditions on upstream evidence, and hence the resulting weights might be very small.

---

class: middle

## Example

.grid[
.kol-1-4[
1) Fix the evidence.
]
.kol-1-4.width-100[![](figures/lec6/gibbs-init.png)]
.kol-1-4[
2) Randomly initialize the other variables
]
.kol-1-4.width-100[![](figures/lec6/gibbs-init2.png)]
]

3) Repeat
- Choose a non-evidence variable $X$.
- Resample $X$ from $P(X|\text{all other variables})$.

.center.width-100[![](figures/lec6/gibbs-process.png)]

---

class: middle

## Demo

See `code/lecture6-gibbs.ipynb`.

---

class: middle

## MCMC

- Gibbs sampling is a special case of a more general set of methods called
**Markov chain Monte Carlo** (MCMC) methods.
- Metropolis-Hastings is one of the most famous MCMC methods.
    - Gibbs sampling is a special case of Metropolis-Hastings.

---

# Summary

- **Exact inference** by variable elimination .
    - NP-complete on general graphs, but polynomial on polytrees.
    - space = time, very sensitive to topology.
- **Approximate inference** gives reasonable estimates of the true posterior probabilities in a network and can cope with much larger networks than can exact algorithms.
    - LW does poorly when there is lots of evidence.
    - LW and GS generally insensitive to topology.
    - Convergence can be slow with probabilities close to 1 or 0.
    - Can handle arbitrary combinations of discrete and continuous variables.
- Want to know more about sampling methods? Follow [MATH2022](https://www.programmes.uliege.be/cocoon/en/cours/MATH2022-1.html).

---

class: end-slide, center
count: false

The end.

---

# References

- Cooper, Gregory F. "The computational complexity of probabilistic inference using Bayesian belief networks." Artificial intelligence 42.2-3 (1990): 393-405.
