class: middle, center, title-slide

# Introduction to Artificial Intelligence

Lecture 7: Reasoning over time

---

# Today

- *Markov models*
    - Markov processes
    - Inference tasks
        - Prediction
        - Filtering
        - Smoothing
        - Most likely explanation
    - Hidden Markov models
- *Filtering*
    - Kalman filter
    - Dynamic Bayesian networks
    - Particle filters

---

# Pacman revenge

.center[
<video controls preload="auto" height="400" width="640">
  <source src="./figures/lec7/pacman-no-beliefs.mp4" type="video/mp4">
</video>]

<span class="Q">[Q]</span> How to make good use of the sonar readings?

.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

---

class: middle, center

# Markov models

---

# Reasoning over time or space

- Often, we want to **reason about a sequence** of observations.
    - Speech recognition
    - Robot localization
    - User attention
    - Medical monitoring.
- Therefore, we need to introduce **time** (or *space*) in our model.
- Consider the world as a *discrete* series of *time slices*, each of which contains a set of random variables.
    - $\mathbf{X}\_t$ denotes the set of **unobservable** state variables at time $t$.
    - $\mathbf{E}\_t$ denotes the set of *observable* evidence variables at time $t$.
- We specify a **transition model** $P(\mathbf{X}\_t | \mathbf{X}\_{0:t-1})$ that defines the probability distribution over the latest state variables, given the previous values.
- Similarly, we define a **sensor model** $P(\mathbf{E}\_t | \mathbf{X}\_{0:t}, \mathbf{E}\_{0:t-1})$.

---

# Markov processes (1)

- **Markov assumption**: $\mathbf{X}\_t$ depends on only a bounded subset of $\mathbf{X}\_{0:t-1}$.
    - Processes that satisfy this assumption are called **Markov processes** or **Markov chains**.
- *First-order* Markov processes: $P(\mathbf{X}\_t | \mathbf{X}\_{0:t-1}) = P(\mathbf{X}\_t | \mathbf{X}\_{t-1})$.
    - i.e., $\mathbf{X}\_t$ and $\mathbf{X}\_{0:t-2}$ are conditionally independent given $\mathbf{X}\_{t-1}$.
- *Second-order* Markov processes: $P(\mathbf{X}\_t | \mathbf{X}\_{0:t-1}) = P(\mathbf{X}\_t | \mathbf{X}\_{t-2}, \mathbf{X}\_{t-1})$.

<br><br>
.center.width-100[![](figures/lec7/markov-process.png)]

---

# Markov processes (2)

- Additionally, we make a **sensor Markov assumption**: $P(\mathbf{E}\_t | \mathbf{X}\_{0:t}, \mathbf{E}\_{0:t-1}) = P(\mathbf{E}\_t | \mathbf{X}\_{t})$
- *Stationary* process: the transition and the sensor models are the same for all $t$ (i.e., the laws of physics do not change with time).

---

# Joint distribution

.center.width-70[![](figures/lec7/markov-process-generic.png)]

- A Markov process can be described as a *growable* Bayesian network, unrolled through time, with a specified restricted structure between time steps.
    - i.e., we can use standard Bayesian network reasoning when truncating the sequence.
- Therefore, the *joint distribution* of all variables up to $t$ in a (first-order) Markov process is:
    $$P(\mathbf{X}\_{0:t}, \mathbf{E}\_{1:t}) = P(\mathbf{X}\_{0}) \prod\_{i=1}^t P(\mathbf{X}\_{i} | \mathbf{X}\_{i-1}) P(\mathbf{E}\_{i}|\mathbf{X}\_{i}) $$

---

# Example: Weather

.center.width-80[![](figures/lec7/weather-bn.png)]
.grid[
.col-2-3[
- $P(Umbrella\_t | Rain\_t)$?
- $P(Rain\\\_t | Umbrella\\\_{0:t-1})$?
- $P(Rain\\\_{t+2} | Rain\\\_{t})$?
]
.col-1-3.center[
![](figures/lec7/weather-transition.png)
Transition model $P(Rain\\\_t | Rain\\\_{t-1})$]]
<span class="Q">[Q]</span> How else can you represent the transition model?

---

# Inference tasks

