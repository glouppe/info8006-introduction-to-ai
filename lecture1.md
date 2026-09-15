class: middle, center, title-slide

# Introduction to Artificial Intelligence

Lecture 1: Intelligent agents

<br><br>
Prof. Gilles Louppe<br>
[g.louppe@uliege.be](mailto:g.louppe@uliege.be)

---

class: middle

# Intelligent agents

---

# Agents and environments

<br><br><br>

.grid[
.kol-1-5.center[
<br><br><br>
Percepts $e$
]
.kol-3-5.center[
.width-95[![](figures/lec1/loop.svg)]
]
.kol-1-5[
<br><br><br>
Actions $a$
]
]

---

class: middle

## Agents

- An agent is an entity that .bold[perceives] its environment through sensors and takes .bold[actions] through actuators.

- At each time step $t$, the agent receives a percept ${e\_t \in \mathcal{P}}$ and takes an action ${a\_t \in \mathcal{A}}$, where $\mathcal{P}$ and $\mathcal{A}$ are the sets of possible percepts and actions.

- The agent's behavior is described by its .bold[policy] ${\pi : \mathcal{P}^\* \to \mathcal{A}}$, which maps the percept sequence to the next action, $$a\_t = \pi(e\_{1:t}),$$ where ${e\_{1:t} = (e\_1, \ldots, e\_t)}$ and $\mathcal{P}^\*$ is the set of all finite percept sequences.

---

class: middle

## Simplified Pacman world

.width-20.center[![](figures/lec1/pacman.png)]

Let us consider a 2-cell world with a Pacman agent.
- Percepts: ${\mathcal{P} = \\{\text{left cell}, \text{right cell}\\} \times \\{\text{food}, \text{no food}\\}}$, the location of Pacman and the content of its cell, e.g. ${e\_1 = (\text{left cell}, \text{no food})}$.
- Actions: ${\mathcal{A} = \\{\text{go left}, \text{go right}, \text{eat}, \text{do nothing}\\}}$.

???

Take the time to explain that the game is here different from the actual Pacman.

---

class: middle

The .bold[policy] $\pi$ of a Pacman agent maps percept sequences ${e\_{1:t} \in \mathcal{P}^\*}$ to actions ${a\_t \in \mathcal{A}}$. It can be implemented as a table.

| Percept sequence $e\_{1:t}$ | Action $a\_t = \pi(e\_{1:t})$ |
| ---------------- | ------ |
| $(\text{left cell}, \text{no food})$     | $\text{go right}$ |
| $(\text{left cell}, \text{food})$     | $\text{eat}$ |
| $(\text{right cell}, \text{no food})$     | $\text{go left}$ |
| $(\text{right cell}, \text{food})$     | $\text{eat}$ |
| $(\text{left cell}, \text{no food}), (\text{left cell}, \text{no food})$     | $\text{go right}$ |
| $(\text{left cell}, \text{no food}), (\text{left cell}, \text{food})$     | $\text{eat}$ |
| $\ldots$ | $\ldots$ |

???

The size of the table grows exponentially with the (maximum) length of the percept sequence! With $|\mathcal{P}| = 4$ percepts, there are $4^t$ percept sequences of length $t$.

---

class: middle, center, black-slide

.width-100.center[![](figures/lec1/pacman-world.jpg)]

What about the actual Pacman?<br> How would you design its agent program to play optimally?

???

Run the program!

---

# Rational agents

A sequence of environment states is evaluated by a .bold[performance measure].

An agent is .bold[rational] if it chooses actions that maximize the expected value of the performance measure, given the percept sequence to date.

.alert[Rationality only concerns .bold[what] decisions are made (not the thought process behind them, human-like or not).]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

.center[![](figures/lec1/max-utility.png)

In this course, Artificial intelligence = .bold[Maximizing expected performance]
]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

???

Underline the importance of .bold[expected].

---

class: middle

- Rationality $\neq$ omniscience    
    - percepts may not supply all relevant information.
- Rationality $\neq$ clairvoyance
    - action outcomes may not be as expected.
- Hence, rational $\neq$ successful.
- However, rationality leads to .bold[exploration], .bold[learning] and .bold[autonomy].

---

# Performance, environment, actuators, sensors

The characteristics of the performance measure, environment, action space and
percepts dictate approaches for selecting rational actions.
They are summarized as the .bold[task environment].

## Example 1: a chess-playing agent
- performance measure: win, draw, lose, ...
- environment: chess board, opponent, ...
- actions: move pieces, ...
- sensors: board state, opponent moves, ...

---

class: middle

## Example 2: a self-driving car
- performance measure: safety, destination, legality, comfort, ...
- environment: streets, highways, traffic, pedestrians, weather, ...
- actions: steering, accelerator, brake, horn, speaker, display, ...
- sensors: video, accelerometers, gauges, engine sensors, GPS, ...

