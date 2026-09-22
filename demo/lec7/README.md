# Lecture 7 demos

The two notebooks of the live coding sessions, adapted from
[Deep Learning (with PyTorch)](https://github.com/Atcold/pytorch-Deep-Learning)
by Alfredo Canziani.

## Logistic regression and MLPs on a spiral

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
| Linear model with a softmax output | 0.55 |
| MLP, one hidden layer of 100 units | 0.98 |

No linear model does better than chance here. The last cell lists what to vary
live: the non-linearity, the width, the depth and the activation function.

## MLP against ConvNet on MNIST

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
