class: middle, center, title-slide

# Introduction to Artificial Intelligence

Lecture 6: Reasoning over time

<br><br>
Prof. Gilles Louppe<br>
[g.louppe@uliege.be](mailto:g.louppe@uliege.be)

---

# Today

Maintain a **belief state** about the world, and update it as time passes and evidence is collected.

.grid[
.kol-1-2[
- Markov models
    - Markov processes
    - Inference tasks
    - Hidden Markov models
- Filters
    - Kalman filter
    - Particle filter
]
.kol-1-2[.width-100[![](figures/lec6/outline-cartoon.png)]
]
]

.alert[Do not overlook this lecture!]

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle, black-slide

.center[
<video controls preload="auto" height="400" width="640">
  <source src="./figures/lec6/pacman-no-beliefs.mp4" type="video/mp4">
</video>

.bold[Pacman revenge]: How to make good use of the sonar readings?
]

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

???

```
python3 run.py --nghosts 2 --layout maze_small
python3 run.py --nghosts 3 --layout maze_medium
python3 run.py --nghosts 4 --layout maze_huge

```

---

class: middle

# Markov models

---

class: middle

## Modelling the passage of time

We will consider the world as a *discrete* series of time slices, each of which contains a set of random variables:
- $\mathbf{X}\_t$ denotes the set of **unobservable** state variables at time $t$.
- $\mathbf{E}\_t$ denotes the set of *observable* evidence variables at time $t$.

---

class: middle

We specify:
- a prior ${\bf P}(\mathbf{X}\_0)$ that defines our inital belief state over hidden state variables.
- a **transition model** ${\bf P}(\mathbf{X}\_t | \mathbf{X}\_{0:t-1})$ (for $t > 0$) that defines the probability distribution over the latest state variables, given the previous (unobserved) values.
- a **sensor model** ${\bf P}(\mathbf{E}\_t | \mathbf{X}\_{0:t}, \mathbf{E}\_{0:t-1})$ (for $t > 0$) that defines the probability distribution over the latest evidence variables, given all previous (observed and unobserved) values.

---

# Markov processes

## Markov assumption
- The current state of the world depends only on its immediate previous state(s), i.e., $\mathbf{X}\_t$ depends on only a bounded subset of $\mathbf{X}\_{0:t-1}$.
- Random processes that satisfy this assumption are called **Markov processes**.

---

class: middle

## First-order Markov processes

- Markov processes such that $${\bf P}(\mathbf{X}\_t | \mathbf{X}\_{0:t-1}) = {\bf P}(\mathbf{X}\_t | \mathbf{X}\_{t-1}).$$
- i.e., $\mathbf{X}\_t$ and $\mathbf{X}\_{0:t-2}$ are conditionally independent given $\mathbf{X}\_{t-1}$.

<br>
.center.width-100[![](figures/lec6/markov-process.png)]

---

exclude: True
class: middle

## Second-order Markov processes

- Markov processes such that $${\bf P}(\mathbf{X}\_t | \mathbf{X}\_{0:t-1}) = {\bf P}(\mathbf{X}\_t | \mathbf{X}\_{t-2}, \mathbf{X}\_{t-1}).$$
- i.e., $\mathbf{X}\_t$ and $\mathbf{X}\_{0:t-3}$ are conditionally independent given $\mathbf{X}\_{t-1}$ and $\mathbf{X}\_{t-2}$.

<br>
.center.width-100[![](figures/lec6/markov-process-2.png)]

---

class: middle

## Sensor Markov assumption

- Additionally, we make a (first-order) **sensor Markov assumption**: $${\bf P}(\mathbf{E}\_t | \mathbf{X}\_{0:t}, \mathbf{E}\_{0:t-1}) = {\bf P}(\mathbf{E}\_t | \mathbf{X}\_{t})$$

## Stationarity assumption

- The transition and the sensor models are the same for all $t$ (i.e., the laws of physics do not change with time).

---

# Joint distribution

<br>
.center.width-100[![](figures/lec6/smoothing-dbn.svg)]
<br>

A Markov process can be described as a *growable* Bayesian network, unrolled infinitely through time, with a specified **restricted structure** between time steps.

Therefore, the *joint distribution* of all variables up to $t$ in a (first-order) Markov process is
$${\bf P}(\mathbf{X}\_{0:t}, \mathbf{E}\_{1:t}) = {\bf P}(\mathbf{X}\_{0}) \prod\_{i=1}^t {\bf P}(\mathbf{X}\_{i} | \mathbf{X}\_{i-1}) {\bf P}(\mathbf{E}\_{i}|\mathbf{X}\_{i}).$$

---

class: middle

## Example: Will you take your umbrella today?


.center.width-80[![](figures/lec6/weather-bn.svg)]

.grid[
.kol-1-2[
.center.width-100[![](figures/lec6/weather-forecast.png)]
]
.kol-1-2[
- ${\bf P}(\text{Umbrella}\_t | \text{Rain}\_t)$?
- ${\bf P}(\text{Rain}\_t | \text{Umbrella}\_{0:t-1})$?
- ${\bf P}(\text{Rain}\_{t+2} | \text{Rain}\_{t})$?
]]

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

.center.width-60[![](figures/lec6/weather-transition.png)]

The transition model ${\bf P}(\text{Rain}\_t | \text{Rain}\_{t-1})$ can equivalently be represented by a state transition diagram.

---

# Inference tasks

- *Prediction*: ${\bf P}(\mathbf{X}\_{t+k}| \mathbf{e}\_{1:t})$ for $k>0$
    - Computing the posterior distribution over future states.
    - Used for evaluation of possible action sequences.
- *Filtering*: ${\bf P}(\mathbf{X}\_{t}| \mathbf{e}\_{1:t})$
    - Filtering is what a rational agent does to keep track of the current hidden state $\mathbf{X}\_t$, its **belief state**, so that rational decisions can be made.
- *Smoothing*: ${\bf P}(\mathbf{X}\_{k}| \mathbf{e}\_{1:t})$ for $0 \leq k < t$
    - Computing the posterior distribution over past states.
    - Used for building better estimates, since it incorporates more evidence.
    - Essential for learning.    