- *Filtering*: $P(\mathbf{X}\_{t}| \mathbf{e}\_{1:t})$
    - Filtering is what a rational agent does to keep track of the current state (its **belief state**), so that rational decisions can be made.
- *Prediction*: $P(\mathbf{X}\_{t+k}| \mathbf{e}\_{1:t})$ for $k>0$
    - Computing the posterior distribution over future states.
    - Used for evaluation of possible action sequences.
- *Smoothing*: $P(\mathbf{X}\_{k}| \mathbf{e}\_{1:t})$ for $0 \leq k < t$
    - Computing the posterior distribution over past states.
    - Used for building better estimates, since it incorporates more evidence.
    - Essential for learning.    
- *Most likely explanation*: $\arg \max\_{\mathbf{x}\_{1:t}} P(\mathbf{x}\_{1:t}| \mathbf{e}\_{1:t})$
    - Decoding with a noisy channel, speech recognition, etc.

---

# Prediction

.center.width-100[![](figures/lec7/prediction.png)]

<br>

- To predict the future, the current *belief state* $P(\mathbf{X}\_{t} | \mathbf{e}\_{1:t})$ get *pushed* through the transition model.
$$P(\mathbf{X}\_{t+1}| \mathbf{e}\_{1:t}) = \sum\_{\mathbf{x}\_{t}} P(\mathbf{X}\_{t+1} | \mathbf{x}\_{t}) P(\mathbf{x}\_{t} | \mathbf{e}\_{1:t})$$
- As time passes, uncertainty "accumulates" if we do not accumulate new evidence.

---

# Ghostbusters: Basic dynamics

.center[
<video controls preload="auto" height="400" width="640">
  <source src="./figures/lec7/gb-basics.mp4" type="video/mp4">
</video>]

.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

---

# Ghostbusters: Circular dynamics

.center[
<video controls preload="auto" height="400" width="640">
  <source src="./figures/lec7/gb-circular.mp4" type="video/mp4">
</video>]

.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

---

# Ghostbusters: Whirlpool

.center[
<video controls preload="auto" height="400" width="640">
  <source src="./figures/lec7/gb-whirlpool.mp4" type="video/mp4">
</video>]

.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

---

# Stationary distributions

What if $t \to \infty$?
- For most chains, the influence of the initial distribution gets less and less over time.
- Eventually, the distribution converges to a fixed point, called the **stationary distribution**.
- It satisfies:
$$P(\mathbf{X}\_\infty) = P(\mathbf{X}\_{\infty+1}) = \sum\_{\mathbf{x}\_\infty} P(\mathbf{X}\_{\infty+1} | \mathbf{x}\_\infty) P(\mathbf{x}\_\infty) $$

---

# Example

.width-50.center[![](figures/lec7/stationary.png)]

.grid[
.col-3-4[
$P(\mathbf{X}\_\infty = sun) = P(\mathbf{X}\_{\infty+1} = sun)$<br>
$\quad = P(\mathbf{X}\_{\infty+1}=sun | \mathbf{X}\_{\infty}=sun) P(\mathbf{X}\_{\infty}=sun)$<br> $\quad\quad + P(\mathbf{X}\_{\infty+1}=sun | \mathbf{X}\_{\infty}=rain) P(\mathbf{X}\_{\infty}=rain)$<br>
$\quad = 0.9 P(\mathbf{X}\_{\infty}=sun) + 0.3 P(\mathbf{X}\_{\infty}=rain)$

Therefore, $P(\mathbf{X}\_\infty = sun) = 3 P(\mathbf{X}\_\infty = rain)$

Which implies that:<br>
$P(\mathbf{X}\_\infty = sun) = \frac{3}{4}$<br>
$P(\mathbf{X}\_\infty = rain) = \frac{1}{4}$

]
.col-1-4[

.center[
| $\mathbf{X}\_{t-1}$ | $\mathbf{X}\_{t}$ | $P$ |
| --- | --- | --- |
| $sun$ | $sun$ | 0.9 |
| $sun$ | $rain$ | 0.1 |
| $rain$ | $sun$ | 0.3 |
| $rain$ | $rain$ | 0.7 |
]

<br><br><br>

![](figures/lec7/stationary-cartoon.png)

]
]

