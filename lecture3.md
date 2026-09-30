class: middle, center, title-slide

# Introduction to Artificial Intelligence

Lecture 3: Games and Adversarial search

<br><br>
Prof. Gilles Louppe<br>
[g.louppe@uliege.be](mailto:g.louppe@uliege.be)

---

class: center, black-slide, middle

<iframe width="600" height="450" src="https://www.youtube.com/embed/LJS7Igvk6ZM" frameborder="0" allowfullscreen></iframe>

???

Questions to ask after the video, each a preview of the lecture, with short answers:
- Who are the agents, and what can each of them do? The friends; each chooses whom to approach, the blonde or one of her friends. (the formal definition of a game)
- What does Nash reason about, moves or outcomes? Outcomes: he scores how the evening ends and reasons back from there. (utilities of terminal states, backed up)
- Why can't a friend decide on his own, once and for all? His best choice depends on what the others do, so he needs an answer for every situation they can create. (a strategy, not a fixed plan)
- Are the interests of the friends opposed or shared? Both: they compete for the blonde, yet all lose if all go for her. (zero-sum games, and beyond)
- What does Nash assume the others will do? That they reason as well as he does, each in his own interest. (an optimal opponent, as in minimax)
- Would his plan hold if one friend changed his mind? No: if nobody goes for the blonde, a single friend does better by going for her.

---

# Today

.question[How to act rationally in a .bold[multi-agent] environment? How to anticipate and respond to the .bold[arbitrary behavior] of other agents?]

- Adversarial search
    - Minimax
    - $\alpha$-$\beta$ pruning
    - H-Minimax
    - Expectiminimax
    - Monte Carlo Tree Search
- Modeling assumptions
- State-of-the-art agents.

---

class: middle

# Games

---

class: middle

## Formal definition