- *Most likely explanation*: $\arg \max\_{\mathbf{x}\_{1:t}} P(\mathbf{x}\_{1:t}| \mathbf{e}\_{1:t})$
    - Decoding with a noisy channel, speech recognition, etc.

---

# Base cases

.grid[
.kol-1-2.center[
.width-80[![](figures/lec6/base-case2.png)]

$\begin{aligned}
{\bf P}(\mathbf{X}\_2) &= \sum\_{\mathbf{x}\_1} {\bf P}(\mathbf{X}\_2, \mathbf{x}\_1) \\\\
&= \sum\_{\mathbf{x}\_1} P(\mathbf{x}\_1) {\bf P}(\mathbf{X}\_2 | \mathbf{x}\_1)
\end{aligned}$

(Predict) Push ${\bf P}(\mathbf{X}\_1)$ forward through the transition model.
]
.kol-1-2.center[
.width-80[![](figures/lec6/base-case1.png)]

$\begin{aligned}
{\bf P}(\mathbf{X}\_1 | \mathbf{e}\_1) &=\frac{ {\bf P}(\mathbf{e}\_1 | \mathbf{X}\_1) {\bf P}(\mathbf{X}\_1)}{P(\mathbf{e}\_1)} \\\\
&\propto {\bf P}(\mathbf{e}\_1 | \mathbf{X}\_1) {\bf P}(\mathbf{X}\_1)
\end{aligned}$

(Update) Update ${\bf P}(\mathbf{X}\_1)$ with the evidence $\mathbf{e}\_1$, given the sensor model.
]
]

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

# Prediction

.center.width-50[![](figures/lec6/stationary-cartoon.png)]

To predict the future  ${\bf P}(\mathbf{X}\_{t+k}| \mathbf{e}\_{1:t})$:
- **Push** the prior belief state ${\bf P}(\mathbf{X}\_{t} | \mathbf{e}\_{1:t})$ through the transition model:
$${\bf P}(\mathbf{X}\_{t+1}| \mathbf{e}\_{1:t}) = \sum\_{\mathbf{x}\_{t}} {\bf P}(\mathbf{X}\_{t+1} | \mathbf{x}\_{t}) P(\mathbf{x}\_{t} | \mathbf{e}\_{1:t})$$

- Repeat up to $t+k$, using ${\bf P}(\mathbf{X}\_{t+k-1}| \mathbf{e}\_{1:t})$ to compute ${\bf P}(\mathbf{X}\_{t+k}| \mathbf{e}\_{1:t})$.

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle, black-slide

.center[
<video controls preload="auto" height="400" width="640">
  <source src="./figures/lec6/gb-basics.mp4" type="video/mp4">
</video>]

.center[Random dynamics]

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle, black-slide

.center[
<video controls preload="auto" height="400" width="640">
  <source src="./figures/lec6/gb-circular.mp4" type="video/mp4">
</video>]

.center[Circular dynamics]

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle, black-slide

.center[
<video controls preload="auto" height="400" width="640">
  <source src="./figures/lec6/gb-whirlpool.mp4" type="video/mp4">
</video>]

.center[Whirlpool dynamics]

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

.center[
.width-100[![](figures/lec6/prediction.png)]

.width-100[![](figures/lec6/uncertainty.png)]

As time passes, uncertainty "accumulates" if we do not accumulate new evidence.
]

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

# Stationary distributions

What if $t \to \infty$?
- For most chains, the influence of the initial distribution gets lesser and lesser over time.
- Eventually, the distribution converges to a fixed point, called a **stationary distribution**.
- This distribution is such that
$${\bf P}(\mathbf{X}\_\infty) = {\bf P}(\mathbf{X}\_{\infty+1}) = \sum\_{\mathbf{x}\_\infty} {\bf P}(\mathbf{X}\_{\infty+1} | \mathbf{x}\_\infty) P(\mathbf{x}\_\infty) $$

---

class: middle

| $\mathbf{X}\_{t-1}$ | $\mathbf{X}\_{t}$ | $P$ |
| --- | --- | --- |
| $\text{sun}$ | $\text{sun}$ | 0.9 |
| $\text{sun}$ | $\text{rain}$ | 0.1 |
| $\text{rain}$ | $\text{sun}$ | 0.3 |
| $\text{rain}$ | $\text{rain}$ | 0.7 |

## Example

$
\begin{aligned}
P(\mathbf{X}\_\infty = \text{sun}) =&\, P(\mathbf{X}\_{\infty+1} = \text{sun}) \\\\
=&\, P(\mathbf{X}\_{\infty+1}=\text{sun} | \mathbf{X}\_{\infty}=\text{sun}) P(\mathbf{X}\_{\infty}=\text{sun})\\\\
 & + P(\mathbf{X}\_{\infty+1}=\text{sun} | \mathbf{X}\_{\infty}=\text{rain}) P(\mathbf{X}\_{\infty}=\text{rain})\\\\
=&\, 0.9 P(\mathbf{X}\_{\infty}=\text{sun}) + 0.3 P(\mathbf{X}\_{\infty}=\text{rain})
\end{aligned}
$

Therefore, $P(\mathbf{X}\_\infty=\text{sun}) = 3 P(\mathbf{X}\_\infty=\text{rain})$.

Which implies that
$P(\mathbf{X}\_\infty=\text{sun}) = \frac{3}{4}$ and
$P(\mathbf{X}\_\infty=\text{rain}) = \frac{1}{4}$.

---

# Filtering

<br><br>

.center.width-90[![](figures/lec6/observation.png)]
<br>

What if we collect new observations?
Beliefs get reweighted, and uncertainty "decreases".

???

$${\bf P}(\mathbf{X}\_{t+1}| \mathbf{e}\_{1:t+1}) \propto {\bf P}(\mathbf{e}\_{t+1} | \mathbf{X}\_{t+1}) {\bf P}(\mathbf{X}\_{t+1} | \mathbf{e}\_{1:t})$$

---

class: middle

## Bayes filter

An agent maintains a **belief state** estimate ${\bf P}(\mathbf{X}\_{t}| \mathbf{e}\_{1:t})$ and updates it as new evidences $\mathbf{e}\_{t+1}$ are collected.

