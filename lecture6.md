class: middle, center, title-slide

# Introduction to Artificial Intelligence

Lecture 6: Probabilistic reasoning II

---

# Today

- *Inference in Bayesian networks*:
    - X, Y, Z
- *Probabilistic reasoning over time*:
    - X, Y, Z

---

class: middle, center

# Inference in Bayesian networks

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

.center.width-100[![](figures/lec6/enumeration-tree.png)]

Enumeration is **inefficient**: there are repeated computations!
- e.g., it computes $P(j|a)P(m|a)$ for both values $e$ and $\lnot e$.

---

# Inference by variable elimination

---

# Basic operations

---

# Variable elimination algorithm

.center.width-100[![](figures/lec6/inference-ve.png)]

---

# Irrelevant variables

---

# Complexity of exact inference

---

# Inference by stochastic simulation

---

# Approximate inference by MCMC

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