A .bold[game] is defined by
- the .bold[states] ${s \in \mathcal{S}}$ and the .bold[initial state] ${s\_1 \in \mathcal{S}}$;
- the .bold[actions] ${\text{actions}(s) \subseteq \mathcal{A}}$ available in state ${s}$;
- the .bold[transition model] ${s' = \text{result}(s, a)}$, the state reached by taking ${a}$ in ${s}$;
- a function ${\text{player}(s) \in \\{1, \ldots, N\\}}$ that says whose turn it is in state ${s}$;
- the .bold[terminal states] ${T \subseteq \mathcal{S}}$, tested by ${\text{terminal-test}(s)}$, i.e. ${s \in T}$;
- a .bold[utility] ${\text{utility}(s, p)}$, the payoff of player ${p}$ when the game ends in ${s \in T}$, e.g. ${1}$, ${0}$ or ${\frac{1}{2}}$ for a win, a loss or a draw.

Together, ${s\_1}$, ${\text{actions}}$ and ${\text{result}}$ define the .bold[game tree], whose nodes are states and whose edges are actions.

???

A game is a mathematical model of strategic interaction between rational decision makers.

Outline on the blackboard.

---

class: middle

## Strategies

Even in a deterministic and fully observable environment, the opponents may act .bold[arbitrarily]: the next state depends on their choices, which we cannot predict.

A fixed sequence of actions ${a\_{1:T}}$, the solution of a search problem, is then of no use, since the opponent may lead the game anywhere. A .bold[solution] is instead a .bold[strategy], or .bold[policy], ${\pi\_p : \mathcal{S} \to \mathcal{A}}$ for player ${p}$: a move for every state the opponent can lead to.

---

class: middle

## Zero-sum games

A game is .bold[zero-sum] if the utilities of the players sum to the same constant ${c}$ in every terminal state:
$$\sum\_{p=1}^N \text{utility}(s, p) = c \quad \text{for all } s \in T.$$
- e.g., in chess, ${c = 1}$: ${1 + 0}$, ${0 + 1}$ or ${\frac{1}{2} + \frac{1}{2}}$.
- With two players, ${\text{utility}(s, 2) = c - \text{utility}(s, 1)}$: a .bold[single utility] describes the game, which player 1 .bold[maximizes] and player 2 .bold[minimizes].
- This is .bold[strict competition]: what one player gains, the other loses.

<br>
.center.width-40[![](figures/lec3/zero-sum-cartoon.png)]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

???

The term 'zero-sum' is confusing but makes sense if you imagine each player is charged an entry of 1/2 (for chess). Constant-sum game would have been better.

The bar scene is not zero-sum: the friends can all lose together, or all do well together.

---

class: middle

## Tic-Tac-Toe game tree

.width-80[![](figures/lec3/tictactoe.png)]

.question[What is an optimal strategy (or perfect play)? How do we find it?]

???

Play a game against the students. Perfect play by both sides is a draw, so the game is won only on a mistake.

Play X and open in a corner: 7 of the 8 replies lose, and only the center holds the draw (after the center, the 4 edges lose; after an edge, 4 replies lose).

On every move, in this order: win; block their line; fork (two threats at once); block their fork; center; the corner opposite theirs; any corner; any edge.

If they open in a corner as X, take the center: any other reply loses.

This rule set is a minimax strategy: it never does worse than a draw, and it wins only when the opponent errs.

---

class: middle

# Minimax

---

class: middle

## Assumptions

Games vary along three axes: .bold[chance], .bold[information] and the .bold[number of players]. We start with the simplest case of each.

- We assume a .bold[deterministic], .bold[turn-taking], .bold[two-player] .bold[zero-sum game] with .bold[perfect information].
    - e.g., Tic-Tac-Toe, Chess, Checkers, Go, etc.
- We will call our two players MAX and MIN. MAX moves first.

.center.width-55[![](figures/lec3/tictactoe-cartoon.png)]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

.center.width-25[![](figures/lec3/adversarial-search-cartoon.png)]

## Adversarial search

- In a search problem, the solution ${a\_{1:T}}$ is a fixed plan.
- In a game, MAX cannot know which move MIN will play, .bold[now or later]. It must anticipate .bold[every] reply of MIN, every reply to its own answers, and so on until the game ends.
- A .bold[strategy] ${\pi\_\text{MAX}}$ therefore fixes, in advance,
    - its move in the initial state,
    - its move after each possible reply of MIN,
    - its move after each possible reply of MIN to those moves, ...

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

???

Analogy with chess, checkers or belotte.

---

# Perfect play

What does MAX obtain from a state if .bold[both players play perfectly] from there on? Reason .bold[backwards], from the end of the game.

.center.width-70[![](figures/lec3/minimax-tree-1.svg)]

- At the .bold[leaves], the game is over: the payoff is the utility.

---

count: false

# Perfect play

What does MAX obtain from a state if .bold[both players play perfectly] from there on? Reason .bold[backwards], from the end of the game.

.center.width-70[![](figures/lec3/minimax-tree-2.svg)]

- At the .bold[leaves], the game is over: the payoff is the utility.
- At a .bold[MIN node], MIN plays the move that is worst for MAX: the left node is worth ${\min(3, 12, 8) = 3}$, the other two ${2}$.

---

count: false

# Perfect play

What does MAX obtain from a state if .bold[both players play perfectly] from there on? Reason .bold[backwards], from the end of the game.

.center.width-70[![](figures/lec3/minimax-tree-3.svg)]

- At the .bold[leaves], the game is over: the payoff is the utility.
- At a .bold[MIN node], MIN plays the move that is worst for MAX: the left node is worth ${\min(3, 12, 8) = 3}$, the other two ${2}$.
- At the .bold[root], MAX plays the move that is best for it, knowing how MIN will answer: ${\max(3, 2, 2) = 3}$, reached by ${a\_1}$.

???

This is backward induction: the scores of the outcomes are backed up, one level at a time, to the decision at the root.

---

# Minimax

The .bold[minimax value] $\text{minimax}(s)$ is the utility that MAX obtains from $s$ when both players play perfectly. Backing up values from the terminal states gives
$$\text{minimax}(s) = \begin{cases}
\text{utility}(s) & \text{if } s \in T \\\\
\max\limits\_{a} \text{minimax}(\text{result}(s, a)) & \text{if MAX plays} \\\\
\min\limits\_{a} \text{minimax}(\text{result}(s, a)) & \text{if MIN plays,}
\end{cases}$$
where the $\max$ and $\min$ are over ${a \in \text{actions}(s)}$.

The .bold[optimal] next move (for MAX) maximizes the minimax value of the resulting state, ${\pi^\*(s) = \arg\max\limits\_{a} \text{minimax}(\text{result}(s, a))}$.
- ${\text{minimax}(s)}$ is a .bold[guarantee]: whatever MIN plays, MAX obtains at least ${\text{minimax}(s)}$, and an optimal MIN holds it to exactly that.
- MAX thus plans for the .bold[worst case], without any assumption on the strength of the opponent.

???

Blackboard.

---

class: middle

## Properties of Minimax

- .bold[Completeness]:
    - Yes, if tree is finite.
- .bold[Optimality]:
    - Yes, if MIN is an optimal opponent.
    - What if MIN is suboptimal?
        - Show that MAX does at least as well.
    - What if MIN is suboptimal and predictable?
        - Other strategies might do better than Minimax. However they may do worse on an optimal opponent.

???

On the perfect play tree: MAX plays ${a\_1}$, of value ${3}$. An optimal MIN answers with the leaf ${3}$; a suboptimal MIN picks ${12}$ or ${8}$, and MAX gets more. MAX never gets less than ${3}$, whatever MIN does.

At least as well, not strictly better: if MIN errs where it does not matter (the other replies may be worth as much), or never errs, MAX gets exactly ${3}$.

In general, MAX playing ${\pi^\*}$ from ${s}$ obtains at least ${\text{minimax}(s)}$, by induction from the leaves:
- at a terminal state, it obtains ${\text{utility}(s) = \text{minimax}(s)}$;
- at a MAX node, it plays the child of value ${\text{minimax}(s)}$;
- at a MIN node, every child is worth at least ${\min = \text{minimax}(s)}$, whichever MIN picks.

---

class: middle

## Minimax efficiency

- Assume $\text{minimax}(s)$ is implemented using its recursive definition.
- How efficient is minimax?
    - Time complexity: same as DFS, i.e., $O(b^m)$.
    - Space complexity:
        - $O(bm)$, if all actions are generated at once, or
        - $O(m)$, if actions are generated one at a time.

.question[Do we need to explore the whole game tree?]

---

# Pruning

.center.width-80[![](figures/lec3/minimax-pruned.svg)]

$$\begin{aligned}
\text{minimax}(\text{root}) &= \max(\min(3, 12, 8), \min(2, x, y), \min(14, 5, 2)) \\\\
&= \max(3, z, 2) \quad \text{where } z = \min(2, x, y) \leq 2 \\\\
&= 3.
\end{aligned}$$

Therefore, it is possible to compute the .bold[correct] minimax decision .bold[without looking at every node] in the tree.

---

# Pruning, step by step

.center.width-80[![](figures/lec3/alpha-beta-1.svg)]

The first leaf of B is ${3}$: B, a MIN node, is worth .bold[at most] ${3}$.

---

count: false

# Pruning, step by step

.center.width-80[![](figures/lec3/alpha-beta-2.svg)]

The leaf ${12}$ does not change the bound of B: MIN would not choose it.

---

count: false

# Pruning, step by step

.center.width-80[![](figures/lec3/alpha-beta-3.svg)]

B is worth exactly ${3}$: MAX is guaranteed .bold[at least] ${3}$ at the root.

---

count: false

# Pruning, step by step

.center.width-80[![](figures/lec3/alpha-beta-4.svg)]

The first leaf of C is ${2}$: C is worth at most ${2 < 3}$. MAX will never choose C, so its other leaves are .bold[pruned].

---

count: false

# Pruning, step by step

.center.width-80[![](figures/lec3/alpha-beta-5.svg)]

The first leaf of D is ${14}$: D is worth at most ${14}$, and so is the root.

---

count: false

# Pruning, step by step

.center.width-80[![](figures/lec3/alpha-beta-6.svg)]

The other leaves bring D down to ${2}$. The root is worth exactly ${3}$, reached by ${a\_1}$.

---

class: middle

.grid[
.kol-3-5[
We want to compute $v = \text{minimax}(n)$, for $\text{player(n)}$=MIN.
- We loop over $n$'s children.
- The minimax values are being computed one at a time and $v$ is updated iteratively.
- Let $\alpha$ be the best value (i.e., the highest) at any choice point along the path for MAX.
- If $v$ becomes lower than $\alpha$, then .bold[$n$ will never be reached] in actual play.
- Therefore, we can .bold[stop iterating] over the remaining $n$'s other children.
]
.kol-2-5[.center.width-100[![](figures/lec3/alpha-beta-path.svg)]]
]

???

Go back to step 4 of the previous sequence: C is pruned because its value, at most 2, is below α = 3.

If the minimax value $v$ for MIN becomes lower than the best value $\alpha$ for MAX, then $n$ will never be reached.

---

class: middle

Similarly, $\beta$ is defined as the best value (i.e., lowest) at any choice point along the path for MIN. We can halt the expansion of a MAX node as soon as $v$ becomes larger than $\beta$.

## $\alpha$-$\beta$ pruning
- Updates the values of $\alpha$ and $\beta$ as the path is expanded.
- Prune the remaining branches (i.e., terminate the recursive calls) as soon as the value of the current node is known to be worse than the current $\alpha$ or $\beta$ value for MAX or MIN, respectively.

???

If the minimax value $v$ for MAX becomes larger the best value $\beta$ for MIN, then $n$ will never be reached.

---

# $\alpha$-$\beta$ search

.center.width-90[![](figures/lec3/alpha-beta-search.svg)]

???

Note that MAX plays first, hence the first call to MAX-VALUE in the main function.

---

class: middle

## Properties of $\alpha$-$\beta$ search

- Pruning has .bold[no effect] on the minimax values. Therefore, .bold[completeness] and .bold[optimality] are preserved from Minimax.
- Time complexity:
    - The effectiveness depends on the order in which the states are examined.
    - If states could be examined in .bold[perfect order], then $\alpha$-$\beta$ search examines only $O(b^{m/2})$ nodes to pick the best move, vs. $O(b^m)$ for minimax.
        - $\alpha$-$\beta$ can solve a tree twice as deep as minimax can in the same amount of time.
        - Equivalent to an effective branching factor $\sqrt{b}$.
- Space complexity: $O(m)$, as for Minimax.

---

# Game tree size

.center.width-30[![](figures/lec3/chess.jpg)]

Chess:
- $b \approx 35$ (approximate average branching factor)
- $d \approx 100$ (depth of a game tree for typical games)
- $b^d \approx 35^{100} \approx 10^{154}$.
- For $\alpha$-$\beta$ search and perfect ordering, we get $b^{d/2} \approx 35^{50} = 10^{77}$.

Finding the exact solution with Minimax remains .bold[intractable].

---

# Transposition table

- Repeated states occur frequently because of .bold[transpositions]: distinct permutations of the move sequence end in the same state.
- Like the closed set of graph search, a .bold[transposition table] stores ${\text{minimax}(s)}$ for every state ${s}$ already evaluated, so that a repeated state is looked up rather than searched again.

.question[What data structure should be used to efficiently store and look up the values of states?]

???

A .bold[hash table], keyed by the state, with expected ${O(1)}$ insertion and look-up.

In chess programs, the key is a 64-bit Zobrist hash: a random number is drawn once for every (piece, square) pair, and the key of a position is the XOR of the numbers of its pieces, updated in ${O(1)}$ after each move. The table has a fixed size and replaces old entries, keeping those searched deepest. With α-β pruning, an entry also stores the depth of the search and whether the value is exact or only a bound.

---

# Imperfect real-time decisions

Under .bold[time constraints], searching down to the terminal states is not feasible in most realistic games. The solution is to cut the search earlier:
- replace the $\text{utility}(s)$ function with a heuristic .bold[evaluation function] $\text{eval}(s)$ that estimates the state utility;
- replace the terminal test by a .bold[cutoff test] ${\text{cutoff-test}(s, d)}$ that decides when to stop expanding a state $s$ at depth $d$.

$$\text{h-minimax}(s, d) = \begin{cases}
\text{eval}(s) & \text{if cutoff} \\\\
\max\limits\_{a} \text{h-minimax}(\text{result}(s, a), d + 1) & \text{if MAX plays} \\\\
\min\limits\_{a} \text{h-minimax}(\text{result}(s, a), d + 1) & \text{if MIN plays.}
\end{cases}$$

.question[Can $\alpha$-$\beta$ search be adapted to implement H-Minimax?]

???

Yes.

Replace the if-statements with the terminal test with if-statements with the cutoff test.

---

class: middle

## Evaluation functions

An evaluation function $\text{eval}(s)$ returns an .bold[estimate] of the expected utility of the game from a state $s$. Its computation .bold[must be short]: that is the whole point of cutting the search.

Ideally, $\text{eval}(s)$ .bold[orders] states as their minimax values do. Its values may differ from the minimax values, as long as the order is preserved. In non-terminal states, it should be strongly .bold[correlated] with the actual chances of winning.

???

- Like for heuristics in search, evaluation functions can be learned using machine learning algorithms.

---

class: middle

## Quiescence

.center.width-70[![](figures/lec3/chess-eval.png)]

These two states differ only in the position of the rook at the lower right, yet Black has the advantage in (a) but not in (b). If the search stops in (b), Black does not see that White's next move captures its queen.

The cutoff should only be applied to .bold[quiescent] states, whose value is unlikely to exhibit wild swings in the near future.

---

# The horizon effect

H-Minimax sees the game only down to its cutoff depth, its .bold[horizon]. Below it, $\text{eval}(s)$ stands in for everything that may happen next, and evaluation functions are .bold[always imperfect].

.center.width-70[![](figures/lec3/horizon-1.svg)]

Searching to depth 2, ${a\_1}$ looks best: $\text{eval}$ rates it ${5}$, against ${0}$ for ${a\_2}$.

---

count: false

# The horizon effect

H-Minimax sees the game only down to its cutoff depth, its .bold[horizon]. Below it, $\text{eval}(s)$ stands in for everything that may happen next, and evaluation functions are .bold[always imperfect].

.center.width-70[![](figures/lec3/horizon-2.svg)]

Beyond the horizon, ${a\_1}$ loses: what it seemed to gain is paid back later (${-9}$). The search took a .bold[bad move] for a .bold[good move], because its consequences were hidden beyond the horizon.

---

class: middle

## Depth versus evaluation

An inaccurate $\text{eval}$ can be compensated by a .bold[deeper search], as long as $\text{eval}$ becomes .bold[more accurate] closer to the end of the game. The deeper the cutoff, the later in the game the evaluated states: the search sees more consequences for itself, and the errors of $\text{eval}$ matter less. At the limit, the search reaches the terminal states and needs no evaluation at all.

The converse does not hold: a better $\text{eval}$ cannot compensate a .bold[shallow search]. What lies beyond the horizon can only be estimated, and a perfect evaluation, ${\text{eval}(s) = \text{minimax}(s)}$ everywhere, would require solving the game.

???

This is what happens in practice, in chess, checkers or Go, but not in every game: there exist pathological games where searching deeper with an imperfect evaluation makes decisions worse (Nau, 1983).

The horizon effect goes both ways: a good move, such as a sacrifice that pays off only later, may look bad.

It also delays losses: when a loss cannot be avoided, the search prefers moves that push it past the horizon, e.g. giving away pawns to postpone the loss of the queen.

Programs move the horizon where it matters: they search deeper on states that are not quiescent (quiescence search) and on forced moves (singular extensions).

---

class: middle, black-slide

.center[<video controls preload="auto" height="480" width="640">
  <source src="figures/lec3/depth2.mp4" type="video/mp4">
</video>]

.caption[Cutoff at depth 2, evaluation = the closer to the dot, the better.]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

???

```
cd demo/lec3
uv run python run.py --agentfile hminimax.py --pdepth 2 --nghosts 2 --slowmo on
uv run python run.py --agentfile hminimax.py --pdepth 10 --nghosts 2 --slowmo on
```

---

class: middle, black-slide

.center[<video controls preload="auto" height="480" width="640">
  <source src="figures/lec3/depth10.mp4" type="video/mp4">
</video>]

.caption[Cutoff at depth 10, evaluation = the closer to the dot, the better.]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

# Multi-agent games

For games that are not zero-sum, or have .bold[more than two players], minimax generalizes by backing up a .bold[vector] of utilities ${v(s) \in \mathbb{R}^N}$, one per player, where the player to move maximizes its own component:
$$v(s) = \begin{cases}
\left(\text{utility}(s, 1), \ldots, \text{utility}(s, N)\right) & \text{if } s \in T \\\\
v(\text{result}(s, a^\*)) & \text{otherwise,}
\end{cases}$$
where ${a^\* = \arg\max\_{a} v\_{\text{player}(s)}(\text{result}(s, a))}$.

In a two-player zero-sum game, ${v\_2(s) = c - v\_1(s)}$, and maximizing ${v\_2}$ is minimizing ${v\_1}$: this is minimax.

---

class: middle

## Cooperation and competition

.center.width-80[![](figures/lec3/multi-agent-tree-1.svg)]

Without a zero-sum constraint, the interests of the players are no longer opposed: they may .bold[cooperate] or .bold[compete], depending on the state.

---

count: false
class: middle

## Cooperation and competition

.center.width-80[![](figures/lec3/multi-agent-tree-2.svg)]

Without a zero-sum constraint, the interests of the players are no longer opposed: they may .bold[cooperate] or .bold[compete], depending on the state.

---

class: middle

# Stochastic games

---

# Stochastic games

In real life, unpredictable external events can put an agent into unforeseen situations. Games that mirror this unpredictability are called .bold[stochastic games]: they include a random element, such as explicit randomness (rolling dice) or actions that may fail (the wheels of a robot might slip).

<br>
.center.width-40[![](figures/lec3/random-opponent-cartoon.png)]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

In a game tree, the random element is .bold[modeled] with .bold[chance nodes]. A chance node stands for a state-action pair ${(s, a)}$, from which the next state ${s'}$ follows with .bold[probability] ${P(s' \mid s, a)}$.