Recursive Bayesian estimation: ${\bf P}(\mathbf{X}\_{t+1}| \mathbf{e}\_{1:t+1}) = f(\mathbf{e}\_{t+1}, {\bf P}(\mathbf{X}\_{t}| \mathbf{e}\_{1:t}))$
- (Predict step): Project the current belief state forward from $t$ to $t+1$ through the transition model.
- (Update step): Update this new state using the evidence $\mathbf{e}\_{t+1}$.

---

class: middle

$$
\begin{aligned}
{\bf P}(\mathbf{X}\_{t+1}| \mathbf{e}\_{1:t+1}) &= {\bf P}(\mathbf{X}\_{t+1}| \mathbf{e}\_{1:t}, \mathbf{e}\_{t+1}) \\\\
&\propto {\bf P}(\mathbf{e}\_{t+1}| \mathbf{X}\_{t+1}, \mathbf{e}\_{1:t}) {\bf P}(\mathbf{X}\_{t+1}| \mathbf{e}\_{1:t}) \\\\
&\propto {\bf P}(\mathbf{e}\_{t+1}| \mathbf{X}\_{t+1}) {\bf P}(\mathbf{X}\_{t+1}| \mathbf{e}\_{1:t}) \\\\
&\propto {\bf P}(\mathbf{e}\_{t+1}| \mathbf{X}\_{t+1}) \sum\_{\mathbf{x}\_t} {\bf P}(\mathbf{X}\_{t+1}|\mathbf{x}\_t, \mathbf{e}\_{1:t}) P(\mathbf{x}\_t | \mathbf{e}\_{1:t}) \\\\
&\propto {\bf P}(\mathbf{e}\_{t+1}| \mathbf{X}\_{t+1}) \sum\_{\mathbf{x}\_t} {\bf P}(\mathbf{X}\_{t+1}|\mathbf{x}\_t) P(\mathbf{x}\_t | \mathbf{e}\_{1:t})
\end{aligned}
$$

where
- the normalization constant $$Z = P(\mathbf{e}\_{t+1} | \mathbf{e}\_{1:t}) = \sum\_{\mathbf{x}\_{t+1}} P(\mathbf{e}\_{t+1} | \mathbf{x}\_{t+1}) P(\mathbf{x}\_{t+1} | \mathbf{e}\_{1:t}) $$  is used to make probabilities sum to 1;
- in the last expression, the first and second terms are given by the model while the third is obtained recursively.

<!-- $P(\mathbf{X}\_{t+1}| \mathbf{e}\_{1:t+1}) = P(\mathbf{X}\_{t+1}| \mathbf{e}\_{1:t}, \mathbf{e}\_{t+1})$<br>
$\quad = \alpha P(\mathbf{e}\_{t+1}| \mathbf{X}\_{t+1}, \mathbf{e}\_{1:t}) P(\mathbf{X}\_{t+1}| \mathbf{e}\_{1:t}) \quad $<br>
$\quad = \alpha P(\mathbf{e}\_{t+1}| \mathbf{X}\_{t+1}) P(\mathbf{X}\_{t+1}| \mathbf{e}\_{1:t})$<br>
$\quad = \alpha P(\mathbf{e}\_{t+1}| \mathbf{X}\_{t+1}) \sum\_{\mathbf{x}\_t} P(\mathbf{X}\_{t+1}|\mathbf{x}\_t, \mathbf{e}\_{1:t}) P(\mathbf{x}\_t | \mathbf{e}\_{1:t}) $<br>
$\quad = \alpha P(\mathbf{e}\_{t+1}| \mathbf{X}\_{t+1}) \sum\_{\mathbf{x}\_t} P(\mathbf{X}\_{t+1}|\mathbf{x}\_t) P(\mathbf{x}\_t | \mathbf{e}\_{1:t}) $ -->

---

class: middle

We can think of ${\bf P}(\mathbf{X}\_t | \mathbf{e}\_{1:t})$ as a *message* $\mathbf{f}\_{1:t}$ that is propagated **forward** along the sequence, modified by each transition and updated by each new observation.
- Thus, the process can be implemented as $\mathbf{f}\_{1:t+1} \propto \text{forward}(\mathbf{f}\_{1:t}, \mathbf{e}\_{t+1} )$.
- The complexity of a forward update is constant (in time and space) with $t$.

---

class: middle

## Example

.center.width-80[![](figures/lec6/filtering.png)]

<br>

.grid[
.kol-1-4[]
.kol-1-4.center[

| $R\_{t-1}$ | $P(R\_t)$ |
| ---------- | --------- |
| $\text{true}$ | $0.7$ |
| $\text{false}$ | $0.3$ |

]
.kol-1-4.center[

| $R\_{t}$ | $P(U\_t)$ |
| ---------- | --------- |
| $\text{true}$ | $0.9$ |
| $\text{false}$ | $0.2$ |

]
]

???

Solve on blackboard.

---

class: middle, black-slide

.center[
<video controls preload="auto" height="400" width="640">
  <source src="./figures/lec6/pacman-with-beliefs.mp4" type="video/mp4">
</video>

Ghostbusters with a Bayes filter
]

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

???

```
python3 run.py --nghosts 2 --layout maze_small --agentfile sherlockpacman.py --bsagentfile bayesfilter.py --show True
python3 run.py --nghosts 3 --layout maze_medium --agentfile sherlockpacman.py --bsagentfile bayesfilter.py --show True
python3 run.py --nghosts 4 --layout maze_huge --agentfile sherlockpacman.py --bsagentfile bayesfilter.py --show True

```

---

# Smoothing

We want to compute ${\bf P}(\mathbf{X}\_{k}| \mathbf{e}\_{1:t})$ for $0 \leq k < t$.

Divide evidence $\mathbf{e}\_{1:t}$ into $\mathbf{e}\_{1:k}$ and $\mathbf{e}\_{k+1:t}$. Then,

