# Pacman project folder

Credits: [UC Berkeley](http://ai.berkeley.edu/project_overview.html)
         [OpenAI Interface](https://github.com/sohamghosh121/PacmanGym)

## Generalities

Display the command-line help section


## How to launch the game (Part 1/3)
```bash
python run.py -h
```

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
