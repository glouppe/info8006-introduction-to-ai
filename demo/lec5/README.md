# Lecture 5 demo: estimating the fraction of cherry candies

The parameter learning section of lecture 5, run step by step on the candy
example: draw candies from a Bernoulli of parameter $\theta$, estimate
$\theta$ by maximum likelihood, then by Bayesian updating of a Beta prior,
and watch the posterior concentrate as the sample grows.

## Running

From the repository root, with the project environment:

```bash
uv run jupyter lab demo/lec5/cherries.ipynb
```

The notebook needs `numpy`, `scipy` and `matplotlib`, all in the environment.

## What it shows

| Case | |
| --- | --- |
| (a) | one parameter, the fraction $\theta$ of cherries: likelihood, log-likelihood, and the maximum at $c/N$ |
| (b) | the Bayesian view: a Beta prior, the posterior after each candy, and the MAP estimate |

It is the same example as the slides, so the numbers on the board and in the
notebook agree.