.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

---

# Observation

.center.width-70[![](figures/lec7/observation.png)]

<br>

- What if we collect new observations?
- Beliefs get *reweighted*, and uncertainty "decreases".

$$P(\mathbf{X}\_{t+1}| \mathbf{e}\_{1:t+1}) = \alpha P(\mathbf{e}\_{t+1} | \mathbf{X}\_{t+1}) P(\mathbf{X}\_{t+1} | \mathbf{e}\_{1:t})$$

---

# Filtering (1)

- An agent should maintain a current *belief state* estimate $P(\mathbf{X}\_{t}| \mathbf{e}\_{1:t})$ and update it as new evidences $\mathbf{e}\_{t+1}$ are collected.
    - Rather than going back over the entire history of percepts for each update.
- **Recursive estimation**: $P(\mathbf{X}\_{t+1}| \mathbf{e}\_{1:t+1}) = f(\mathbf{e}\_{t+1}, P(\mathbf{X}\_{t}| \mathbf{e}\_{1:t}))$
    - Project the current state belief forward from $t$ to $t+1$
    - Update this new state using the evidence $\mathbf{e}\_{t+1}$.

<hr>

$P(\mathbf{X}\_{t+1}| \mathbf{e}\_{1:t+1}) = P(\mathbf{X}\_{t+1}| \mathbf{e}\_{1:t}, \mathbf{e}\_{t+1})$<br>
$\quad = \alpha P(\mathbf{e}\_{t+1}| \mathbf{X}\_{t+1}, \mathbf{e}\_{1:t}) P(\mathbf{X}\_{t+1}| \mathbf{e}\_{1:t}) \quad $<br>
$\quad = \alpha P(\mathbf{e}\_{t+1}| \mathbf{X}\_{t+1}) P(\mathbf{X}\_{t+1}| \mathbf{e}\_{1:t})$<br>
$\quad = \alpha P(\mathbf{e}\_{t+1}| \mathbf{X}\_{t+1}) \sum\_{\mathbf{x}\_t} P(\mathbf{X}\_{t+1}|\mathbf{x}\_t, \mathbf{e}\_{1:t}) P(\mathbf{x}\_t | \mathbf{e}\_{1:t}) $<br>
$\quad = \alpha P(\mathbf{e}\_{t+1}| \mathbf{X}\_{t+1}) \sum\_{\mathbf{x}\_t} P(\mathbf{X}\_{t+1}|\mathbf{x}\_t) P(\mathbf{x}\_t | \mathbf{e}\_{1:t}) $

The first and second terms are given by the model. The third is obtained recursively.

---

# Filtering (2)

- We can think of $P(\mathbf{X}\_t | \mathbf{e}\_{1:t})$ as a *message* $\mathbf{f}\_{1:t}$ that is propagated **forward** along the sequence, modified by each transition and updated by each new observation.
- Thus, the process can be implemented as $\mathbf{f}\_{1:t+1} = \alpha\, \text{forward}(\mathbf{f}\_{1:t}, \mathbf{e}\_{t+1} )$.
- The complexity of a forward update is constant (in time and space) with $t$.

<br><br><br><br><br><br><br><br>

<span class="Q">[Q]</span> What is the explicit form of the normalization constant $\alpha$?

---

# Example

.center.width-80[![](figures/lec7/filtering.png)]

---

# Smoothing

Divide evidence $\mathbf{e}\_{1:t}$ into $\mathbf{e}\_{1:k}$ and $\mathbf{e}\_{k+1:t}$. Then:

$P(\mathbf{X}\_k | \mathbf{e}\_{1:t}) = P(\mathbf{X}\_k | \mathbf{e}\_{1:k}, \mathbf{e}\_{k+1:t})$<br>
$\quad = \alpha P(\mathbf{X}\_k | \mathbf{e}\_{1:k}) P(\mathbf{e}\_{k+1:t} | \mathbf{X}\_k, \mathbf{e}\_{1:k})$<br>
$\quad = \alpha P(\mathbf{X}\_k | \mathbf{e}\_{1:k}) P(\mathbf{e}\_{k+1:t} | \mathbf{X}\_k)$<br>
$\quad = \alpha\, \mathbf{f}\_{1:k} \mathbf{b}\_{k+1:t}$