$$
\begin{aligned}
{\bf P}(\mathbf{X}\_k | \mathbf{e}\_{1:t}) &= {\bf P}(\mathbf{X}\_k | \mathbf{e}\_{1:k}, \mathbf{e}\_{k+1:t}) \\\\
&\propto {\bf P}(\mathbf{X}\_k | \mathbf{e}\_{1:k}) {\bf P}(\mathbf{e}\_{k+1:t} | \mathbf{X}\_k, \mathbf{e}\_{1:k}) \\\\
&\propto {\bf P}(\mathbf{X}\_k | \mathbf{e}\_{1:k}) {\bf P}(\mathbf{e}\_{k+1:t} | \mathbf{X}\_k).
\end{aligned}
$$

---

class: middle

Let the **backward** message $\mathbf{b}\_{k+1:t}$ correspond to ${\bf P}(\mathbf{e}\_{k+1:t} | \mathbf{X}\_k)$. Then,
$${\bf P}(\mathbf{X}\_k | \mathbf{e}\_{1:t}) = \alpha\, \mathbf{f}\_{1:k} \times \mathbf{b}\_{k+1:t},$$
where $\times$ is a pointwise multiplication of vectors.


This backward message can be computed using backwards recursion:

$$
\begin{aligned}
{\bf P}(\mathbf{e}\_{k+1:t} | \mathbf{X}\_k) &= \sum\_{\mathbf{x}\_{k+1}} {\bf P}(\mathbf{e}\_{k+1:t} | \mathbf{X}\_k, \mathbf{x}\_{k+1}) {\bf P}(\mathbf{x}\_{k+1} | \mathbf{X}\_k) \\\\
&= \sum\_{\mathbf{x}\_{k+1}} P(\mathbf{e}\_{k+1:t} | \mathbf{x}\_{k+1}) {\bf P}(\mathbf{x}\_{k+1} | \mathbf{X}\_k) \\\\
&= \sum\_{\mathbf{x}\_{k+1}} P(\mathbf{e}\_{k+1} | \mathbf{x}\_{k+1}) P(\mathbf{e}\_{k+2:t} | \mathbf{x}\_{k+1}) {\bf P}(\mathbf{x}\_{k+1} | \mathbf{X}\_k)
\end{aligned}
$$

The first and last factors are given by the model. The second factor is obtained recursively. Therefore,
$$\mathbf{b}\_{k+1:t} = \text{backward}(\mathbf{b}\_{k+2:t}, \mathbf{e}\_{k+1} ).$$

---

class: middle

## Forward-backward algorithm

.center.width-100[![](figures/lec6/forward-backward.png)]

Complexity:
- Smoothing for a particular time step $k$ takes: $O(t)$
- Smoothing a whole sequence (because of caching):  $O(t)$

---

class: middle

## Example

.center.width-80[![](figures/lec6/smoothing.png)]

???

Solve on blackboard.

---

.pull-right.width-80[![](figures/lec6/weather.png)]

# Most likely explanation

Suppose that $[\text{true}, \text{true}, \text{false}, \text{true}, \text{true}]$ is the umbrella sequence.

What is the weather sequence that is the most likely to explain this?
- Does the absence of umbrella at day 3 means it wasn't raining?
- Or did the director forget to bring it?
- If it didn't rain on day 3, perhaps it didn't rain on day 4 either, but the director brought the umbrella just in case?

Among all $2^5$ sequences, is there an (efficient) way to find the most likely one?

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

- The most likely sequence  **is not** the sequence of the most likely states!
- The most likely path to each $\mathbf{x}\_{t+1}$, is the most likely path to *some* $\mathbf{x}\_t$ plus one more step. Therefore,
$$
\begin{aligned}
&\max\_{\mathbf{x}\_{1:t}} {\bf P}(\mathbf{x}\_{1:t}, \mathbf{X}\_{t+1} | \mathbf{e}\_{1:t+1}) \\\\
&\propto {\bf P}(\mathbf{e}\_{t+1}|\mathbf{X}\_{t+1}) \max\_{\mathbf{x}\_t}( {\bf P}(\mathbf{X}\_{t+1} | \mathbf{x}\_t) \max\_{\mathbf{x}\_{1:t-1}} {\bf P}(\mathbf{x}\_{1:t-1}, \mathbf{x}\_{t} | \mathbf{e}\_{1:t}) )
\end{aligned}
$$
- Identical to filtering, except that the forward message $\mathbf{f}\_{1:t} = {\bf P}(\mathbf{X}\_t | \mathbf{e}\_{1:t})$ is replaced with
$$\mathbf{m}\_{1:t} = \max\_{\mathbf{x}\_{1:t-1}} {\bf P}(\mathbf{x}\_{1:t-1}, \mathbf{X}\_{t} | \mathbf{e}\_{1:t}),$$
where $\mathbf{m}\_{1:t}(i)$ gives the probability of the most likely path to state $i$.
- The update has its sum replaced by max, resulting in the **Viterbi algorithm**:
$$\mathbf{m}\_{1:t+1} = \alpha {\bf P}(\mathbf{e}\_{t+1} | \mathbf{X}\_{t+1}) \max\_{\mathbf{x}\_{t}} {\bf P}(\mathbf{X}\_{t+1} | \mathbf{x}\_{t}) \mathbf{m}\_{1:t}$$

???

Naive procedure: use smoothing to compute $P(X\_k|e\_{1:t})$, then output the sequence of the most likely value for each $k$.

---

class: middle

## Example

.center.width-90[![](figures/lec6/viterbi.png)]

???

<span class="Q">[Q]</span> How do you retrieve the path, in addition to its likelihood?

---

# Hidden Markov models

So far, we described Markov processes over arbitrary sets of state variables $\mathbf{X}\_t$ and evidence variables $\mathbf{E}\_t$.
- A **hidden Markov model** (HMM) is a Markov process in which the state $\mathbf{X}\_t$ and the evidence $\mathbf{E}\_t$ are both *single discrete* random variables.
    - $\mathbf{X}\_t = X\_t$, with domain $D\_{X\_t} = \\\{1, ..., S\\\}$
    - $\mathbf{E}\_t = E\_t$, with domain $D\_{E\_t} = \\\{1, ..., R\\\}$
- This restricted structure allows for a reformulation of the forward-backward algorithm in terms of matrix-vector operations.

---

class: middle

## Note on terminology

