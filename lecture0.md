class: middle, center, title-slide

# Introduction to Artificial Intelligence

Lecture 0: Artificial Intelligence

<br><br>
Prof. Gilles Louppe<br>
[g.louppe@uliege.be](mailto:g.louppe@uliege.be)

???

R: check https://www.youtube.com/watch?v=z8937RleAZo

R: lecun https://www.facebook.com/konbinitechno/videos/916293425386640/UzpfSTcyMjY3NzE0MjoxMDE1NjEyNjg2MzYwMjE0Mw/

R: What is Intelligence? Quote from Van Neuman

http://ai.stanford.edu/~nilsson/QAI/qai.pdf

R: tesla crash prevention

---

# Today

- Course outline
- Introduction to Artificial Intelligence
- Intelligent agents

---

class: middle

# Artificial intelligence

---

class: middle, center

.width-70[![](figures/lec0/terminator.png)]

"With artificial intelligence we are summoning the demon" -- Elon Musk

---

class: middle, center

.width-60[![](figures/lec0/washing-machine.png)]

"We're really closer to a smart washing machine than Terminator" -- Fei-Fei Li, Director of Stanford AI Lab.

---

# What is AI?

--

count: false

Artificial intelligence is the science of making machines or programs that:
.center.grid[
.kol-1-4[]
.kol-1-4[
.caption[Think like people]
.width-100[![](figures/lec0/ai-think-people.png)]
]
.kol-1-4[
.caption[Think rationally]
.width-100[![](figures/lec0/ai-think-rationally.png)]
]
]
.grid[
.kol-1-4[]
.kol-1-4[
.caption[Act like people]
.width-100[![](figures/lec0/ai-act-people.png)]
]
.kol-1-4[
.caption[Act rationally]
.width-100[![](figures/lec0/ai-act-rationally.png)]
]
]