The **backward** message $\mathbf{b}\_{k+1:t}$ can be computed using backwards recursion:

$P(\mathbf{e}\_{k+1:t} | \mathbf{X}\_k) = \sum\_{\mathbf{x}\_{k+1}} P(\mathbf{e}\_{k+1:t} | \mathbf{X}\_k, \mathbf{x}\_{k+1}) P(\mathbf{x}\_{k+1} | \mathbf{X}\_k) $<br>
$\quad = \sum\_{\mathbf{x}\_{k+1}} P(\mathbf{e}\_{k+1:t} | \mathbf{x}\_{k+1}) P(\mathbf{x}\_{k+1} | \mathbf{X}\_k) $<br>
$\quad = \sum\_{\mathbf{x}\_{k+1}} P(\mathbf{e}\_{k+1} | \mathbf{x}\_{k+1}) P(\mathbf{e}\_{k+2:t} | \mathbf{x}\_{k+1}) P(\mathbf{x}\_{k+1} | \mathbf{X}\_k)$

The first and last factors are given by the model. The second factor is obtained recursively. Therefore,

$\mathbf{b}\_{k+1:t} = \text{backward}(\mathbf{b}\_{k+2:t}, \mathbf{e}\_{k+1} )$.

---

# Forward-backward algorithm

.center.width-100[![](figures/lec7/forward-backward.png)]

Complexity:
- Smoothing for a particular time step $k$ takes: $O(t)$
- Smoothing a whole sequence, naively: $O(t^2)$
- Smoothing a whole sequence, by caching messages:  $O(t)$

---

# Example

.center.width-80[![](figures/lec7/smoothing.png)]

---

# Most likely explanation

- The most likely sequence  **is not** the sequence of most likely states!
- The most likely path to each $\mathbf{x}\_{t+1}$, is the most likely path to *some* $\mathbf{x}\_t$ plus one more step. Therefore,
<br><br>
$\max\_{\mathbf{x}\_{1:t}} P(\mathbf{x}\_{1:t}, \mathbf{X}\_{t+1} | \mathbf{e}\_{1:t+1})$<br>
$\quad = \alpha P(\mathbf{e}\_{t+1}|\mathbf{X}\_{t+1}) \max\_{\mathbf{x}\_t}( P(\mathbf{X}\_{t+1} | \mathbf{x}\_t) \max\_{\mathbf{x}\_{1:t-1}} P(\mathbf{x}\_{1:t-1}, \mathbf{x}\_{t} | \mathbf{e}\_{1:t}) )$
- Identical to filtering, except that the forward message $\mathbf{f}\_{1:t} = P(\mathbf{X}\_t | \mathbf{e}\_{1:t})$ is replaced by:
<br><br>
$\mathbf{m}\_{1:t} = \max\_{\mathbf{x}\_{1:t-1}} P(\mathbf{x}\_{1:t-1}, \mathbf{X}\_{t} | \mathbf{e}\_{1:t})$<br><br>
i.e., $\mathbf{m}\_{1:t}(i)$ gives the probability of the most likely path to state $i$.
- The update has its sum replaced by max, giving the **Viterbi algorithm**:
<br><br>
$\mathbf{m}\_{1:t+1} = \alpha P(\mathbf{e}\_{t+1} | \mathbf{X}\_{t+1}) \max\_{\mathbf{x}\_{1:t}} P(\mathbf{X}\_{t+1} | \mathbf{x}\_{t}) \mathbf{m}\_{1:t}$

---

# Example

.center.width-90[![](figures/lec7/viterbi.png)]

<span class="Q">[Q]</span> How do you retrieve the path, in addition to its likelihood?

---

# Hidden Markov models

- So far, we described Markov processes over arbitrary sets of state variables $\mathbf{X}\_t$ and evidence variables $\mathbf{E}\_t$.
- A **hidden Markov model** (HMM) is a Markov process in which the state $\mathbf{X}\_t$ and the evidence $\mathbf{E}\_t$ are both *single discrete* random variables.
    - i.e., $\mathbf{X}\_t = X\_t$, with domain $\\\{1, ..., S\\\}$.
