import pickle

import torch
import torch.nn as nn

from architecture import PacmanNetwork
from data import PacmanDataset


class Pipeline(nn.Module):
    def __init__(self, path):
        """
        Initialize your training pipeline.

        Arguments:
            path: The file path to the pickled dataset.
        """
        super().__init__()

        self.path = path
        self.dataset = PacmanDataset(self.path)
        self.model = PacmanNetwork()

        self.criterion = # ...
        self.optimizer = # ...

    def train(self):
        print("Beginning of the training of your network...")

        # Your code here

        torch.save(self.model.state_dict(), "pacman_model.pth")
        print("Model saved !")


if __name__ == "__main__":
    pipeline = Pipeline(path="pacman_dataset.pkl")
    pipeline.train()