This amounts to treating the environment as an extra .bold[random player], CHANCE, that moves after each of the other players.

.center.width-30[![](figures/lec3/random-player.png)]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle

## Stochastic game tree

.center.width-80[![](figures/lec3/stochastic-game-tree.svg)]

???

- This tree corresponds to a game with two dices
- What is the best move? The best move cannot be determined anymore, because it depends on chance.

=> Assume the 2nd player is rational and plays optimally and that the 3rd player (corresponding to chance nodes) is random.

---

# Expectiminimax

Because of the uncertainty in the outcomes of actions, states no longer have a .bold[definite] $\text{minimax}$ value.

The value of a chance node ${(s, a)}$ is instead the .bold[expected] value of the state that follows,
$$q(s, a) = \sum\_{s'} P(s' \mid s, a) \, v(s'),$$
the average over the outcomes, weighted by their probabilities, where $\text{minimax}$ would assume the worst outcome. A deterministic action is the special case ${P(\text{result}(s, a) \mid s, a) = 1}$.

---

class: middle

## The expectiminimax recursion

Writing ${v(s) = \text{expectiminimax}(s)}$ for short, the values of states and chance nodes are defined together,
$$v(s) = \begin{cases}
\text{utility}(s) & \text{if } s \in T \\\\
\max\limits\_a q(s, a) & \text{if MAX plays} \\\\
\min\limits\_a q(s, a) & \text{if MIN plays,}
\end{cases} \qquad q(s, a) = \sum\_{s'} P(s' \mid s, a) \, v(s').$$

.question[Does taking the rational move mean the agent will be successful?]

---

class: middle

## Evaluation functions

As for $\text{minimax}(s)$, $\text{expectiminimax}(s)$ may be approximated by cutting the recursion early and using an evaluation function $\text{eval}(s)$.

With chance nodes, preserving the order of states is .bold[not enough]: expectations add values, so $\text{eval}(s)$ must be a .bold[positive linear transformation] of the expected utility for the move to stay correct.

.center.width-70[![](figures/lec3/chance-order-preserving.svg)]
.caption[An order-preserving transformation on leaf values changes the best move.]

If the utilities are bounded, $\alpha$-$\beta$ search can be adapted to stochastic games.

---

class: middle

# Monte Carlo tree search

---

class: middle

## Random playout evaluation

To evaluate a state ${s}$, let the algorithm play .bold[against itself] from ${s}$ with .bold[random moves], thousands of times. Each such game is a .bold[random playout], and the evaluation is the proportion of playouts won,
$$\text{eval}(s) = \frac{1}{K} \sum\_{k=1}^K \mathbf{1}[\text{playout } k \text{ is won}].$$

This evaluation requires .bold[no domain knowledge]: the game engine is all that is needed.

???

Explain MCTS on the blackboard.

---

class: middle

## Monte Carlo Tree Search

Evaluating every move with the same number of random playouts wastes most of them on bad moves. MCTS instead grows a search tree from the root and spends its playouts on the .bold[most promising moves].

Each node $n$ in the current search tree maintains two values:
- the number of wins $Q(n,p)$, over the playouts that passed through $n$, of the player $p$ who made the move leading to $n$;
- the number $N(n)$ of times $n$ has been visited.

---

class: middle

Each round of the search does four things: .bold[selection] down to a node $n$ that is not fully expanded, .bold[expansion] of one child $n'$ of $n$, .bold[simulation] of a random playout from $n'$, and .bold[backpropagation] of the result along the path back to the root.

.width-100[![](figures/lec3/mcts.svg)]

Rounds are repeated for as long as the time budget allows. The move played is the one leading to the most visited child of the root.

---

class: middle

## Exploration and exploitation

Given a limited budget of random playouts, the efficiency of MCTS critically depends on the choice of the nodes made during the .bold[selection] step.

During the selection step, the UCB1 policy picks the child node $n'$ of $n$ that maximizes
$$\frac{Q(n',p)}{N(n')} + c \sqrt{\frac{\log N(n)}{N(n')}},$$
where $p$ is the player to move in $n$. The first term encourages the .bold[exploitation] of nodes with a high win rate, the second the .bold[exploration] of nodes visited little, and the constant $c > 0$ sets the trade-off between the two.

???

With UCB1, the values in the tree converge to the minimax values as the number of rounds grows: the most promising moves end up visited far more often than the others, and their win rates approach their true values.

The score is an upper confidence bound on the win rate of the child: optimism in the face of uncertainty. By Hoeffding's inequality, after ${N(n')}$ playouts the observed win rate is within ${\sqrt{\log(1/\delta) / 2N(n')}}$ of the true one with probability at least ${1 - \delta}$. Taking ${\delta = N(n)^{-4}}$ gives the bonus ${\sqrt{2 \log N(n) / N(n')}}$, i.e. ${c = \sqrt{2}}$.

The bonus shrinks as a child is tried (${1/\sqrt{N(n')}}$), and grows slowly as the parent is visited (${\log N(n)}$), so a child that is neglected is eventually tried again. The log grows just fast enough: every child is tried infinitely often, but a worse child only about ${\log N(n)}$ times out of ${N(n)}$, the smallest possible cost of exploring (Auer, Cesa-Bianchi and Fischer, 2002). Without the log, the search would keep spreading its playouts evenly; with a constant, an unlucky child could be abandoned for good.

---

<br>
## One round of MCTS

.center.width-50[![](figures/lec3/mcts-1.svg)]

Grey nodes are Black's turns, white nodes White's; each shows ${Q(n, p) / N(n)}$ for the player who made the move leading to it. .bold[Selection]: from the root, follow UCB1 down to a node that is not fully expanded.


---

count: false

<br>
## One round of MCTS

.center.width-50[![](figures/lec3/mcts-2.svg)]

.bold[Expansion]: add one of its children, not visited yet (0/0).


---

count: false

<br>
## One round of MCTS

.center.width-50[![](figures/lec3/mcts-3.svg)]

.bold[Simulation]: play a random playout from the new node. Here, White, who made the move leading to it, loses (0/1).


---

count: false

<br>
## One round of MCTS

.center.width-50[![](figures/lec3/mcts-4.svg)]

.bold[Backpropagation]: update the counts along the path back to the root: one more visit for every node, and one more win for the nodes reached by a move of the winner.

???

Nodes are coloured by the player to move, as in the other trees: grey for Black, white for White. Each node shows the wins and visits of the player who made the move leading to it, the other colour. At the root, Black is about to move; its 11/21 are White's wins so far, and the three white nodes under it, Black's possible moves, add up to Black's 10/21.

If White loses the simulation, all nodes along the path increment their visits (the denominator), but only the nodes reached by a move of Black, the white nodes, are credited with a win (the numerator). If instead White wins, only the grey nodes are credited. In games where draws are possible, a draw adds 0.5 to the numerator of both. This ensures that during selection, each player expands towards the most promising moves for that player.

Rounds of search are repeated as long as the time allotted to a move remains. Then the move with the most simulations made (i.e. the highest denominator) is chosen as the final answer.

---

class: middle

# Modeling assumptions

---

class: middle

.center[
![](figures/lec2/search-problems-models.png)

What if our assumptions are incorrect?]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

---

class: middle, black-slide

.grid[
.kol-2-3[

## Setup

- $P_1$: Pacman uses depth 4 search with an evaluation function that avoids trouble, while assuming that the ghost follows $P_2$.
- $P_2$: Ghost uses depth 2 search with an evaluation function that seeks Pacman, while assuming that Pacman follows $P_1$.
- $P_3$: Pacman uses depth 4 search with an evaluation function that avoids trouble, while assuming that the ghost follows $P_4$.
- $P_4$: Ghost makes random moves.
]
.kol-1-3[.width-100[![](figures/lec3/wa-setup.png)]]
]

???

All four videos can be replayed live, from `demo/lec3`: P1 is
`--agentfile hminimax_ADV.py`, P3 is `--agentfile expectimax.py`, P2 is
`--ghostagent cheeky --gdepth 2` (a ghost that searches the tree itself) and
P4 is `--ghostagent rightrandy --p 0` (a ghost that moves uniformly at
random). The command of each is in the notes of its slide.

Beware: at `--pdepth 4` Pacman wins all four games, so the live runs show the
behaviour, not the outcome. To show mismodelling actually costing the game,
use `--pdepth 6 --layout small_adv`: P1 wins (505) and P3, facing the same
adversarial ghost, is eaten (-501).

---

class: middle, black-slide

.center[
<video controls preload="auto" height="400" width="300">
  <source src="figures/lec3/minimax-vs-adversarial.mp4" type="video/mp4">
</video>

Minimax Pacman ($P_1$) vs. Adversarial ghost ($P_2$)
]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

???

Assumptions are correct.

Pacman wins partly because of the larger depth it uses.

```
uv run python run.py --agentfile hminimax_ADV.py --pdepth 4 \
    --ghostagent cheeky --gdepth 2 --layout EH2
```

---

class: middle, black-slide

.center[
<video controls preload="auto" height="400" width="300">
  <source src="figures/lec3/minimax-vs-random.mp4" type="video/mp4">
</video>

Minimax Pacman ($P_1$) vs. Random ghost ($P_4$)
]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

???

Assumptions are incorrect. Has the ghost some masterplan?

```
uv run python run.py --agentfile hminimax_ADV.py --pdepth 4 \
    --ghostagent rightrandy --p 0 --layout EH2
```

---

class: middle, black-slide

.center[
<video controls preload="auto" height="400" width="300">
  <source src="figures/lec3/expectimax-vs-random.mp4" type="video/mp4">
</video>

Expectiminimax Pacman ($P_3$) vs. Random ghost ($P_4$)
]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

???

Assumptions are correct.

```
uv run python run.py --agentfile expectimax.py --pdepth 4 \
    --ghostagent rightrandy --p 0 --layout EH2
```

---

class: middle, black-slide

.center[
<video controls preload="auto" height="400" width="300">
  <source src="figures/lec3/expectimax-vs-adversarial.mp4" type="video/mp4">
</video>

Expectiminimax Pacman ($P_3$) vs. Adversarial ghost ($P_2$)
]

.footnote[Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.]

???

Pacman is lucky!

```
uv run python run.py --agentfile expectimax.py --pdepth 4 \
    --ghostagent cheeky --gdepth 2 --layout EH2
```

---

class: middle

# State-of-the-art game programs

---

class: middle

## Perfect information

.grid[
.kol-2-3[
- 1997, .bold[Deep Blue] defeats Garry Kasparov at chess: $2 \times 10^8$ positions per second, a sophisticated evaluation function, and search extended up to 40 plies on some lines.
- 2007, .bold[checkers is solved]: $10^{14}$ calculations over 18 years prove that perfect play by both sides is a draw.
- 2016, .bold[AlphaGo] beats Lee Sedol 4-1, then Ke Jie in 2017, by combining Monte Carlo tree search with deep learning trained on human and self-play games.

Chess and Go remain unsolved: only their best play is now superhuman.
]
.kol-1-3[.center.width-100[![](figures/lec3/deep-blue.jpg)]]
]

.footnote[Schaeffer et al., "Checkers is solved", Science, 2007; Silver et al., "Mastering the game of Go", Nature, 2016.]

???

A solved game is one whose outcome can be predicted from any position, assuming perfect play on both sides.

---

class: middle, black-slide, center

<iframe width="640" height="400" src="https://www.youtube.com/embed/m2QFSocFeOQ" frameborder="0" allowfullscreen></iframe>

.caption[Press coverage for the victory of AlphaGo against Lee Sedol.]

---

class: middle

## Learning to play, from less and less

- 2017, .bold[AlphaGo Zero] reaches the same level from self-play only, with no human games.
- 2018, .bold[AlphaZero] applies the same recipe to chess, shogi and Go, given only the rules.
- 2020, .bold[MuZero] drops the rules too: it learns a model of the game and plans with it, mastering Go, chess, shogi and Atari.

.center.width-55[![](figures/lec3/alphagozero-training.gif)]

.footnote[Credits: [AlphaGo Zero: Learning from scratch](https://deepmind.com/blog/alphago-zero-learning-scratch/); Schrittwieser et al., "Mastering Atari, Go, chess and shogi by planning with a learned model", Nature, 2020.]

---

class: middle

## Imperfect information

The assumption of perfect information we made at the start is what these games drop:

- 2017-2019, .bold[Libratus] then .bold[Pluribus] beat professionals at no-limit poker, the latter with six players at the table, where no notion of optimal play against all opponents exists.
- 2022, .bold[DeepNash] reaches expert level at Stratego, where each side hides its pieces.
- 2022, .bold[Cicero] plays Diplomacy at human level, combining planning with negotiation in natural language.

.question[What does an optimal strategy even mean when the opponents may cooperate, and lie?]

.footnote[Brown and Sandholm, Science, 2017 and 2019; Perolat et al., Science, 2022; Meta FAIR, Science, 2022.]

---

# Summary

- A .bold[game] is defined by its states, actions and transitions, a function ${\text{player}(s)}$, terminal states ${T \subseteq \mathcal{S}}$ and a utility ${\text{utility}(s, p)}$. Its solution is a strategy ${\pi\_p : \mathcal{S} \to \mathcal{A}}$, not a sequence ${a\_{1:T}}$.

- .bold[Minimax] backs the utilities up the tree, ${\max\limits\_a}$ for MAX and ${\min\limits\_a}$ for MIN, in ${O(b^m)}$ time and ${O(bm)}$ space.

- .bold[${\alpha}$-${\beta}$ pruning] returns the same move while examining ${O(b^{m/2})}$ nodes at best: twice the depth in the same time.

- .bold[H-minimax] cuts the search at depth ${d}$ and replaces the utility by an evaluation function, at the price of the horizon effect.

- .bold[Expectiminimax] averages over chance nodes, ${q(s, a) = \sum\_{s'} P(s' \mid s, a) \, v(s')}$, and .bold[Monte Carlo tree search] samples random playouts instead of evaluating.

- Each is optimal only .bold[relative to a model] of the opponent. Assuming the wrong one is not playing well.

---

class: end-slide, center
count: false

The end.