- This restricted structure allows for a simple *matrix implementation* of the inference algorithms.

---

# Simplified matrix algorithms

- The transition model $P(X\_t | X\_{t-1})$ becomes an $S \times S$ *transition matrix* $\mathbf{T}$, where $\mathbf{T}\_{ij} = P(X\_t=j | X\_{t-1}=i)$.
- The sensor model $P(E\_t | X\_t)$ is defined, for convenience, as an  $S \times S$ *sensor matrix*
$\mathbf{O}\_t$ whose $i$-th diagonal element is $P(e\_t | X\_t = i)$ and whose other entries are 0.
- If we use column vectors to represent forward and backward messages, then we have:
$$\mathbf{f}\_{1:t+1} = \alpha \mathbf{O}\_{t+1} \mathbf{T}^T \mathbf{f}\_{1:t}$$
$$\mathbf{b}\_{k+1:t} = \mathbf{T} \mathbf{O}\_{k+1} \mathbf{b}\_{k+2:t}$$
- Therefore the forward-backward algorithm needs time $O(S^2t)$ and space $O(St)$.

---

# Applications

HMMs can be applied in many fields where the goal is to recover a data sequence that is not immediately observable, but other data data that depend on the sequence are.

- Computational finance
- **Speech recognition**
- Speech synthesis
- Part-of-speech tagging
- Machine translation
- Handwriting recognition
- Time series analysis
- Activity recognition
- ...

---

# Pacman, revisited

.center[
<video controls preload="auto" height="400" width="640">
  <source src="./figures/lec7/pacman-with-beliefs.mp4" type="video/mp4">
</video>]

