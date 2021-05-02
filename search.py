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

import util

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

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # for clear reference to items returned by succesors 
    nextState, nextAction, nextCost = 0, 1, 2
    # init lists
    visited = []
    stack = util.Stack()
    # assign current to start, the actions container, and the cost 
    current = problem.getStartState()
    container = []
    # push start
    stack.push((current,container))
    while not stack.isEmpty():
        # return actions if goal found
        if (problem.isGoalState(current)):
            return container
        
        if current not in visited:
            # visit if unvisited
            visited.append(current)
            # add each successor 
            for successor in problem.getSuccessors(current):
                stack.push((successor[nextState],container + [successor[nextAction]]))
        current, container = stack.pop()
    util.raiseNotDefined()
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #    # for clear reference to items returned by succesors 

    # for clear reference to items returned by succesors 
    nextState, nextAction, nextCost = 0, 1, 2
    # init lists
    visited = []
    queue = util.Queue()
    # assign current to start, the actions container, and the cost 
    current = problem.getStartState()
    container = []
    # push start
    queue.push((current,container))
    while not queue.isEmpty():
        current, container = queue.pop()

        # return actions if goal found
        if (problem.isGoalState(current)):
            return container
        # add each successor 
        if current not in visited:
            visited.append(current)
            for successor in problem.getSuccessors(current):
                queue.push((successor[nextState],container + [successor[nextAction]]))
        
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    
    nextState, nextAction, nextCost = 0, 1, 2
    visited = []
    # use priority queue this time
    queue = util.PriorityQueue()
    current = problem.getStartState()
    # add total cost variable
    totalCost = 0
    container = []
    # add total cost variable to visited and queue
    queue.push((current,container),totalCost)
    while not queue.isEmpty():
        current, container = queue.pop()
        if (problem.isGoalState(current)):
                return container
        if current not in visited:
            for succesor in problem.getSuccessors(current):
                # push the new action cost
                newAction = container + [succesor[nextAction]]
                queue.push((succesor[nextState], newAction), problem.getCostOfActions(newAction))
        visited.append(current)     
    return container
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    nextState, nextAction, nextCost = 0, 1, 2
    visited = []
    queue = util.PriorityQueue()
    current = problem.getStartState()
    # add total cost variable
    totalCost = 0
    container = []
    # add total cost variable to visited and queue
    queue.push((current,container), totalCost)
    while not queue.isEmpty():
        current, container = queue.pop()
        if problem.isGoalState(current):
                return container
        if current not in visited:
            for succesor in problem.getSuccessors(current):
                if succesor[nextState] not in visited: 
                    newAction = container + [succesor[nextAction]]
                    # add a total cost to UCS from above that takes into account the heuristic
                    totalCost = problem.getCostOfActions(newAction) + heuristic(succesor[nextState],problem)
                    queue.push((succesor[nextState], newAction), totalCost)
        visited.append(current)     
    return container
    util.raiseNotDefined()
    


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