Some authors instead divide Markov models into two classes, depending on the observability of the system state:
- Observable system state: Markov chains
- Partially-observable system state: Hidden Markov models.

We follow here instead the terminology of the textbook, as defined in the previous slide.

---

class: middle

## Simplified matrix algorithms

- The prior ${\bf P}(X\_0)$ becomes a (normalized) column vector $\mathbf{f}\_0 \in \mathbb{R}_+^S$.
- The transition model ${\bf P}(X\_t | X\_{t-1})$ becomes an $S \times S$ **transition matrix** $\mathbf{T}$, such that $$\mathbf{T}\_{ij} = P(X\_t=j | X\_{t-1}=i).$$
- The sensor model ${\bf P}(E\_t | X\_t)$ is defined as an  $S \times R$ **sensor matrix** $\mathbf{B}$, such that
$$\mathbf{B}\_{ij} = P(E\_t=j | X\_t=i).$$

---

class: middle

- Let the observation matrix $\mathbf{O}\_t$ be a diagonal matrix whose elements corresponds to the column $e\_t$ of the sensor matrix $\mathbf{B}$.
- If we use column vectors to represent forward and backward messages, then we have
$$\mathbf{f}\_{1:t+1} = \alpha \mathbf{O}\_{t+1} \mathbf{T}^T \mathbf{f}\_{1:t}$$
$$\mathbf{b}\_{k+1:t} = \mathbf{T} \mathbf{O}\_{k+1} \mathbf{b}\_{k+2:t},$$
where $\mathbf{b}\_{t+1:t}$ is an all-one vector of size $S$.
- Therefore the forward-backward algorithm needs time $O(S^2t)$ and space $O(St)$.
---

class: middle

## Example

Suppose that $[\text{true}, \text{true}, \text{false}, \text{true}, \text{true}]$ is the umbrella sequence.

$$
\begin{aligned}
\mathbf{f}\_0 &= \left(\begin{matrix}
    0.5 \\\\
    0.5
\end{matrix}\right)\\\\
\mathbf{T} &= \left(\begin{matrix}
0.7 & 0.3 \\\\
0.3 & 0.7
\end{matrix}\right)\\\\
\mathbf{B} &= \left(\begin{matrix}
0.9 & 0.1 \\\\
0.2 & 0.8
\end{matrix}\right)\\\\
\mathbf{O}\_1 = \mathbf{O}\_2 = \mathbf{O}\_4 = \mathbf{O}\_5 &= \left(\begin{matrix}
0.9 & 0.0 \\\\
0.0 & 0.2
\end{matrix}\right) \\\\
\mathbf{O}\_3 &= \left(\begin{matrix}
0.1 & 0.0 \\\\
0.0 & 0.8
\end{matrix}\right)
\end{aligned}
$$

See `code/lecture6-forward-backward.ipynb` for the execution.

---

class: middle

## Stationary distribution

The stationary distribution $\mathbf{f}$ of a HMM is a distribution such that
$$\mathbf{f} = \mathbf{T}^T \mathbf{f}.$$
Therefore, the stationary distribution corresponds to a (normalized) eigenvector of the transposed transition matrix with an eigenvalue of $1$.

---

class: middle

# Filters

---

class: middle

.center.width-50[![](figures/lec6/robot-helicopter.png)]

Suppose we want to track the position and velocity of a robot from noisy observations collected over time.

Formally, we want to estimate **continuous** state variables such as
- the position $\mathbf{X}\_t$ of the robot at time $t$,
- the velocity $\mathbf{\dot{X}}\_t$ of the robot at time $t$.

We assume *discrete* time steps.

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

???

R: revise a bit the flow for this part of the lecture.

---

# Continuous variables

Let $X: \Omega \to D\_X$ be a random variable.
- When $D\_X$ is uncountably infinite (e.g., $D\_X = \mathbb{R}$), $X$ is called a *continuous random variable*.
- If $X$ is absolutely continuous, its probability distribution is described by a **density function** $p$ that assigns a probability to any interval $[a,b] \subseteq D\_X$ such that
$$P(a < X \leq b) = \int\_a^b p(x) dx,$$
where $p$ is non-negative piecewise continuous and such that $$\int\_{D\_X} p(x)dx=1.$$

---

class: middle

## Uniform

.center.width-60[![](figures/lec5/uniform.png)]

The uniform distribution $\mathcal{U}(a,b)$ is described by the density function
$$
p(x) = \begin{cases}
\frac{1}{b-a} & \text{if } x \in \[a,b\]\\\\
0 & \text{otherwise}
\end{cases}$$
where $a \in \mathbb{R}$ and $b \in \mathbb{R}$ are the bounds of its support.

---

class: middle

## Normal

.center.width-60[![](figures/lec5/normal.png)]

The normal (or Gaussian) distribution $\mathcal{N}(\mu,\sigma)$ is described by the density function
$$p(x) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$$
where $\mu \in \mathbb{R}$ and $\sigma \in \mathbb{R}^+$ are its mean and standard deviation parameters.

???

Comment that
- $\mu$ is the location
- $\sigma$ is the width of the normal

---

class: middle

## Multivariate normal

.center.width-60[![](figures/lec5/mvn.png)]

The multivariate normal distribution generalizes to $n$ random variables. Its (joint) density function is defined as
$$p(\mathbf{x}=x\_1, ..., x\_n) = \frac{1}{\sqrt{(2\pi)^n|\mathbf{\Sigma}|}} \exp\left(-\frac{1}{2} (\mathbf{x}-\mathbf{m})^T \mathbf{\Sigma}^{-1} (\mathbf{x}-\mathbf{m}) \right) $$
where $\mathbf{m} \in \mathbb{R}^n$ and $\mathbf{\Sigma} \in \mathbb{R}^{n\times n}$ is positive semi-definite.

---

class: middle

## Cheat sheet for Gaussian models (Särkkä, 2013)