.footnote[Credits: UC Berkeley, [CS188](http://ai.berkeley.edu/lecture_slides.html)]

---

class: middle, center

# Filters

---

# Continuous state variables

- From noisy observations collected over time, we want to estimate **continuous** state variables, e.g.
    - position $\mathbf{X}\_t$,
    - velocity $\mathbf{\dot{X}}\_t$.
- Applications:
    - tracking
    - robots
    - guidance
    - planet motion
    - financial time series
    - ...

<br><br><br>

<span class="Q">[Q]</span> How can we model this system to make filtering efficient and accurate?

---

# Kalman filters

.center.width-50[![](figures/lec7/kalman-network.png)]

A **Kalman filter** assumes:
- Gaussian prior
- Linear Gaussian transition model
- Linear Gaussian sensor model

---

# Updating Gaussian distributions

- *Prediction step*:
    - If $P(\mathbf{X}\_t | \mathbf{e}\_{1:t})$ is Gaussian and the transition model $P(\mathbf{X}\_{t+1} | \mathbf{x}\_{t})$ is linear Gaussian, then
$$P(\mathbf{X}\_{t+1} | \mathbf{e}\_{1:t}) = \int\_{\mathbf{x}\_t} P(\mathbf{X}\_{t+1} | \mathbf{x}\_{t}) P(\mathbf{x}\_{t} | \mathbf{e}\_{1:t}) d\mathbf{x}\_t $$
is Gaussian.
- *Update step*:
    - If $P(\mathbf{X}\_{t+1} | \mathbf{e}\_{1:t})$ is Gaussian and the sensor model $P(\mathbf{e}\_{t+1} | \mathbf{X}\_{t+1})$ is linear Gaussian, then
$$P(\mathbf{X}\_{t+1} | \mathbf{e}\_{1:t+1}) = \alpha P(\mathbf{e}\_{t+1} | \mathbf{X}\_{t+1}) P(\mathbf{X}\_{t+1} | \mathbf{e}\_{1:t})$$
is also Gaussian.
- Hence, for a Kalman filter, $P(\mathbf{X}\_t | \mathbf{e}\_{1:t})$ is a multivariate Gaussian $\mathcal{N}(\mathbf{\mu}\_t, \mathbf{\Sigma}\_t)$ for all $t$.
- General (nonlinear, non-Gaussian) process: the description of the posterior grows **unboundedly** as $t \to \infty$.

---

# 1D example

- Gaussian random walk on $X$-axis:
    - Gaussian prior with variance $\sigma_0^2$.
    - The transition model adds random perturbations of constant variance $\sigma\_x^2$.
    - The sensor model yields measurements with Gaussian noise with variance $\sigma\_z^2$.
- Then the update equations given a new evidence $z\_{t+1}$ are:
    - $\mu\_{t+1} = \frac{(\sigma\_t^2 + \sigma\_x^2) z\_{t+1} + \sigma\_z^2 \mu_t }{\sigma\_t^2 + \sigma\_x^2 + \sigma\_z^2}$
    - $\sigma\_{t+1}^2 = \frac{(\sigma_t^2 + \sigma\_x^2) \sigma\_z^2}{\sigma\_t^2 + \sigma\_x^2 + \sigma\_z^2}$

.center.width-40[![](figures/lec7/1d-kalman.png)]

???

Add intuition pg 587

---

# General Kalman update

- Transition and sensor models:
    - $P(\mathbf{x}\_{t+1} | \mathbf{x}\_t) = \mathcal{N}(\mathbf{F}\mathbf{x}\_t, \mathbf{\Sigma}\_x)(\mathbf{x}\_{t+1})$
    - $P(\mathbf{z}\_{t} | \mathbf{x}\_t) = \mathcal{N}(\mathbf{H}\mathbf{x}\_t, \mathbf{\Sigma}\_z)(\mathbf{z}\_{t})$
- $\mathbf{F}$ and $\mathbf{\Sigma}\_x$  are matrices describing the linear transition model and transition noise covariance.
- $\mathbf{H}$ and $\mathbf{\Sigma}\_z$ are the corresponding matrices for the sensor model.
- The filter computes the following update:
    - $\mu\_{t+1} = \mathbf{F}\mathbf{\mu}\_t + \mathbf{K}\_{t+1} (\mathbf{z}\_{t+1} - \mathbf{H} \mathbf{F} \mathbf{\mu}\_t)$
    - $\mathbf{\Sigma}\_{t+1} = (\mathbf{I} - \mathbf{K}\_{t+1} \mathbf{H}) (\mathbf{F}\mathbf{\Sigma}\_t \mathbf{F}^T + \mathbf{\Sigma}\_x)$
        - where $\mathbf{K}\_{t+1} = (\mathbf{F}\mathbf{\Sigma}\_t \mathbf{F}^T + \mathbf{\Sigma}\_x) \mathbf{H}^T (\mathbf{H}(\mathbf{F}\mathbf{\Sigma}\_t \mathbf{F}^T + \mathbf{\Sigma}\_x)\mathbf{H}^T + \mathbf{\Sigma}\_z)^{-1}$ is the *Kalman gain matrix*.
- Note that $\mathbf{\Sigma}\_t$ and $\mathbf{K}\_t$ are independent of the evidence. Therefore, they can be computed offline.

???

Add intuition pg 588

---

# 2D tracking: filtering

.center.width-80[![](figures/lec7/kf-filtering.png)]

---

# 2D tracking: smoothing

.center.width-80[![](figures/lec7/kf-smoothing.png)]

---

# Apollo Guidance Computer

.grid[
.col-3-4[
- The **onboard guidance software** of Saturn-V used a *Kalman filter*.
- Goal: merge new data with past position measurements to produce an optimal position estimate of the spacecraft.
]
.col-1-4[
![](figures/lec7/agc.jpg)]
]
.center.width-50[![](figures/lec7/kf-agc.png)]

.footnote[Credits: [Apollo-11 source code](https://github.com/chrislgarry/Apollo-11/blob/4f3a1d4374d4708737683bed78a501a321b6042c/Comanche055/MEASUREMENT_INCORPORATION.agc#L208)]

---

# Limitations

- The Kalman filter cannot be applied if the transition model is **non-linear**.
- The *Extended Kalman Filter* models transition as locally linear around $\mathbf{x}\_t = \mu\_t$.
    - Still fails if the system is locally unsmooth.

.grid[
.col-1-2[![](figures/lec7/kf-bird1.png)]
.col-1-2[![](figures/lec7/kf-bird2.png)]
]

---

# Dynamic Bayesian networks


---

# DBNs vs HMMs

---

# DBNs vs Kalman filters

---

# Exact inference in DBNs

---

# Particle filtering

---

# Summary

---

# References