.footnote[Image credits: [CS188](http://ai.berkeley.edu/lecture_slides.html), UC Berkeley.]

---

# Acting humanly

## The Turing test

A computer passes the **Turing test** (aka the Imitation Game) if a human operator, after posing some written
questions, cannot tell whether the written responses come from a person or from
a computer.

.grid[
.kol-2-3[
.width-100[![The Turing test](figures/lec0/turing-test.jpg)]
]
.kol-1-3.center[
.width-100.circle[![Alan Turing](figures/lec0/alan-turing.jpg)]
.caption[Can machines think?<br> (Alan Turing, 1950)]
]
]

???

- The Turing test is an *operational* definition of intelligence.

---

class: middle

An agent would not pass the Turing test without the following **requirements**:

- natural language processing
- knowledge representation
- automated reasoning
- machine learning
- computer vision (total Turing test)
- robotics (total Turing test)

Despite being proposed almost 70 years ago, the Turing test is *still relevant*
today.

---

class: middle

## Limitations of the Turing test

The Turing test tends to focus on *human-like errors*, *linguistic tricks*, etc.

However, it seems more important to study the **principles** underlying intelligence than to replicate an exemplar.

<br>
.center.width-70[![](figures/lec0/cargo-plane.jpg)]
.caption[Aeronautics is not defined as the field of making machines<br> that fly
so exactly like pigeons that they can fool even other pigeons.]

---

# Thinking humanly

## Cognitive science

Study of the *human mind* and its processes.
- The goal of cognitive science
  is to form a theory about the structure of the mind, summarized as a comprehensive **computer
  model**.
- It includes language, problem-sovling, decision-making and perception.
- A *cognitive architecture* usually follows human-like reasoning and can be used to
produce testable predictions (time of delays during problem solving, kinds of
mistakes, learning rates, etc).

???

Grew out of psychology.

---

class: middle, center

.width-80[![ACT-R](figures/lec0/soar.jpg)]

.caption[The modern SOAR cognitive architecture.]

???

The SOAR architecture is both:
- a theory of cognition
- a computational implementation of that theory

---

class: middle

## Neuroscience

Study of the anatomy and physiology of neural tissue.
- Neurobiology is concerned with the the anatomy and physiology of the brain, from major structures down to neurons and molecules.
- Neuroscience adds to that the study of **how the brain works**, mechanistically, functionally, and systematically to produce observable behavior.

.center.width-50[![](figures/lec0/brain.png)]
.caption[Can we build a computer model of the brain?]

???

Grew out of clinical neurology and neurobiology.

---

class: middle

## Limitations of cognition and neuroscience for AI

.grid[
.kol-2-3[
- In linguistics, the argument of **poverty of the stimulus** states that children
do not receive sufficient input to generalize grammatical rules through
linguistic input alone.
    - A baby hears too few sentences to deduce the grammar of English before he speaks correctly.

- (Controversial) Therefore, humans must be *biologically pre-wired*
with **innate knowledge** for representing language.
]
.kol-1-3.center[
.circle.width-100[![Noam Chomsky](figures/lec0/chomsky.png)]
.caption[How do we know what we know? (Noam Chomsky, 1980)]
]
]

It may not be possible to implement a fully functioning
computer model of the human mind without background knowledge of some sort.
This is a huge technical **obstacle**, as accessing
this knowledge would require reverse-engineering the brain.

---

# Thinking rationally

## The logical approach

- The rational thinking approach is concerned with the study of *irrefutable
reasoning processes*. It ensures that all actions performed by a computer are
formally **provable** from inputs and prior knowledge.

- The "laws of thought" were supposed to govern the operation of the mind.
Their study initiated the field of *logic* and the *logicist tradition* of AI
(1960-1990).

---

class: middle

## The Zebra puzzle

.grid[
.kol-1-2[
- There are five houses.
- The English man lives in the red house.
- The Swede has a dog.
- The Dane drinks tea.
- The green house is immediately to the left of the white house.
- They drink coffee in the green house.
- The man who smokes Pall Mall has birds.
- In the yellow house they smoke Dunhill.
- In the middle house they drink milk.
]
.kol-1-2[
- The Norwegian lives in the first house.
- The man who smokes Blend lives in the house next to the house with cats.
- In a house next to the house where they have a horse, they smoke Dunhill.
- The man who smokes Blue Master drinks beer.
- The German smokes Prince.
- The Norwegian lives next to the blue house.
- They drink water in a house next to the house where they smoke Blend.
]
]

---

class: middle, center

Who owns the zebra?

---

class: middle

```prolog
select([A|As],S):- select(A,S,S1),select(As,S1).
select([],_).

next_to(A,B,C):- left_of(A,B,C) ; left_of(B,A,C).
left_of(A,B,C):- append(_,[A,B|_],C).

zebra(Owns, HS):-  % color,nation,pet,drink,smokes
      HS =    [ h(_,norwegian,_,_,_), _,  h(_,_,_,milk,_), _, _],
      select( [ h(red,englishman,_,_,_),  h(_,swede,dog,_,_),
                h(_,dane,_,tea,_),        h(_,german,_,_,prince) ], HS),
      select( [ h(_,_,birds,_,pallmall),  h(yellow,_,_,_,dunhill),
                h(_,_,_,beer,bluemaster) ],                         HS),
      left_of(  h(green,_,_,coffee,_),    h(white,_,_,_,_),         HS),
      next_to(  h(_,_,_,_,dunhill),       h(_,_,horse,_,_),         HS),
      next_to(  h(_,_,_,_,blend),         h(_,_,cats, _,_),         HS),
      next_to(  h(_,_,_,_,blend),         h(_,_,_,water,_),         HS),
      next_to(  h(_,norwegian,_,_,_),     h(blue,_,_,_,_),          HS),
      member(   h(_,Owns,zebra,_,_), HS).

:- ?- time(( zebra(Who, HS), maplist(writeln,HS), nl, write(Who), nl, nl, fail
             ; write('No more solutions.') )).
```

---

class: middle

Output =
```prolog
h(yellow,norwegian, cats,  water, dunhill)
h(blue,  dane,      horse, tea,   blend)
h(red,   englishman,birds, milk,  pallmall)
h(green, german,    zebra, coffee,prince)
h(white, swede,     dog,   beer,  bluemaster)

german

No more solutions.
% 5,959 inferences, 0.000 CPU in 0.060 seconds (0% CPU, Infinite Lips)
```

---

class: middle

## Limitations of logical inference

- Representation of *informal* knowledge is difficult.
- Hard to define provable *plausible* reasoning.
- *Combinatorial explosion* (in time and space).
- Logical inference is only a part of intelligence. It does not cover everything:
    - e.g., might be no provably correct thing to do, but still something must be done;
    - e.g., reflex actions can be more successful than slower carefully deliberated ones.

.center[![Pain withdrawal reflex](figures/lec0/reflex.jpg)]
.caption[Pain withdrawal reflexes do not involve inference.]

---

# Acting rationally

A **rational agent** acts so as to achieve the best (expected) outcome.
- Correct logical inference is just one of several possible mechanisms for achieving this goal.
- Perfect rationality cannot be achieved due to computational limitations!
  The amount of reasoning is adjusted according to available resources and importance of the result.
- The brain is good at making rational decisions but not perfect either.

---

class: middle

Rationality only concerns *what* decisions are made (not the thought process behind them, human-like or not).

Goals are expressed in terms of the **performance** or **utility** of outcomes. Being rational means maximizing its expected performance.
The standard of rationality is general and mathematically well defined.

---

class: middle

.center[![](figures/lec0/max-utility.png)

In this course, Artificial intelligence = **Maximizing expected performance**
]

.footnote[Image credits: [CS188](http://ai.berkeley.edu/lecture_slides.html), UC Berkeley.]

---

# AI prehistory

- *Philosophy:* logic, methods of reasoning, mind as physical system, foundations of learning, language, rationality.
- *Mathematics:* formal representation and proof, algorithms, computation, (un)decidability, (in)tractability, probability.
- *Psychology:* adaptation, phenomena of perception and motor control, psychophysics.
- *Economics:* formal theory of rational decisions.
- *Linguistics:* knowledge representation, grammar.
- *Neuroscience:* plastic physical substrate for mental activity.
- *Control theory:* homeostatic systems, stability, simple optimal agent designs.

---

# A short history of AI

## 1940-1950: Early days
- 1943: McCulloch and Pitts: Boolean circuit model of the brain.
- 1950: Turing's "Computing machinery and intelligence".


---

class: middle

## 1950-1970: Excitement and expectations
- 1950s: Early AI programs, including Samuel's checkers program,
Newell and Simon's Logic Theorist and Gelernter's Geometry Engine.
- 1956: Dartmouth meeting: "Aritificial Intelligence" adopted.
- 1958: Rosenblatt invents the perceptron.
- 1965: Robinson's complete algorithm for logical reasoning.
- 1966-1974: AI discovers computational complexity.

.center.width-70[![](figures/lec0/dartmouth.jpg)]

---

class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/aygSMgK3BEM" frameborder="0" allowfullscreen></iframe>

---

class: middle

## 1970-1990: Knowledge-based approaches
- 1969: Neural network research almost disappears after Minsky and Papert's book.
- 1969-1979: Early development of knowledge-based systems.
- 1980-1988: Expert systems industrial boom.
- 1988-1993: Expert systems industry busts  (AI winter).

---

class: middle

## 1990-Present: Statistical approaches
- 1985-1995: The return of neural networks.
- 1988-: Resurgence of probability, focus on uncertainty, general increase in technical depth.
- 1995-2010: New fade of neural networks.
- 1995-: Complete intelligent agents and learning systems.
- 2000-: Availability of very large datasets.
- 2010-: Availability of fast commodity hardware (GPUs).
- 2012-: Resurgence of neural networks with  deep learning approaches.

---

# What can AI do at present?

- Translate spoken Chinese to spoken English, live?
- Answer multi choice questions, as good as an 8th grader?
- Converse with a person for an hour?
- Play decently at Chess? Go? Poker? Soccer?
- Buy groceries on the web? in a supermarket?
- Prove mathematical theorems?
- Drive a car safely on a parking lot? in New York?
- Perform a surgery?
- Identify skin cancer better than a dermatologist?
- Write a funny story?
- Paint like Vangogh? Compose music?
- Show common sense?

---

class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/V1eYniJ0Rnk" frameborder="0" allowfullscreen></iframe>

Playing Atari games

---

class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/g-dKXOlsf98" frameborder="0" allowfullscreen></iframe>

Beat the best human Go players (2016)

---

class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/eHipy_j29Xw" frameborder="0" allowfullscreen></iframe>

Beat teams of human players at real-time strategy games (Dota 2) (2018)

---

class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/Nu-nlQqFCKg" frameborder="0" allowfullscreen></iframe>

Speech translation and synthesis (2012)

---

class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/qWl9idsCuLQ" frameborder="0" allowfullscreen></iframe>

Semantic segmentation (2017)

---

class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/8BFzu9m52sc" frameborder="0" allowfullscreen></iframe>

Generating image descriptions (2015)

---

class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/IvmLEq9piJ4" frameborder="0" allowfullscreen></iframe>

Detecting skin cancer (2017)

---

class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/gn4nRCC9TwQ" frameborder="0" allowfullscreen></iframe>

Learning to walk (2017)

???

Single algorithm for learning! Nothing is hardcoded.

Similar to a baby learning to walk.

---

class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/gy5g33S0Gzo" frameborder="0" allowfullscreen></iframe>

Folding laundry (2010)

---

class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/yyLa6xIK9Qs" frameborder="0" allowfullscreen></iframe>

Playing soccer (2018)

---

class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/-96BEoXJMs0" frameborder="0" allowfullscreen></iframe>

Driving a car (2016)

---

class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/hYZM5l0G28I" frameborder="0" allowfullscreen></iframe>

Learning to sort waste (Norman Marlier, ULiège, 2018)

---

count: false
class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/MsuS0gaSHJ0" frameborder="0" allowfullscreen></iframe>

Learning to sort waste (Norman Marlier, ULiège, 2018)

---

# What is missing?

Intelligence is not just about **pattern recognition**, which is something most of these works are based on.

It is about *modeling the world*:
- explaining and understanding what we see;
- imagining things we could see but haven't yet;
- problem solving and planning actions to make these things real;
- building new models as we learn more about the world.

---

class: end-slide, center
count: false

The end.

---

# References

- Turing, Alan M. "Computing machinery and intelligence." Mind 59.236 (1950): 433-460.
- Newell, Allen, and Herbert Simon. "The logic theory machine--A complex information processing system." IRE Transactions on information theory 2.3 (1956): 61-79.
- Chomsky, Noam. "Rules and representations." Behavioral and brain sciences 3.1 (1980): 1-15.