## Example 3: a medical diagnosis system
- performance measure: patient health, cost, time, ...
- environment: patient, hospital, medical records, ...
- actions: diagnosis, treatment, referral, ...
- sensors: medical records, lab results, ...

---

class: middle

## Example 4: a coding agent
- performance measure: tests pass, correct and readable code, user satisfaction, cost, ...
- environment: code repository, terminal, web, user, ...
- actions: edit files, run commands, search the web, ask the user, ...
- sensors: file contents, command outputs, user messages, ...

???

The agents of Lecture 0 fit this vocabulary. Tool calls are the actuators, tool results the sensors. The model decides; the harness implements the sensors and the actuators.

---

class: middle

## What you ask for is what you get

.quote[As a general rule, it is better to design performance measures according to what one actually wants in the environment, rather than according to how one thinks the agent should behave. .author[Russell and Norvig]]

A rational agent maximizes the performance measure it is given, not the one we had in mind.

???

The example of AIMA: a vacuum cleaner rewarded for the amount of dirt it cleans up can clean the dirt, dump it back on the floor, and clean it again. Reward a clean floor instead.

Modern agents do the same. In 2025, METR reported frontier models that modified the tests or the scoring code of their tasks, or read the answer that the scorer had already computed, instead of solving the task.

---

class: middle, black-slide

.center[
<iframe width="600" height="450" src="https://www.youtube.com/embed/tlOIHko8ySg" frameborder="0" allowfullscreen></iframe>

Faulty reward functions in the wild (OpenAI, 2016).
]

