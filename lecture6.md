class: middle, center, title-slide

# Introduction to Artificial Intelligence

Lecture 6: Probabilistic reasoning II

---

# Today

- *Exact inference*:
    - Inference by enumeration
    - Inference by variable elimination
    - Complexity of exact inference
- *Approximate inference*:
    - Stochastic simulation
    - Rejection sampling
    - Importance sampling
    - MCMC
- *Probabilistic reasoning over time*:
    - X, Y, Z

---

class: middle, center

# Exact inference

---

# Inference tasks

- Inference: **computing a desired probability** from a joint probability distribution.
- Examples:
    - *Simple queries*: $P(X\_i|E=e)$
    - *Conjunctive queries*: $P(X\_i,X\_j|E=e)=P(X\_i|E=e)P(X\_j|X\_i,E=e)$
    - *Most likely explanation*: $\arg \max_q P(Q=q|E=e)$
        - Do you need to necessarily know $P(Q=q|E=e)$ to answer this?
    - *Optimal decisions*: take the decision that maximizes the expected utility of the outcomes.
        - requires $P(outcome|action,evidence)$
    - *Value of information*: which evidence to seek next?

---

# Inference by enumeration

Start from the joint distribution $P(Q, E\_1, ..., E\_k, H\_1, ..., H\_r)$.
1. *Select* the entries consistent with the evidence  $E_1, ..., E_k = e_1, ..., e_k$.
2. *Marginalize* out the hidden variables to obtain the joint of the query and the evidence variables $P(Q,e\_1,...,e\_k)$.
3. *Normalize* by $Z = P(e_1,...,e_k) = \sum_q P(q,e_1,...,e_k)$.

---

# Inference by enumeration in BNs

Consider the burglary network and the query $P(B|j,m)$:

.pull-right[![](figures/lec6/bn-burglar.png)]

$P(B|j,m)$<br>
$= P(B,j,m) / P(j,m)$<br>
$= \alpha P(B,j,m)$<br>
$= \alpha \sum_e \sum_a P(B,j,m,e,a)$

Rewrite full joint entries using product of CPT entries:

$P(B|j,m)$<br>
$= \alpha \sum_e \sum_a P(B)P(e)P(a|B,e)P(j|a)P(m|a)$
$= \alpha  P(B) \sum_e P(e) \sum_a P(a|B,e)P(j|a)P(m|a)$

Recursive depth-first enumeration: **$O(n)$** space, **$O(d^n)$** time

---

# Enumeration algorithm

.center.width-100[![](figures/lec6/inference-enumeration.png)]

---

# Evaluation tree

.center.width-90[![](figures/lec6/enumeration-tree.png)]

Enumeration is **inefficient**: there are repeated computations!
- e.g., $P(j|a)P(m|a)$ is computed twice, once for $e$ and once for $\lnot e$.
- These can be avoided by storing intermediate results!

---

# Inference by variable elimination

- The **variable elimination** (VE) algorithm carries out summations right-to-left and *stores intermediate results* (called **factors**) to avoid recomputations.
- The algorithm interleaves:
    - Joining sub-tables
    - Eliminating hidden variables

<hr>

Example:

$P(B|j,m)$<br>
$= \alpha  P(B) \sum_e P(e) \sum_a P(a|B,e)P(j|a)P(m|a)$<br>
$= \alpha  f_1(B) \sum_e f_2(E) \sum_a f_3(A,B,E) f_4(A) f_5(A)$<br>
$= \alpha  f_1(B) \sum_e f_2(E) f_6(B,E)$ (eliminate $A$)<br>
$= \alpha  f_1(B) f_7(B)$ (eliminate $E$)<br>

---

# VE: factors

- Each **factor $f_i$** is a matrix indexed by the values of its argument variables. E.g.:

.center.width-90[![](figures/lec6/ve-factors.png)]

- Factors are initialized with the CPTs annotating the nodes of the Bayesian network, conditioned on the evidence.

---

# VE: join

The *pointwise product*, or **join**, of two factors $f_1$ and $f_2$ yields a new factor $f$.
- The variables of $f$ are the *union* of the variables in $f_1$ and $f_2$.
- The elements of $f$ are given by the product of the corresponding elements in $f_1$ and $f_2$.

.center.width-100[![](figures/lec6/ve-product.png)]

---

# VE: elimination

*Summing out*, or **eliminating**, a variable from a sum of products of factors:
- move any constant factor outside the summation;
- add up submatrices of pointwise product of remaining factors.
Variable elimination
<hr>

Example (eliminate $E$):

$\sum_e f_2(E) f_3(A,B,E) f_4(A) f_5(A)$<br>
$= f_4(A) f_5(A) \sum_e f_2(E) f_3(A,B,E)$<br>
$= f_4(A) f_5(A) f_6'(A,B)$

---

# Variable elimination algorithm

Idea:
- *Incrementally* build a list of factors from the nodes in the network.
- *Eliminate* hidden variables when encountered.
- *Join* all remaining factors and normalize.

<hr>

.center.width-100[![](figures/lec6/inference-ve.png)]

---

# Irrelevant variables

- Consider the query $P(JohnCalls|Burglar=true)$.
    - $P(J|b) = \alpha P(b) \sum_e P(e) \sum_a P(a|b,e) P(J|a) \sum_m P(m|a)$
- $\sum_m P(m|a) = 1$, therefore $M$ is **irrelevant** for the query.
- In other words, $P(J|b)$ remains unchanged if we remove $M$ from the network.
- **Theorem**: $H$ is irrelevant for $P(Q|E=e)$ unless $H \in \text{ancestors}(\\\{Q\\\} \cup E)$

---

# Elimination ordering

XXX: redraw
.center.width-50[![](figures/lec6/ve-ordering.png)]

- Consider the query $P(X\_n|y\_1,...,y\_n)$.
- Work through the two elimination orderings:
    - $Z, X\_1, ..., X\_{n-1}$
    - $X\_1, ..., X\_{n-1}, Z$
- What is the size of the maximum factor generated for each of the orderings?
- Answer: $2^{n+1}$ vs. $2^2$ (assuming boolean values)

---

# Complexity of exact inference

- The computational and space complexity of variable elimination is determined by **the largest factor**.
- The elimination *ordering* can greatly affect the size of the largest factor.
- Does there always exist an ordering that only results in small factors? **No!**

---

# Worst case complexity?

XXX: reduction to 3SAT, hence NP-complete

---

class: middle, center

# Approximate inference

---

# Ancestral sampling

---

# Rejection sampling

---

# Importance sampling

---

# MCMC

---

class: middle, center

# Probabilistic reasoning over time

---

# Markov models

---

# Hidden Markov models

---

# Particle filters

---

# Summary
