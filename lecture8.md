class: middle, center, title-slide

# Introduction to Artificial Intelligence

Lecture 8: Learning

---

# Today

- *Learning*
- *Statistical learning*
- *Supervised learning*
- *Reinforcement learning*
- *Unsupervised learning*

---

# Intelligence?

- What we covered so far...
    - Search algorithms, using a model specified by domain knowledge.
    - Adversarial search, for known fully observable games.
    - Constraint satisfaction problems, by exploiting a known structure of the states.
    - Logical inference, using well-specified facts and inference rules.
    - Reasoning about uncertain knowledge, as represented using domain-motivated graphs.
- Enough to implement complex and rational behaviors, *in some situations*.
- But is that **intelligence**?
- Aren't we missing a distinctive feature of intelligence?

---

# Chomsky vs. Piaget

.grid[
.col-2-3[
- *Noam Chomsky* (innatism):
    - State that humans possess a genetically determined faculty for thought and language.
    - The structures of language and thought are set in motion through interaction with the environment.
- *Jean Piaget* (constructivism):
    - Deny the existence of innate cognitive structure specific for thought and language.
    - Postulate instead all cognitive acquisitions, including language, to be the outcome of a gradual process of construction, i.e., a learning procedure.
]
.col-1-3[![](figures/lec8/piaget-chomsky.jpg)]
]


<span class="Q">[Q]</span> What about AI? Should it be a pre-wired efficient machine? Or a machine that can learn and improve? or maybe a bit of both?

---

# The debate continues...

.center[
<iframe width="640" height="480" src="https://www.youtube.com/embed/aCCotxqxFsk?&loop=1&start=0" frameborder="0" volume="0" allowfullscreen></iframe>
]

---

# Learning

- What if the environment is *unknown*?
- **Learning** can be use a system construction method.
    - i.e., expose the agent to reality rather trying to hardcode reality into the agent's program.
- Learning can be used as an *automated way* to modify the agent's decision mechanisms to improve performance.

---

# Learning agents

.center.width-100[![](figures/lec8/learning-agent.png)]

---

# Learning element

- The design of the **learning element** is dictated by:
    - What type of performance element is used.
    - Which functional component is to be learned.
    - How that functional component is represented.
    - What kind of feedback is available.
- Examples:    

.center.width-70[![](figures/lec8/table-components.png)]
- The nature and frequency of the feedback often determines a learning strategy:
    - *Supervised learning*: correct answer for each instance.
    - *Reinforcement learning*: occasional rewards.
    - *Unsupervised learning*: no feedback!

---

class: middle, center,

# Statistical learning

---

# Bayesian learning

---

# Learning with complete data

---

# Learning with hidden variables

---

class: middle, center,

# Supervised learning

---

# Supervised learning

---

# Feature vectors

---

# Linear classifiers

---

# Binary decision rules

---

# Perceptron

---

# Multiclass decision rules

---

# Properties of perceptrons

---

# Apprenticeship

---

# Multi-layer perceptron

---

# Backpropagation

---

# Deep Learning

compositional
demo pliage
apprentissage de concepts non-programmés

---

class: middle, center

# Reinforcement learning

---

# Reinforcement learning

learning by interaction

---

class: middle, center

# Unsupervised learning

---

# Unsupervised learning

learning by observation

---

# Summary

---

# References
