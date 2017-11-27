Pac man project folder

Credits : UC Berkeley

See following link : http://ai.berkeley.edu/project_overview.html

Scoring : -#time steps + 10*#number of food dots eaten + 200*#ghost_eaten + (-500 if lose else 500)

How to launch the game : 

 > python pacman.py
	-> Launches an interactive game

 > python pacman.py -l tinyMaze -p youragentmodule
	-> Launches a game with your pacman class, located in youragentmodule, and with the maze tinyMaze (see layout folder).
	   /!\ The agent module name is the same as the class name but with the first capitalized letter
	   e.g. if the module agent523821 is provided then the class Agent523821 will be imported 

 > python pacman.py -l tinyMaze -p youragentmodule --numghosts n
	-> Same configuration as above including at most n ghosts. Note that the final number of ghosts is the minimum
	   between the number of ghosts defined in the maze and n 

  > python pacman.py -l tinyMaze -p youragentmodule --numghosts n -g randyghost
	-> Same configuration as above defining the pattern of the ghosts (here a random ghost)

Please see help section of the command line for more information about the parameters.
