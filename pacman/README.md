# Pacman project folder

Credits: [UC Berkeley](http://ai.berkeley.edu/project_overview.html)
         [OpenAI Interface](https://github.com/sohamghosh121/PacmanGym)

## Generalities

All the instructions below have been tested under Linux and should work for MacOS.

See [Anaconda webpage](https://conda.io/docs/user-guide/install/index.html) for instructions to install Anaconda/Miniconda (recommended)

Create your own Anaconda environment and activate it
```bash
conda create -n <env_name> python=3.6
source activate <env_name>
```

From now, it is assumed that <env_name> is activated. 

Dependencies
```bash
pip install -U gym numpy stopit argparse
```

Display the command-line help section
```bash
python run.py -h
```

Install and use pycodestyle to check PEP8 compliance of Python scripts
```bash
pip install -U pycodestyle
pycodestyle <yourscript>.py
```

Install and use autopep8 to rewrite Python scripts into PEP8 format
```bash
pip install -U autopep8
autopep8 --in-place --aggressive --aggressive <yourscript>.py
```

/!\ Check your file again with pycodestyle

## How to launch the game (Part 1/3)


Launches a game with a random agent in default map mediumClassic:
```bash
python run.py
```

Launches a game with your Pacman agent class, named PMAgent located in `youragentmodule.py`, and with the maze originalClassic (see layout folder).
```bash
python run.py --layout originalClassic --agentfile youragentmodule.py
```
 - e.g., python run.py --layout originalClassic --agentfile human.py launches the keyboard agent, allowing the user to directly play the game.

Same configuration as above, but skip the call to `registerInitialState` method.
```bash
python run.py --layout mediumClassic --agentfile youragentmodule.py --onlyonline
```


See the help section of the command line for more information about the parameters.

## Scoring

The score function is computed as follows:

`score = -#time steps + 10*#number of food dots eaten + (500 when finished)`
