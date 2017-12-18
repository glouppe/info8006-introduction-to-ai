class: middle, center, title-slide

# Introduction to Artificial Intelligence

Lecture 10: Artificial General Intelligence

---

# From technological breakthroughs...

.center.width-100[![](figures/lec10/ai-in-news.png)]

---

# ... to popular media

.grid[
.col-1-4[![](figures/lec10/news1.png)]
.col-1-4[![](figures/lec10/news2.png)]
.col-1-4[![](figures/lec10/news3.png)]
.col-1-4[![](figures/lec10/news4.png)]
]
.grid[
.col-1-4[![](figures/lec10/news5.png)]
.col-1-4[![](figures/lec10/news6.png)]
.col-1-4[![](figures/lec10/news7.png)]
.col-1-4[![](figures/lec10/news8.png)]
]
.grid[
.col-1-4[![](figures/lec10/news11.png)]
.col-1-4[![](figures/lec10/news9.png)]
.col-1-4[![](figures/lec10/news10.png)]
.col-1-4[![](figures/lec10/news12.png)]
]

---

# Singularity

Irving John Good (1965):

- Let an **ultraintelligent** machine be defined as a machine that can far surpass all the intellectual activities of any man however clever.
- Since the design of machines is one of these intellectual activities, an ultraintelligent machine could *design even better machines*.
- There would then unquestionably be an **'intelligence explosion'**, and the intelligence of man would be left far behind.
- Thus the first ultraintelligent machine is the *last invention* that man need ever make, provided that the machine is docile enough to tell us how to keep it under control.

---

# Artificial narrow intelligence

- Artificial intelligence today is still very **narrow**.
    - Modern AI systems often reach super-human level performance.
    - ... but only at very specific problems!
    - They do not generalize to the real world nor to arbitrary tasks.

---

# AlphaGo

Convenient properties of AlphaGo:
- *Deterministic* (no noise in the game).
- *Fully observed* (each player has complete information)
- *Discrete action space* (finite number of actions possible)
- *Perfect simulator* (the effect of any action is known exactly)
- *Short episodes* (200 actions per game)
- *Clear and fast evaluation* (as stated by Go rules)
- *Huge dataset available* (games)

.center.width-40[![](figures/lec10/go.png)]

---

# Picking challenge

.center.width-100[![](figures/lec10/picking.png)]

.center[Can we run AlphaGo on a robot for the Amazon Picking Challenge?]

---

class: middle

- *Deterministic*: OK
- *Fully observed*: **OKish**
- *Discrete action space*: OK
- *Perfect simulator*: **TROUBLE**
- *Short episodes*: **challenge**
- *Clear and fast evaluation*: not good
- *Huge dataset available*: **challenge**

---

# Where could AGI come from?

- *Supervised learning*: "It works, just scale up!"
- *Unsupervised learning*: "It will work, if we only scale up!"
- *AIXI*: "Guys, I can write down optimal AI."
- *Brain simulation*: "This will work one day, right?"
- *Artificial life*: "Let just do what Nature did."

---

# Supervised learning

---

# Unsupervised learning

---

# AIXI

---

# Brain simulation

---

# Artificial Life

---

# Something else?

---

# Further readings

- Add ref to Karpathy's slides
- Bostrom book
