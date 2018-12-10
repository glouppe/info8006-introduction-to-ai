class: middle, center, title-slide

# Introduction to Artificial Intelligence

Lecture 10: Communication

<br><br>
Prof. Gilles Louppe<br>
[g.louppe@uliege.be](g.louppe@uliege.be)

???

R: check KC tuto on NLP

R: check https://gitlab.com/Valiox/voice-transfer-across-languages
https://drive.google.com/file/d/1Q8SIQi57r6N5wvc4IPTxv0_tQ-D0K3Fb/view


http://lxmls.it.pt/2017/talk.pdf

---

# Today



.grid[
.kol-2-3[
Can you **talk** to an artificial agent? Can it understand what it hears?

- Machine translation
- Speech recognition
- Speech synthesis
]
.kol-1-3[
.center.width-100[![](figures/lec10/robot-speech.png)]
]
]

.footnote[Image credits: [CS188](http://ai.berkeley.edu/lecture_slides.html), UC Berkeley.]

---

class: middle

# Machine translation

???

R: check 23.4

---

class: middle

.center.width-100[![](figures/lec10/translate.png)]

## Machine translation

Automatic translation of text from one natural language (the source) to another (the target), while preserving the intended meaning.

<span class="Q">[Q]</span> How would engineer a machine translation system?

---

class: middle

## Issue of dictionary lookups

.center.width-90[![](figures/lec10/lookups.png)]

.footnote[Image credits: [CS188](http://ai.berkeley.edu/lecture_slides.html), UC Berkeley.]

---

class: middle

.center.width-100[![](figures/lec10/translate-soccer.png)]

.center[To obtain a correct translation, one must decide whether "it" refers to the soccer ball or to the window. Therefore, one must understand physics as well as language.]

---

# History

.center.width-100[![](figures/lec10/history.png)]

.footnote[Image credits: [CS188](http://ai.berkeley.edu/lecture_slides.html), UC Berkeley.]

???

R: review

---

# Data-driven machine translation

<br>
.center.width-100[![](figures/lec10/data-driven-mt.png)]

.footnote[Image credits: [CS188](http://ai.berkeley.edu/lecture_slides.html), UC Berkeley.]

---

class: middle

## Machine translation systems

Translation systems must model the source and target languages, but systems vary in the type of models they use.
- Some systems attempt to analyze the source language text all the way into an interlingua knowledge representation and then generate sentences in the target language from that representation.
- Other systems are based on a *transfer model*. They keep a database of translation rules and whenever the rule matches, they translate directly. Transfer can occur at the lexical, syntactic or semantic level.

---

class: middle

.center.width-100[![](figures/lec10/vauquois.png)]

---

# Statistical machine translation

To translate an English sentence $e$ into a French sentence $f$, we seek the strings of words $f^\*$ such that
$$f^\* = \arg\max\_f P(f|e).$$

- The language model $P(f|e)$ is learned from a **bilingual corpus**, i.e. a collection of parallel texts, each an English/French pair.
- Most of the English sentences to be translated will be novel, but will be composed of phrases that that have been see before.
- The corresponding French phrases will be reassembled to form a French sentence that make sense.

---

class: middle

Given an English source sentence $e$, finding a French translation $f$ is a matter of three steps:
- Break $e$ into phrases $e\_1, ..., e\_n$.
- For each phrase $e\_i$, choose a corresponding French phrase $f\_i$. We use the notation $P(f\_i|e\_i)$ for the phrasal probability that $f\_i$ is a translation of $e\_i$.
- Choose a permutation of the phrases $f\_1, ..., f\_n$. For each $f\_i$, we choose a *distortion* $d\_i$, which is the number of words that phrase $f\_i$ has moved with respect to $f\_{i-1}$; positive for moving to the right, negative for moving the left.

---

class: middle

.center.width-100[![](figures/lec10/translation-wumpus.png)]

---

class: middle

We define the probability $P(f,d|e)$ that the sequence of phrases $f$ with distortions $d$ is a translation of the sequence of phrases $e$.

Assuming mutual independence of each phrase translation and each distortion, we have
$$P(f,d|e) = \prod\_i P(f\_i | e\_i) P(d\_i).$$

- The best $f$ and $e$ cannot be found through enumeration because of the combinatorial explosion.
- Instead, local bearm search with a heuristic that estimates probability has proven effective at finding a nearly-most-probable translation.

---

class: middle

All that remains is to learn the phrasal and distortion probabilities:
1. Find parallel texts.
2. Segment into sentences.
3. Align sentences.
4. Align phrases.
5. Extract distortions.
6. Improve estimates with expectation-minimization.


---

# Neural machine translation

Modern machine translation systems are all based on neural networks of various types.

<br>

.center.width-80[![](figures/lec10/gnmt.jpg)]

---

class: middle

## Attention-based recurrent neural network

.grid[
.kol-1-2[
- Encoder: bidirectional RNN, producing a set of annotation vectors $h\_i$.
- Decoder: attention-based.
    - Compute attention weights $\alpha\_{ij}$.
    - Compute the weighted sum of the annotation vectors, as a way to align the input words to the output words.
    - Decode using the context vector, the embedding of the previous output word and the hidden state.
]
.kol-1-2[
.center.width-100[![](figures/lec10/nmt.png)]
]
]

---

class: middle

## Unsupervised machine translation

- The latest approaches do not even need to have a bilingual corpus!
- Machine translation can be learned in a **fully unsupervised** way with unsupervised alignment.

---

class: middle

Word-by-word translation:
- Learn word embedding trained to predict the words around a given word using a context.
- Embedding in different languages share similar neighborhood structure.
- The system learn rotation of the word embedding in one language to match the word embedding in the other language, using adversarial training.
- This can be used to infer a fairly accurate bilingual dictionary without access to any translation!

.center.width-60[![](figures/lec10/umt-word-by-word.gif)]

.footnote[Image credits: [Facebook AI Research](https://code.fb.com/ai-research/unsupervised-machine-translation-a-novel-approach-to-provide-fast-accurate-translations-for-more-languages/), Unsupervised machine translation.]

---

class: middle

Translating sentences
- The translation model must be able to reconstruct a sentence in a given language from a noisy version of it.
- The model also learns to reconstruct any source sentence given a noisy translation of the same sentence in the target domain, and vice-versa.
- The source and target sentence latent representations are constrained to have the same latent distributions through adversarial training.

.center.width-90[![](figures/lec10/umt1.png)]

.footnote[Image credits: [Lample et al, arXiv:1711.00043](https://arxiv.org/pdf/1711.00043.pdf).]



???

R: improve, make it more intuitive, work on the figures

https://code.fb.com/ai-research/unsupervised-machine-translation-a-novel-approach-to-provide-fast-accurate-translations-for-more-languages/


---

class: middle

# Speech recognition

???

R: check 23.5
R: check lec 15 of bair

---

---


class: middle

# Speech synthesis

---

# Summary

---

class: end-slide, center
count: false

The end.

---

# References
