class: middle, center, title-slide

# Introduction to Artificial Intelligence

Lecture 5: Probabilistic reasoning I

---

# Today

.grid[
.col-1-2[
- *Probability*:
    - Random variables
    - Joint and marginal distributions
    - Conditional distributions
    - Product rule, Chain rule, Bayes' rule
    - Inference
- *Bayesian networks*:
    - X, Y , Z
]
.col-1-2[
![](figures/lec5/proba-cartoon.png)
]
]

**You will need these concepts a lot! (Now and in future courses)**

.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

---

# Inference in Ghostbusters

.center.width-40[![](figures/lec5/gb-grid.png)]

- A ghost is in the grid somewhere.
- Sensor readings tell how close a square is to the ghost.
    - On the ghost: red
    - 1 or 2 away: orange
    - 3 or 4 away: yellow
    - 5+ away" green
- Sensors are *noisy*, but we know $P(Color|Distance)$.

.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

---

# Inference in Ghostbusters

.center[
<video controls preload="auto" height="400" width="640">
  <source src="./figures/lec5/gb-noprob.mp4" type="video/mp4">
</video>]

<span class="Q">[Q]</span> Could we use a logical agent for this game?

.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

---

class: middle, center

# Quantifying uncertainty

---

# Uncertainty

- General situation:
    - *Observed variables* (evidence): agent knows certain things about the state of the world (e.g., sensor readings).
    - *Unobserved variables*: agent needs to reason about other aspects that are **uncertain** (e.g., where the ghost is).
    - *Model*: agent knows or believes something about how the known variables relate to the unknown variables.
- How to handle uncertainty?
    - A purely logical approach either:
        - risks falsehood (because of ignorance about the world or laziness in the model)
        - leads to conclusions that are too weak for decision making.
    - **Probabilistic reasoning** provides a framework for managing our knowledge and *beliefs*.

---

# Probability

- Probabilistic assertions **summarize** effects of
    - *laziness* (failure to enumerate all world states)
    - *ignorance* (lack of relevant facts, initial conditions, correct model, etc).
- *Subjective* or *Bayesian* **probabilities** relate propositions to one's own state of knowledge.
    - e.g., $P(\text{ghost in } [3,2]) = 0.02$
- These are **not** claims of a "probabilistic tendency" in the current situation (but might be learned from past experience of similar situations).
- Probabilities of propositions change with new evidence:
    - e.g., $P(\text{ghost in } [3,2] | \text{red in } [3,2]) = 0.99$

---

# Probability basics

- Begin with a set $\Omega$, the *sample space*.
    - e.g., 6 possible rolls of a die.
    - $\omega \in \Omega$ is a *sample point*, *possible world* or *atomic event*.
- A **probability space** is a sample space with an assignment $P(\omega)$ for every $\omega \in \Omega$ such that:
    - $0 \leq P(\omega) \leq 1$
    - $\sum_{\omega} P(\omega) = 1$
    - e.g., $P(1) = P(2) = P(3) = P(4) = P(5) = P(6) = \frac{1}{6}$

---

# Random variables

- A **random variable** is a function $X: \Omega \to D\_X$ from the sample space to some domain.
    - e.g., $Odd(1) = true$ and $D_{Odd} = \\{ true, false \\}$.
- $P$ induces a **probability distribution** for any random variable $X$.
    - $P(X=x\_i) = \sum\_{\\{\omega: X(\omega)=x\_i\\}} P(\omega)$
    - e.g., $P(Odd=true) = P(1)+P(3)+P(5) = \frac{1}{2}$.
    - When clear from the context, we will denote $P(X=x\_i)$ as $P(x_i)$.
- In practice, we will use a random variable to represent some aspect of the world about which we (may) have uncertainty.
    - $R$: Is it raining?
    - $T$: Is it hot or cold?
    - $L$: Where is the ghost?
    - ...

---

# Probability distributions

- Intuitively, one can think of the *probability distribution* of a random variable as a **table** that associates a probability value to each *outcome* (assignment) of the variable.
- By construction, probability values are *normalized* (i.e., sum to $1$).
- This table can be infinite!

.grid[
.center.col-1-2[
$P(W)$

| $W$ | $P$ |
| --- | --- |
| $sun$ | $0.6$ |
| $rain$ | $0.1$ |
| $fog$ | $0.3$ |
| $meteor$ | $0.0$ |

]
.col-1-2[
![](figures/lec5/pw.png)
]
]

.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

---

# Joint distributions

- A **joint probability distribution** over a set of random variables $X_1, ..., X_n$ specifies
the probability of each outcome.

$$P(x\_1, ..., x\_n) = \sum\_{\\{\omega: X\_1(\omega)=x\_1, ..., X\_n(\omega)=x\_n\\}} P(\omega)$$

- Example $P(T,W)$:

.center[
| $T$ | $W$ | $P$ |
| --- | --- | --- |
| $hot$ | $sun$ | $0.4$ |
| $hot$ | $rain$ | $0.1$ |
| $cold$ | $sun$ | $0.2$ |
| $cold$ | $rain$ | $0.3$ |
]

---

# Events

- An **event** is a set $E$ of outcomes.
    - $P(E) = \sum_{(x_1, ..., x_n) \in E} P(x_1, ..., x_n)$
- From a joint distribution, the probability of any event can be calculated.
    - Probability that it is hot and sunny?
    - Probability that it is hot?
    - Probability that it is hot or sunny?
- Interesting events often correspond to *partial assignments*.
    - e.g., $P(T=hot)$

---

# Marginal distributions

---

# Conditional probability

- mention prior probability

---

# Probabilistic inference

---

# Inference by enumeration

---

# The product rule

---

# The chain rule

---

# The Bayes' rule

---

# Inference with Bayes' rule

---

# Frequentism vs. Bayesianism

pg 491



---

# Ghostbusters, revisited

.center[
<video controls preload="auto" height="400" width="640">
  <source src="./figures/lec5/gb-prob.mp4" type="video/mp4">
</video>]

.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

---

class: middle, center

# Probabilistic reasoning

---

# Summary