If the random variables $\mathbf{x}$ and $\mathbf{y}$ have Gaussian probability distributions
$$
\begin{aligned}
p(\mathbf{x}) &= \mathcal{N}(\mathbf{x}|\mathbf{m}, \mathbf{P}) \\\\
p(\mathbf{y}|\mathbf{x}) &= \mathcal{N}(\mathbf{y}|\mathbf{H}\mathbf{x}+\mathbf{u}, \mathbf{R}),
\end{aligned}
$$
then the joint distribution of $\mathbf{x}$ and $\mathbf{y}$ is Gaussian with
$$
\begin{aligned}
p\left(\begin{matrix}
\mathbf{x} \\\\
\mathbf{y} 
\end{matrix}\right) = \mathcal{N}\left( \left(\begin{matrix}
\mathbf{x} \\\\
\mathbf{y} 
\end{matrix}\right) \bigg\vert \left(\begin{matrix}
\mathbf{m} \\\\
\mathbf{H}\mathbf{m}+\mathbf{u} 
\end{matrix}\right), \left(\begin{matrix}
\mathbf{P} & \mathbf{P}\mathbf{H}^T \\\\
\mathbf{H}\mathbf{P} & \mathbf{H}\mathbf{P}\mathbf{H}^T + \mathbf{R} 
\end{matrix}\right) \right).
\end{aligned}
$$

---

class: middle

If $\mathbf{x}$ and $\mathbf{y}$ have the joint Gaussian distribution 
$$
\begin{aligned}
p\left(\begin{matrix}
\mathbf{x} \\\\
\mathbf{y} 
\end{matrix}\right) = \mathcal{N}\left( \left(\begin{matrix}
\mathbf{x} \\\\
\mathbf{y} 
\end{matrix}\right) \bigg\vert \left(\begin{matrix}
\mathbf{a} \\\\
\mathbf{b} 
\end{matrix}\right), \left(\begin{matrix}
\mathbf{A} & \mathbf{C} \\\\
\mathbf{C}^T & \mathbf{B}
\end{matrix}\right) \right),
\end{aligned}
$$
then the marginal and conditional distributions of $\mathbf{x}$ and $\mathbf{y}$ are given by
$$
\begin{aligned}
p(\mathbf{x}) &= \mathcal{N}(\mathbf{x}|\mathbf{a}, \mathbf{A}) \\\\
p(\mathbf{y}) &= \mathcal{N}(\mathbf{y}|\mathbf{b}, \mathbf{B}) \\\\
p(\mathbf{x}|\mathbf{y}) &= \mathcal{N}(\mathbf{x}|\mathbf{a}+\mathbf{C}\mathbf{B}^{-1}(\mathbf{y}-\mathbf{b}), \mathbf{A}-\mathbf{C}\mathbf{B}^{-1}\mathbf{C}^T) \\\\
p(\mathbf{y}|\mathbf{x}) &= \mathcal{N}(\mathbf{y}|\mathbf{b}+\mathbf{C}^T\mathbf{A}^{-1}(\mathbf{x} - \mathbf{a}) , \mathbf{B}-\mathbf{C}^T\mathbf{A}^{-1}\mathbf{C}).
\end{aligned}
$$

---

# Continuous Bayes filter

The Bayes filter similarly applies to **continuous** state and evidence variables $\mathbf{X}\_{t}$ and $\mathbf{E}\_{t}$, in which case summations are replaced with integrals and probability mass functions with probability densities:
$$
\begin{aligned}
p(\mathbf{x}\_{t+1}| \mathbf{e}\_{1:t+1}) &\propto\, p(\mathbf{e}\_{t+1}| \mathbf{x}\_{t+1}) \int p(\mathbf{x}\_{t+1}|\mathbf{x}\_t) p(\mathbf{x}\_t | \mathbf{e}\_{1:t}) d{\mathbf{x}\_t}
\end{aligned}
$$
where the normalization constant is
$$\alpha = 1\, / \int p(\mathbf{e}\_{t+1} | \mathbf{x}\_{t+1}) p(\mathbf{x}\_{t+1} | \mathbf{e}\_{1:t}) d\mathbf{x}\_{t+1}.$$

---

# Kalman filter

The **Kalman filter** is a special case of the Bayes filter, which assumes:
- Gaussian prior
- Linear Gaussian transition model
- Linear Gaussian sensor model

.grid[
.kol-1-2.center[
<br><br><br>
![](figures/lec6/lg-model1.png)

$p(\mathbf{x}\_{t+1} | \mathbf{x}\_t) = \mathcal{N}(\mathbf{x}\_{t+1} | \mathbf{A} \mathbf{x}\_t + \mathbf{b}, \mathbf{\Sigma}\_{\mathbf{x}})$

Transition model

]
.kol-1-2.center[
![](figures/lec6/lg-model2.png)

$p(\mathbf{e}\_{t} | \mathbf{x}\_t) = \mathcal{N}(\mathbf{e}\_t | \mathbf{C} \mathbf{x}\_t + \mathbf{d}, \mathbf{\Sigma}\_{\mathbf{e}})$

Sensor model
]
]

---

class: middle

## Filtering Gaussian distributions

- .italic[Prediction step:]<br><br>
If the distribution $p(\mathbf{x}\_t | \mathbf{e}\_{1:t})$ is Gaussian and the transition model $p(\mathbf{x}\_{t+1} | \mathbf{x}\_{t})$ is linear Gaussian, then the one-step predicted distribution given by
$$p(\mathbf{x}\_{t+1} | \mathbf{e}\_{1:t}) = \int p(\mathbf{x}\_{t+1} | \mathbf{x}\_{t}) p(\mathbf{x}\_{t} | \mathbf{e}\_{1:t}) d\mathbf{x}\_t $$
is also a Gaussian distribution.
- .italic[Update step:]<br><br>
If the prediction $p(\mathbf{x}\_{t+1} | \mathbf{e}\_{1:t})$ is Gaussian and the sensor model $p(\mathbf{e}\_{t+1} | \mathbf{x}\_{t+1})$ is linear Gaussian, then after conditioning on new evidence, the updated distribution
$$p(\mathbf{x}\_{t+1} | \mathbf{e}\_{1:t+1}) = \alpha p(\mathbf{e}\_{t+1} | \mathbf{x}\_{t+1}) p(\mathbf{x}\_{t+1} | \mathbf{e}\_{1:t})$$
is also a Gaussian distribution.

---

class: middle

