# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from . import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState() ============(5,5)
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())   ============True
    print "Start's successors:", problem.getSuccessors(problem.getStartState())  ===========[((x1,y1),'South',1),((x2,y2),'West',1)]
    """
    "*** YOUR CODE HERE ***"
    from game import Directions

    #initialization
    fringe = util.Stack()
    visitedList = []

    #push the starting point into stack
    fringe.push((problem.getStartState(),[],0))
    #pop out the point
    (state,toDirection,toCost) = fringe.pop()
    #add the point to visited list
    visitedList.append(state)

    while not problem.isGoalState(state): #while we do not find the goal point
        successors = problem.getSuccessors(state) #get the point's successors
        for son in successors:
            if (not son[0] in visitedList) or (problem.isGoalState(son[0])): # if the successor has not been visited,push it into stack
                fringe.push((son[0],toDirection + [son[1]],toCost + son[2])) 
                visitedList.append(son[0]) # add this point to visited list
        (state,toDirection,toCost) = fringe.pop()

    return toDirection

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from game import Directions

    #initialization
    fringe = util.Queue()
    visitedList = []

    #push the starting point into queue
    fringe.push((problem.getStartState(),[],0))
    #pop out the point
    (state,toDirection,toCost) = fringe.pop()
    #add the point to visited list
    visitedList.append(state)

    while not problem.isGoalState(state): #while we do not find the goal point
        successors = problem.getSuccessors(state) #get the point's successors
        for son in successors:
            if not son[0] in visitedList: # if the successor has not been visited,push it into queue
                fringe.push((son[0],toDirection + [son[1]],toCost + son[2])) 
                visitedList.append(son[0]) # add this point to visited list
        (state,toDirection,toCost) = fringe.pop()

    return toDirection



def iterativeDeepeningSearch(problem):
    """This function is for the first of the grad students questions"""
    "*** MY CODE HERE ***"
    from game import Directions

    #initialization
    fringe = util.Stack()
    limit = 1;

    while True: # repeat search with the depth increases until we find the goal
        visitedList = []
        #push the starting point into stack
        fringe.push((problem.getStartState(),[],0))
        #pop out the point
        (state,toDirection,toCost) = fringe.pop()
        #add the point to visited list
        visitedList.append(state)
        while not problem.isGoalState(state): #while we do not find the goal point
            successors = problem.getSuccessors(state) #get the point's succesors
            for son in successors:
                # add the points when it meets 1. not been visited 2. within the depth 
                if (not son[0] in visitedList) and (toCost + son[2] <= limit): 
                    fringe.push((son[0],toDirection + [son[1]],toCost + son[2])) 
                    visitedList.append(son[0]) # add this point to visited list

            if fringe.isEmpty(): # if the no goal is found within the current depth, jump out and increase the depth
                break

            (state,toDirection,toCost) = fringe.pop()

        if problem.isGoalState(state):
            return toDirection

        limit += 1 # increase the depth


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from game import Directions

    #initialization
    fringe = util.PriorityQueue() 
    visitedList = []

    #push the starting point into queue
    fringe.push((problem.getStartState(),[],0),0) # push starting point with priority num of 0
    #pop out the point
    (state,toDirection,toCost) = fringe.pop()
    #add the point to visited list
    visitedList.append((state,toCost))

    while not problem.isGoalState(state): #while we do not find the goal point
        successors = problem.getSuccessors(state) #get the point's succesors
        for son in successors:
            visitedExist = False
            total_cost = toCost + son[2]
            for (visitedState,visitedToCost) in visitedList:
                # we add the point only if the successor has not been visited, or has been visited but now with a lower cost than the previous one
                if (son[0] == visitedState) and (total_cost >= visitedToCost): 
                    visitedExist = True # point recognized visited
                    break

            if not visitedExist:        
                # push the point with priority num of its total cost
                fringe.push((son[0],toDirection + [son[1]],toCost + son[2]),toCost + son[2]) 
                visitedList.append((son[0],toCost + son[2])) # add this point to visited list

        (state,toDirection,toCost) = fringe.pop()

    return toDirection

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from game import Directions

    #initialization
    fringe = util.PriorityQueue() 
    visitedList = []

    #push the starting point into queue
    fringe.push((problem.getStartState(),[],0),0 + heuristic(problem.getStartState(),problem)) # push starting point with priority num of 0
    #pop out the point
    (state,toDirection,toCost) = fringe.pop()
    #add the point to visited list
    visitedList.append((state,toCost + heuristic(problem.getStartState(),problem)))

    while not problem.isGoalState(state): #while we do not find the goal point
        successors = problem.getSuccessors(state) #get the point's succesors
        for son in successors:
            visitedExist = False
            total_cost = toCost + son[2]
            for (visitedState,visitedToCost) in visitedList:
                # if the successor has not been visited, or has a lower cost than the previous one
                if (son[0] == visitedState) and (total_cost >= visitedToCost): 
                    visitedExist = True
                    break

            if not visitedExist:        
                # push the point with priority num of its total cost
                fringe.push((son[0],toDirection + [son[1]],toCost + son[2]),toCost + son[2] + heuristic(son[0],problem)) 
                visitedList.append((son[0],toCost + son[2])) # add this point to visited list

        (state,toDirection,toCost) = fringe.pop()

    return toDirection


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ids = iterativeDeepeningSearch
