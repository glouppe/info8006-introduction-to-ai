# Project 2 - Neural Networks for imitation learning

## Deliverables

You are requested to deliver:
- A file named `architecture.py` containing the implementation of your neural network,
- A file named `data.py` containing the handling of the dataset,
- A file named `train.py` containing the training loop of your model,
- A file named `pacmanagent.py` containing the implementation of an agent whose decisions are based on the predictions of your model,
- A file named `submission.csv` containing the action predictions for each game state contained in the `pacman_test.pkl` file. The predictions must follow the same order as the states appear in `pacman_test.pkl`. A file `write_submission.py` and an example `example_submission.csv` is provided to help you write your predictions in the right format.
- A file named `pacman_model.pth` of your saved final model.
- A file named `run.py` allowing us to run your agent on a test layout.

## Installation and preparation

The following packages must be installed in your `pacman` environment to successfully complete this project:
```console
$ conda activate pacman
$ conda install pytorch 
$ conda install pandas
```
To get familiar with the PyTorch library, neural networks and how to train them, we have provided a completed notebook [`mnist.ipynb`](./mnist.ipynb) that solves an inpainting task on the MNIST dataset using a multi-layer perceptron (MLP).

You also saw during [Lecture 7](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture7.md) the comparison between an MLP and a CNN ([`lecture7-convnet.ipynb`](../../code/lecture7-convnet.ipynb)) and a multi-class classification task ([`lecture7-spiral.ipynb`](../../code/lecture7-spiral.ipynb)).

You may use our implementations as inspiration, but be careful: the task and data format may differ in this project.

## Instructions

In this project, Pacman got tired of having to learn a strategy against a smarty ghost on his own. He therefore wants to base his actions on those of an expert, and decides to learn to imitate him in order to achieve the best possible score without getting caught.

He disposes of a dataset `pacman_dataset.pkl` containing GameState-action pairs taken by the expert.

Your task is to perform **imitation learning** (see [Lecture 7](https://glouppe.github.io/info8006-introduction-to-ai/?p=lecture7.md)) on the expert's actions in order to achieve the best possible score while avoiding a walking ghost that would kill him if it reaches his position.

You need to:
- Handle the dataset and extract relevant features from the complete GameState object (see [pacman.py](pacman_module/pacman.py) file for more information). The class `PacmanDataset` may be completed accordingly.
- Design a neural network which takes the features you derived from the GameState as input and outputs the prediction for the next action to be taken. The class `PacmanNetwork` may be completed accordingly.
- Train your architecture. The class `Pipeline` may be completed accordingly. Think about a strategy for evaluating your trained model. You can run your training algorithm simply using 
```console
$ python train.py 
```
- Design an agent that will take actions based on the predictions of your network. You must complete the `pacmanagent.py` file. To vizualise the performance of your imitation learning agent on a layout, you must complete the `run.py` file according to your `train.py` and `pacmanagent.py` implementation and use the command 
```console
$ python run.py 
```
to see your agent perform in a game. Pay attention that the score obtained by your agent on a test layout does **NOT** reflect its performance compared to that of the expert it is trying to imitate, and therefore does not represent the score obtained on the leaderboard. 


To get started, download and extract the [archive](../project2.zip?raw=true) of the project in the directory of your choice. 

**Note:** by “*may be completed accordingly,*” we mean that we are proposing a structure for your code. The use of our structure is entirely optional and is provided solely for your convenience. 


## Leaderboard

The goal of the competition is to reach the best accuracy on the test set provided in `pacman_test.pkl`. This test set only contains GameState objects without the associated actions. 
Your predictions computed on the data in `pacman_test.pkl` can be submitted multiple times on Gradescope, where a leaderboard will allow you to compare your methods to other groups. A function to write your results in a CSV file is provided in `write_submission.py`.
When submitting *during the competition* (before the deadline), your **public** score will be computed on 50% of the total test set. 
*Once the competition is over*, new **private** scores will be computed on the remaining 50% of the test set. **Only the private scores will count as the final scores.**


## Evaluation

Your project will be evaluated as follow:

- **Accuracy of your predictions on a private test set** (75%): 
- **Code** (25%):
    - **Feature engineering**: We evaluate the reasoning behind your feature selection/engineering.
    - **Architecture**: We evaluate the design of your architecture (originality/suitability for the task).
    - **Training loop**: We evaluate your training strategy.
    - **Agent**: We evaluate how your agent takes actions based on your predictions (we check if your `run.py` file runs with your model `pacman_model.pth`).
    - **Style** (5%): You are awarded the maximal grade if your code is PEP-8 compliant and no points otherwise. This test is public.

- A bonus will be awarded based on your position in the **private leaderboard**. This bonus is worth 1 point for first place and decreases linearly to last place. 


### Oral exam

The evaluation of the projects will also include a short oral exam (5-10 min per student). Our goal is not to re-assess the projects themselves, but rather to ensure that each student can explain and justify the choices made in the projects (algorithms or models) as well as their implementation details (code). In an era where AI tools can do more than ever, we believe it is critical that you demonstrate your own understanding and skills.

We will design the oral exam such that it should be a formality for students who have worked properly on the projects by themselves. This means that you should be able to discuss your work confidently and clearly. This oral exam will be individual (not in groups).

If you pass the oral exam, you will receive the project grades as assigned. If you fail the oral exam, your project grades will be set to zero.

The oral exams will take place during the last week of December. A schedule will be shared in due course.