Therefore, for the Kalman filter,  $p(\mathbf{x}\_t | \mathbf{e}\_{1:t})$ is a multivariate Gaussian distribution $\mathcal{N}(\mathbf{x}\_t | \mathbf{\mu}\_t, \mathbf{\Sigma}\_t)$ for all $t$.

- Filtering reduces to the computation of the parameters $\mu_t$ and  $\mathbf{\Sigma}\_t$.
- By contrast, for general (non-linear, non-Gaussian) processes, the description of the posterior grows **unboundedly** as $t \to \infty$.

---

class: middle

## 1D example

Gaussian random walk:
- Gaussian prior: $$p(x\_0) = \mathcal{N}(x\_0 | \mu\_0, \sigma\_0^2) $$
- The transition model adds random perturbations of constant variance:
    $$p(x\_{t+1}|x\_t) =  \mathcal{N}(x\_{t+1}|x\_t, \sigma\_x^2)$$
- The sensor model yields measurements with Gaussian noise of constant variance:
    $$p(e\_{t}|x\_t) =  \mathcal{N}(e\_t | x\_t, \sigma\_e^2)$$

---

class: middle

The one-step predicted distribution is given by
$$
\begin{aligned}
p(x\_1) &= \int p(x\_1 | x\_0) p(x\_0) dx\_0 \\\\
&\propto \int \exp\left(-\frac{1}{2} \frac{(x\_{1} - x\_0)^2}{\sigma\_x^2}\right) \exp\left(-\frac{1}{2} \frac{(x\_0 - \mu\_0)^2}{\sigma\_0^2}\right) dx\_0 \\\\
&\propto \int \exp\left( -\frac{1}{2} \frac{\sigma\_0^2 (x\_1 - x\_0)^2 + \sigma\_x^2(x\_0 - \mu\_0)^2}{\sigma\_0^2 \sigma\_x^2} \right) dx\_0 \\\\
&... \,\, \text{(simplify by completing the square)} \\\\
&\propto \exp\left( -\frac{1}{2} \frac{(x\_1 - \mu\_0)^2}{\sigma\_0^2 + \sigma\_x^2} \right) \\\\
&= \mathcal{N}(x\_1 | \mu\_0, \sigma\_0^2 + \sigma\_x^2)
\end{aligned}
$$

Note that the same result can be obtained by using instead the Gaussian models identities.

---

class: middle

For the update step, we need to condition on the observation at the first time step:
$$
\begin{aligned}
p(x\_1 | e\_1) &\propto p(e\_1 | x\_1) p(x\_1) \\\\
&\propto \exp\left(-\frac{1}{2} \frac{(e\_{1} - x\_1)^2}{\sigma\_e^2}\right)  \exp\left( -\frac{1}{2} \frac{(x\_1 - \mu\_0)^2}{\sigma\_0^2 + \sigma\_x^2} \right) \\\\
&\propto \exp\left( -\frac{1}{2} \frac{\left(x\_1 - \frac{(\sigma\_0^2 + \sigma\_x^2) e\_1 + \sigma\_e^2 \mu\_0}{\sigma\_0^2 + \sigma\_x^2 + \sigma\_e^2}\right)^2}{\frac{(\sigma\_0^2 + \sigma\_x^2)\sigma\_e^2}{\sigma\_0^2 + \sigma\_x^2 + \sigma\_e^2}} \right) \\\\
&= \mathcal{N}\left(x\_1 \bigg\vert \frac{(\sigma\_0^2 + \sigma\_x^2) e\_1 + \sigma\_e^2 \mu\_0}{\sigma\_0^2 + \sigma\_x^2 + \sigma\_e^2}, \frac{(\sigma\_0^2 + \sigma\_x^2)\sigma\_e^2}{\sigma\_0^2 + \sigma\_x^2 + \sigma\_e^2}\right)
\end{aligned}
$$

---

class: middle

.center.width-70[![](figures/lec6/walk.png)]

In summary, the update equations given a new evidence $e\_{t+1}$ are:
$$
\begin{aligned}
\mu\_{t+1} &= \frac{(\sigma\_t^2 + \sigma\_x^2) e\_{t+1} + \sigma\_e^2 \mu\_t }{\sigma\_t^2 + \sigma\_x^2 + \sigma\_e^2} \\\\
\sigma\_{t+1}^2 &= \frac{(\sigma_t^2 + \sigma\_x^2) \sigma\_e^2}{\sigma\_t^2 + \sigma\_x^2 + \sigma\_e^2}
\end{aligned}
$$

???

We can interpret
the calculation for the new mean $\mu\_{t+1}$ as simply a weighted mean of the new observation
$e\_{t+1}$ and the old mean $\mu\_t$ .
- If the observation is unreliable, then $\sigma\_e^2$ is large and we pay more
attention to the old mean;
- If the observation is reliable, then we pay more attention to the evidence and less to the old mean.
- if the old mean is unreliable ($\sigma\_t^2$ is large) or the process is highly
unpredictable ($\sigma\_x^2$ is large), then we pay more attention to the observation

---

class: middle

## General Kalman update

The same derivations generalize to multivariate normal distributions.

Assuming the transition and sensor models
$$
\begin{aligned}
p(\mathbf{x}\_{t+1} | \mathbf{x}\_t) &= \mathcal{N}(\mathbf{x}\_{t+1} | \mathbf{F} \mathbf{x}\_t, \mathbf{\Sigma}\_{\mathbf{x}}) \\\\
p(\mathbf{e}\_{t} | \mathbf{x}\_t) &= \mathcal{N}(\mathbf{e}\_{t} | \mathbf{H} \mathbf{x}\_t, \mathbf{\Sigma}\_{\mathbf{e}}),
\end{aligned}
$$
we arrive at the following general update equations:
$$
\begin{aligned}
\mu\_{t+1} &= \mathbf{F}\mathbf{\mu}\_t + \mathbf{K}\_{t+1} (\mathbf{e}\_{t+1} - \mathbf{H} \mathbf{F} \mathbf{\mu}\_t) \\\\
\mathbf{\Sigma}\_{t+1} &= (\mathbf{I} - \mathbf{K}\_{t+1} \mathbf{H}) (\mathbf{F}\mathbf{\Sigma}\_t \mathbf{F}^T + \mathbf{\Sigma}\_x) \\\\
\mathbf{K}\_{t+1} &= (\mathbf{F}\mathbf{\Sigma}\_t \mathbf{F}^T + \mathbf{\Sigma}\_x) \mathbf{H}^T (\mathbf{H}(\mathbf{F}\mathbf{\Sigma}\_t \mathbf{F}^T + \mathbf{\Sigma}\_x)\mathbf{H}^T + \mathbf{\Sigma}\_e)^{-1}
\end{aligned}$$
where $\mathbf{K}\_{t+1}$ is the Kalman gain matrix.

