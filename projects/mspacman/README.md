# Pacman project folder

Credits: [UC Berkeley](http://ai.berkeley.edu/project_overview.html)

## How to launch the game

Launches an interactive game:
```bash
python pacman.py
```

Launches a game with your Pacman class, located in `youragentmodule.py`, and with the maze tinyMaze (see layout folder).
 /!\ The agent module name is the same as the class name but with the first capitalized letter.
     E.g. if the module `agent523821` is provided then the class `Agent523821` will be imported.
```bash
python pacman.py -l tinyMaze -p youragentmodule
```

Same configuration as above including at most `n` ghosts. Note that the final number of ghosts is the minimum
between the number of ghosts defined in the maze and `n`. *Set `n` to 0 to play in search mode only.*
```bash
python pacman.py -l tinyMaze -p youragentmodule --numghosts n
```

Same configuration as above, but defining the pattern of the ghosts (here a random ghost).
```bash
python pacman.py -l tinyMaze -p youragentmodule --numghosts n -g randyghost
```

See the help section of the command line for more information about the parameters.

## Scoring

The score function is computed as follows:

`score = -#time steps + 10*#number of food dots eaten + 200*#ghost_eaten + (-500 if lose else 500)`

(See `pacman.py` for more details.)
