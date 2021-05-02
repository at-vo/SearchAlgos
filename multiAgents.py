# multiAgents.py
# --------------
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


import random

import util
from game import Agent, Directions  # noqa
from util import manhattanDistance  # noqa


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # print("succ:\n",successorGameState)
        # print("newpos:",newPos)
        # print("newfood:",newFood)
        # print("ghstates:",newGhostStates)
        #print("scareTime:",newScaredTimes)
        
        # define variables
        high = float('inf')
        low = -high
        newFoodList = newFood.asList()
        nextFood = high
        toReturn = 0
        
        #print("foodlist: ",newFoodList)
        # make it go if pacman stops
        if action == "Stop":
            return low

        # find the lowest food distance using manhattan
        for pos in newFoodList:
            dist = manhattanDistance(newPos,pos)
            if dist < nextFood:
                nextFood = dist 
        # ghostPos = currentGameState.getGhostPositions()
        # print(nextFood)

        # make food a higher priority if on scared timer
        # for time in newScaredTimes:
        #     if time > 0:
        #         nextFood += 2
        minGhostPos = high
        for ghost in newGhostStates:
            currGhostPos = manhattanDistance(newPos,ghost.getPosition())
            if currGhostPos < minGhostPos:
                minGhostPos = currGhostPos
        #print(minGhostPos)
        # make pacman run away from ghost
        if minGhostPos < 2:
            #print("oh no!")
            return low
        # take the reciprocal of the good value
        toReturn = 1/nextFood
        # print("succscore:", successorGameState.getScore())
        # print("currscore:", currentGameState.getScore())

        diffScore = successorGameState.getScore() - currentGameState.getScore()
        #print("diffScore: ",diffScore)
        toReturn += diffScore
        

        return toReturn


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn="scoreEvaluationFunction", depth="2"):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        
        # define a recursive call for minMax comparison
        def minMaxFunction(gameState, agentIndex, depth):
            # common return for win/lose or specified depth
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            # maximize pacman position
            if agentIndex == 0:
                # assign lowest value to compare to first
                toReturn = float('-inf')
                # find the highest value for the current depth and index
                for state in gameState.getLegalActions(agentIndex):
                    minMax = minMaxFunction(gameState.generateSuccessor(agentIndex,state),1,depth)
                    # check max
                    if minMax > toReturn:
                        toReturn = minMax
                return toReturn

            # minimize ghost positions
            else:
                # # check next index
                nextIndex = agentIndex + 1
                if gameState.getNumAgents() == nextIndex:
                    nextIndex = 0
                if nextIndex == 0:
                   depth += 1
                # do same as max but for min
                toReturn = float('inf')
                for state in gameState.getLegalActions(agentIndex):
                    minMax = minMaxFunction(gameState.generateSuccessor(agentIndex,state),nextIndex,depth)
                    if minMax < toReturn:
                        toReturn = minMax
                return toReturn
        # evaluate pacman position at root as a maximum
        toReturn = 0
        maxValue = float('-inf')
        # for initial action
        for state in gameState.getLegalActions(0):
            minMax = minMaxFunction(gameState.generateSuccessor(0,state), 1, 0)
            # find minimum value and then set toReturn to min
            if minMax > maxValue:
                maxValue = minMax
                toReturn = state
        return toReturn
        


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