???

Note that $\mathbf{\Sigma}\_{t+1}$ and $\mathbf{K}\_{t+1}$ are independent of the evidence. Therefore, they can be computed offline.

These equations intuitively make sense.

Consider
the update for the mean state estimate $\mu\_{t+1}$.
- The term  $\mathbf{F}\mathbf{\mu}\_t$ is the predicted state at $t + 1$,
- so
$\mathbf{H} \mathbf{F} \mathbf{\mu}\_t$ is the predicted observation.
- Therefore, the term $\mathbf{e}\_{t+1} - \mathbf{H} \mathbf{F} \mathbf{\mu}\_t$ represents the error in
the predicted observation.
- This is multiplied by $ \mathbf{K}\_{t+1}$ to correct the predicted state; hence,
$ \mathbf{K}\_{t+1}$ is a measure of how seriously to take the new observation relative to the prediction.

---

class: middle

## 2d tracking by filtering

.center.width-80[![](figures/lec6/kf-filtering.png)]

???

In this example, $\mathbf{X}$ includes the X-Y positions and the X-Y velocities.

---

class: middle, black-slide

## Apollo guidance computer

- The Kalman filter put man on the Moon, literally!
- The onboard guidance software of Saturn-V used a Kalman filter to merge new data with past position measurements to produce an optimal position estimate of the spacecraft.

.grid[
.kol-1-6[]
.kol-1-3[.width-100[![](figures/lec6/saturn-v.jpg)]]
.kol-1-3[.width-100[![](figures/lec6/agc.jpg)]]
]

.footnote[Credits: [Apollo-11 source code](https://github.com/chrislgarry/Apollo-11/blob/4f3a1d4374d4708737683bed78a501a321b6042c/Comanche055/MEASUREMENT_INCORPORATION.agc#L208)]

---

class: center, black-slide, middle

<iframe width="640" height="400" src="https://www.youtube.com/embed/aNzGCMRnvXQ?cc_load_policy=1&hl=en&version=3" frameborder="0" allowfullscreen></iframe>

---

class: middle, black-slide

## Data assimilation for weather forecasts solves a filtering problem

.center[
<iframe width="640" height="400" src="https://www.youtube.com/embed/9c4kXW7btBE?cc_load_policy=1&hl=en&version=3" frameborder="0" allowfullscreen></iframe>
]

---

# Dynamic Bayesian networks

.grid[
.kol-2-3[.center.width-100[![](figures/lec6/dbn-cartoon.png)]]
.kol-1-3[.center.width-80[![](figures/lec6/robot-dbn1.svg)]]
]

Dynamics Bayesian networks (DBNs) can be used for tracking multiple variables over time, using multiple sources of evidence. Idea:
- Repeat a fixed Bayes net structure at each time $t$.
- Variables from time $t$ condition on those from $t-1$.

DBNs are a generalization of HMMs and of the Kalman filter.

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

## Exact inference

.center.width-100[![](figures/lec6/dbn-unrolling.svg)]

Unroll the network through time and run any exact inference algorithm (e.g., variable elimination)
- Problem: inference cost for each update grows with $t$.
- Rollup filtering: add slice $t+1$, sum out slice $t$ using variable elimination.
    - Largest factor is $O(d^{n+k})$ and the total update cost per step is $O(nd^{n+k})$.
    - Better than HMMs, which is $O(d^{2n})$, but still **infeasible** for large numbers of variables.

---

class: middle

## Approximate inference

If exact inference in DBNs intractable, then let's use *approximate inference* instead.
- Likelihood weighting? Generated samples **pay no attention** to the evidence!
- The fraction of samples that remain close to the actual series of events drops exponentially with $t$.

$\Rightarrow$ We need a better solution!

---

# Particle filter

 Basic idea:
- Maintain a finite population of samples, called **particles**.
    - The representation of our beliefs is a list of $N$ particles.
- Ensure the particles track the high-likelihood regions of the
state space.
- Throw away samples that have very low weight, according to the evidence.
- Replicate those that have high weight.

This scales to high dimensions!

.center.width-50[![](figures/lec6/robot.png)]

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

## Update cycle

.center.width-100[![](figures/lec6/particle-filter.png)]

.footnote[Image credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

.center.width-100[![](figures/lec6/pf-algorithm.png)]

---

class: middle

## Robot localization

.center.width-70[![](figures/lec6/pf-demo.png)]

.center[(See demo)]

---

class: middle, black-slide, center

.width-50[![](figures/lec6/ragi.jpg)]

The RAGI robot makes use of a particle filter to locate itself within Montefiore.<br>
(See [RTBF, mars 2019](https://www.rtbf.be/info/regions/liege/detail_liege-l-intelligence-artificielle-vous-accueille-a-l-universite?id=10183022).)

---

class: middle

.width-100[![](figures/lec6/ragi-localization.png)]

.footnote[Credits: Tom Ewbank, RAGI.]

---

# Summary

- Temporal models use state and sensor variables replicated over time.
    - Their purpose is to maintain a belief state as time passes and as more evidence is collected.
- The Markov and stationarity assumptions imply that we only need to specify
    - a transition model ${\bf P}(\mathbf{X}\_{t+1} | \mathbf{X}\_t)$,
    - a sensor model ${\bf P}(\mathbf{E}\_t | \mathbf{X}\_t)$.
- Inference tasks include filtering, prediction, smoothing and finding the most likely sequence.
- Filter algorithms are all based on the core of idea of
    - projecting the current belief state through the transition model,
    - updating the prediction according to the new evidence.

---

class: end-slide, center
count: false

The end.