.footnote[Credits: [OpenAI](https://openai.com/index/faulty-reward-functions/), 2016.]

???

CoastRunners rewards hitting targets along the course, not finishing the race. The agent found a lagoon where it circles and hits the same three targets as they reappear. It catches fire, crashes into other boats, goes the wrong way, and still scores about 20% more than human players.

---

# Environment types

.bold[Fully observable] vs. .bold[partially observable]
> Whether the agent sensors give access to the complete state of the environment, at each point in time.

.bold[Deterministic] vs. .bold[stochastic]
> Whether the next state of the environment is completely determined by the current state and the action executed by the agent.

.bold[Episodic] vs. .bold[sequential]
> Whether the agent's experience is divided into atomic independent episodes.

.bold[Static] vs. .bold[dynamic]
> Whether the environment can change while the agent is deliberating (semidynamic if only the performance measure changes).

---

class: middle

.bold[Discrete] vs. .bold[continuous]
> Whether the state of the environment, the time, the percepts or the actions are continuous.

.bold[Single agent] vs. .bold[multi-agent]
> Whether the environment includes several agents that may interact with each other.

.bold[Known] vs. .bold[unknown]
> Reflects the agent's state of knowledge of the "laws of physics" of the environment.

---

class: middle

Are the following task environments fully observable? deterministic? episodic?
static? discrete? single agents? Known?

- Crossword puzzle
- Chess, with a clock
- Poker
- Backgammon
- Taxi driving
- Medical diagnosis
- Part-picking robot
- A coding agent
- The real world

???

Suggested answers (observable, deterministic, episodic, static, discrete, agents, known). Several are debatable, which is the point of the exercise.
- Crossword puzzle: fully, deterministic, sequential, static, discrete, single, known.
- Chess, with a clock: fully, deterministic, sequential, semidynamic, discrete, multi, known.
- Poker: partially, stochastic, sequential, static, discrete, multi, known.
- Backgammon: fully, stochastic, sequential, static, discrete, multi, known.
- Taxi driving: partially, stochastic, sequential, dynamic, continuous, multi, mostly known.
- Medical diagnosis: partially, stochastic, sequential, dynamic, continuous, single, partially known.
- Part-picking robot: partially, stochastic, episodic, dynamic, continuous, single, known.
- A coding agent: partially (it cannot read everything at once, nor the intent of the user), stochastic (flaky tests, network, replies of the user), sequential, mostly static while it works, discrete, single or multi (the user, other agents), partially known.
- The real world: partially, stochastic, sequential, dynamic, continuous, multi, unknown.

---

class: middle, center, black-slide

.width-100.center[![](figures/lec1/pacman-world.jpg)]

What about Pacman?

---

# Agent programs

Our goal is to design an .bold[agent program] that implements the agent
policy. 

Agent programs can be designed and implemented in many ways:
- with tables
- with rules
- with search algorithms
- with learning algorithms

The best design depends on the task environment.

---

# Reflex agents


Reflex agents ...
- choose an action based on current percept (and maybe memory);
- may have memory or model of the world's current state;
- do not consider the future consequences of their actions.

<br>
.center.width-50[![](figures/lec1/reflex-agent-cartoon.png)]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

## Simple reflex agents

.center.width-80[![](figures/lec1/simple-reflex-agent.svg)]

???

Solution to huge tables: forget about the past!

Compress them using condition-action rules.

---

class: middle

.bold[Simple reflex agents] select actions on the basis of the current percept,
ignoring the rest of the percept history.

They are implemented by condition-action rules that match the
current percept to an action. Rules provide a way to .bold[compress] the function table.

They can only work if the correct
decision can be made on the basis of the current percept only, which is rarely the case in practice unless the environment is fully observable.

.question[Examples: Smoke detectors, automatic doors, motion-activated lights, etc.]

---

class: middle

## Model-based reflex agents

.center.width-80[![](figures/lec1/model-based-reflex-agent.svg)]

???

Solution: do not actually forget about the past. Remember what you have seen so far by maintaining an internal representation of the world, a belief state.

Then map this state to an action.

---

class: middle

.bold[Model-based reflex agents] handle partial observability of the environment by keeping track of the part of the world they cannot see now.

They maintain an internal state that is updated on the basis of a .bold[model] which determines:
- how the environment evolves independently of the agent;
- how the agent actions affect the world.

.question[Example: robot vacuum cleaner, smart thermostats, etc.]

---

# Planning agents

Planning agents ...
- ask "what if?";
- make decisions based on (hypothesized) consequences of actions;
- must have a model of how the world evolves in response to actions;
- must formulate a goal.

<br>
.center.width-50[![](figures/lec1/plan-agent-cartoon.png)]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

## Goal-based agents

.center.width-80[![](figures/lec1/goal-based-agent.svg)]

???

It is not easy to map a state to an action because goals are not explicit in condition-action rules.

---

class: middle

The decision process of a .bold[goal-based agent] can be summarized as follows:
1. generate possible sequences of actions;
2. predict the resulting states;
3. assess .bold[goals] in each;
4. select the first action of a sequence where the goal is achieved.

Finding action sequences that achieve goals is difficult. .bold[Search] and .bold[planning] are two strategies.

.question[Examples: GPS navigation system, game-playing agents.]

---

class: middle

## Utility-based agents

.center.width-80[![](figures/lec1/utility-based-agent.svg)]

???

Often there are several sequences of actions that achieve a goal. We should pick the best.

---

class: middle

Goals are often not enough to generate high-quality behavior. Goals only provide binary assessment of performance.

Instead, a .bold[utility function] scores any given sequence of environment states. The higher the score, the better the sequence.

A rational utility-based agent chooses an action that .bold[maximizes the expected utility of its outcomes].

.question[Examples: self-driving cars, recommendation systems.]

???

Note that the utility function is different from the performance measure, which is only used to evaluate the agent's behavior. The utility function is an internalization of the performance measure.

---

# Learning agents

<br>
.center.width-80[![](figures/lec1/learning-agent.svg)]

---

class: middle

.bold[Learning agents] improve their performance and adapt to new circumstances by learning from their experiences. They are capable of self-improvement.

They can make changes to any of the knowledge components by:
- learning how the .bold[world] evolves;
- learning what are the .bold[consequences] of actions;
- learning the utility of actions through .bold[rewards].

.question[Examples: robots, reasoning models trained by reinforcement learning.]

???

A reasoning model maps onto this diagram. The performance element is the language model. The critic is a program that checks the final answer against the correct one, the performance standard. The learning element is the reinforcement learning algorithm that updates the weights. Exploration comes from sampling several attempts per problem.

---

class: middle, black-slide

.center[
<iframe width="600" height="450" src="https://www.youtube.com/embed/xAXvfVTgqr0" frameborder="0" allowfullscreen></iframe>

Learning to walk in the real world in one hour (Wu et al., 2022).
]

.footnote[Credits: [Wu et al.](https://danijar.com/project/daydreamer/), 2022.]

---

# Summary

- An .bold[agent] is an entity that perceives and acts in an environment.
- The .bold[performance measure] evaluates the agent's behavior. .bold[Rational agents] act so as to maximize the expected value of the performance measure.
- .bold[Task environments] include performance measure, environment, actuators and sensors. They can vary along several significant dimensions.
- The .bold[agent program] effectively implements the agent policy. Its design is dictated by the task environment.
- .bold[Simple reflex agents] respond directly to percepts, whereas .bold[model-based reflex agents] maintain internal state to track the world. .bold[Goal-based agents] act to achieve goals while .bold[utility-based agents] try to maximize their expected performance.
- All agents can improve their performance through .bold[learning].

???

Next week we will see how to implement our first agent, a goal-based agent based on search algorithms.

---

class: end-slide, center
count: false

The end.
