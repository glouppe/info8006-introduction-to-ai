# Lecture 7 demos

## Shallow network, interactive

`shallow.html` is shown on two full slides: `?mode=build` after the family of piecewise linear
functions, `?mode=approximate` after the universal approximation theorem (without the parameter, both
modes are available as tabs). It is a plain
web page (no dependency beyond the KaTeX files of `assets/`), in the notation of the slides: a
network with one input, one output and $q$ ReLU hidden units, $h_j = \text{ReLU}(w_j x + b_j)$ and
$y = \sum_j v_j h_j + c$, on $[0, 1]$.

- *build*: one to four units, each with sliders for $w_j$, $b_j$ and $v_j$, plus $c$. It draws the
  network (edge width with the weight, dashed when negative), the hidden units with their joints
  at $x = -b_j / w_j$, and the output as the sum of the weighted units.
- *approximate*: up to 40 units, whose joints are spread evenly over the interval; the output
  weights and $c$ are fitted by least squares to a target (a bump, a wave, or a ramp and a dip),
  and the RMS error falls as $q$ grows, which is the universal approximation theorem at work.

Open it on its own with the deck server running: `http://localhost:8000/demo/lec7/shallow.html`.

## Shallow network with two inputs

`shallow2d.html` follows the figure of the units of a network with two inputs: the same network, with
inputs $x_0$, $x_1$, one to four ReLU units and sliders for $w_{j0}$, $w_{j1}$, $b_j$, $v_j$ and $c$,
opening on the figure's parameters. It draws the network, each unit $h_j(x_0, x_1)$ and the output
$y = \sum_j v_j h_j + c$ over $[-1, 1]^2$, on the figures' diverging scale (blue positive, orange
negative, white at zero), with the joint of each unit dashed in its color, and counts the linear regions
of $y$ as the distinct on/off patterns of the units (7 for the three units of the figure, at most
$1 + q + q(q-1)/2$).

## Folding

`fold.html` animates the slide on the composition of two shallow networks, in place of Prince's
figure. The first network $y = f(x)$, three ReLU units, is a zigzag whose three pieces each cover the
whole range, so that it folds the input interval onto itself in three layers; the second, $y' = g(y)$,
is another three-unit network. The animation loops through the slide's three steps on the input space drawn as a
sheet of paper in oblique projection, one panel per piece of $f$: a) the sheet folds like an accordion,
b) $g$ is drawn on the folded sheet, c) the sheet unfolds and reveals $g(f(x))$, the pattern of $g$ three times, mirrored on the descending piece. Small plots of
$f$, $g$ and $g \circ f$ sit above it; the slider scrubs through the animation.

## Notebooks

The two notebooks of the live coding sessions, adapted from
[Deep Learning (with PyTorch)](https://github.com/Atcold/pytorch-Deep-Learning)
by Alfredo Canziani.

Both need PyTorch, which is an extra of the course environment:

```bash
uv sync --extra torch
```

### Logistic regression and MLPs on a spiral

Two classes of points in the plane, wound into a spiral. The notebook trains,
in turn, logistic regression, its multiclass version with a softmax output,
and an MLP, drawing the decision regions as training goes. It is used twice
in the lecture: after gradient descent, for logistic regression, and after the
training section, for MLPs.

```bash
uv run jupyter lab demo/lec7/spiral.ipynb
```

| Model | Accuracy after 2000 steps |
| --- | --- |
| Logistic regression | 0.48 |
| Linear model with a softmax output | 0.48 |
| MLP, one hidden layer of 100 units | 0.99 |

No linear model does better than chance here. The last cell lists what to vary
live: the non-linearity, the width, the depth and the activation function.

### MLP against ConvNet on MNIST

An MLP and a convolutional network with the same number of parameters (about
6,400), trained for one epoch on MNIST, then again with the pixels of every
image shuffled by the same permutation.

```bash
uv run jupyter lab demo/lec7/convnet.ipynb
```

| Model | Test accuracy | Pixels shuffled |
| --- | --- | --- |
| MLP | 0.886 | 0.886 |
| ConvNet | 0.966 | 0.870 |

The ConvNet wins as long as neighboring pixels are neighbors in the input.
Shuffling costs the MLP nothing, since it ignores where pixels are, and the
ConvNet its advantage.

MNIST (12 MB to download, 64 MB unpacked) goes to `demo/lec7/data/` on the
first run; the folder is git-ignored.
