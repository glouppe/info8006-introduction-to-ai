class: middle, center, title-slide

# Introduction to Artificial Intelligence

Lecture 6: Probabilistic reasoning II

---

# Today

- *Inference*:
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
    - ...

---

# Inference by enumeration

1. *Select* the entries consistent with the evidence  $E_1, ..., E_k = e_1, ..., e_k$.
2. *Marginalize* out the hidden variables to obtain the joint of the query and the evidence variables.
$$P(Q,e\_1,...,e\_k) = \sum\_{h\_1, ..., h\_r} P(Q, h\_1, ..., h\_r, e\_1, ..., e\_k)$$
3. *Normalize*.
$$Z = \sum_q P(Q=q,e_1,...,e_k)$$
$$P(Q|e_1, ..., e_k) = \frac{1}{Z} P(Q,e_1,...,e_k)$$

---

# Inference by enumeration in BNs

---

# Enumeration algorithm

---

# Evaluation tree

---

# Variable elimination

---

# Basic operations

---

# Variable elimination algorithm

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
