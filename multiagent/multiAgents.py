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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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
        oldFood = currentGameState.getFood()
        #print('*****')
        #print(successorGameState)
        #print(newPos)
        #print(newFood)
        #print(newGhostStates[0].getPosition())
        #print(newScaredTimes)
        #print('*****')
        for ghost in newGhostStates:
            if util.manhattanDistance(ghost.getPosition(), newPos) < 2:
                return -9999
        
        if oldFood[newPos[0]][newPos[1]] == 'T':
            return 200
        
        score = 0
        for food in oldFood.asList():
            score = max(score, 200 / (util.manhattanDistance(food, newPos) + random.randrange(1, 2)))

        "*** YOUR CODE HERE ***"
        return score

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        return self.getValue(1, gameState)[1]

    def getValue(self, depth, gameState):
        if depth % gameState.getNumAgents() == 1:
            if gameState.isWin() or gameState.isLose() or depth == gameState.getNumAgents() * self.depth + 1:
                return self.evaluationFunction(gameState), 'Left'
            key = max
            score = -99999
        else:
            if gameState.isLose() or gameState.isWin() or depth == gameState.getNumAgents() * self.depth + 1:
                return self.evaluationFunction(gameState), 'Left'
            key = min
            score = 99999
        
        agentIndex = (depth-1) % gameState.getNumAgents()
        legalActions = gameState.getLegalActions(agentIndex)
        direction = legalActions[0]
        for action in legalActions:
            oldScore = score
            score = key(score, self.getValue(depth+1, gameState.generateSuccessor(agentIndex, action))[0])
            if score != oldScore:
                direction = action
        return score, direction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()

        def maxValue(depth, gameState, alpha, beta):
            """
            :return value and action
            :rtype float, str
            """
            if gameState.isWin() or gameState.isLose() or depth == gameState.getNumAgents() * self.depth + 1:
                return self.evaluationFunction(gameState), 'Left'

            v = -oo 
            agentIndex = (depth - 1) % gameState.getNumAgents()
            actions = gameState.getLegalActions(agentIndex)
            opAction = actions[0]
            for action in actions:
                oldv = v
                v = max(v, minValue(depth+1, gameState.generateSuccessor(agentIndex, action), alpha, beta)[0])
                if oldv != v:
                    opAction = action
                if v > beta:
                    return v, action
                alpha = max(alpha, v)
            return v, opAction
       
        def minValue(depth, gameState, alpha, beta):
            """
            :return value and action
            :rtype int, str
            """
            if gameState.isWin() or gameState.isLose() or depth == gameState.getNumAgents() * self.depth + 1:
                return self.evaluationFunction(gameState), 'Left'

            v = oo 
            agentIndex = (depth - 1) % gameState.getNumAgents()
            actions = gameState.getLegalActions(agentIndex)
            opAction = actions[0]
            for action in actions:
                oldv = v
                if agentIndex == gameState.getNumAgents() - 1:
                    v = min(v, maxValue(depth+1, gameState.generateSuccessor(agentIndex, action), alpha, beta)[0])
                else:
                    v = min(v, minValue(depth+1, gameState.generateSuccessor(agentIndex, action), alpha, beta)[0])
                if oldv != v:
                    opAction = action
                if v < alpha:
                    return v, action
                beta = min(beta, v)
            return v, opAction

        oo = 1e9
        return maxValue(1, gameState, -oo, oo)[1]

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
        #util.raiseNotDefined()
        bestValue = -1e10
        bestAction = Directions.STOP
        for action in gameState.getLegalActions(0):
            value = self.getValue(gameState.generateSuccessor(0, action), 0, 1)
            if value > bestValue:
                bestAction = action
                bestValue = value
        return bestAction
    
    def isTerminal(self, gameState, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return True
        return False

    def getValue(self, gameState, depth, agentIndex):
        if self.isTerminal(gameState, depth):
            return self.evaluationFunction(gameState)

        if agentIndex == 0:
            return self.getMax(gameState, depth)
        else:
            return self.getExp(gameState, depth, agentIndex)

    def getMax(self, gameState, depth):
        v = -1e9
        for action in gameState.getLegalActions(0):
            v = max(v, self.getValue(gameState.generateSuccessor(0, action), depth, 1))
            #if v >= beta:
            #    return v
            #alpha = max(alpha, v)
        return v

    def getExp(self, gameState, depth, agentIndex):
        v = 0
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            #p = len(actions)
            if agentIndex == gameState.getNumAgents() - 1:
                v += self.getValue(gameState.generateSuccessor(agentIndex, action), depth+1, 0)
            else:
                v += self.getValue(gameState.generateSuccessor(agentIndex, action), depth, agentIndex+1)
        return v
            





def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    # Useful information you can extract from a GameState (pacman.py)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    #oldFood = currentGameState.getFood()
        #print('*****')
        #print(successorGameState)
        #print(newPos)
        #print(newFood)
        #print(newGhostStates[0].getPosition())
        #print(newScaredTimes)
        #print('*****')
    if currentGameState.isWin():
        return 1e9
    if currentGameState.isLose():
        return -1e9
    for ghost in newGhostStates:
        if util.manhattanDistance(ghost.getPosition(), newPos) < 2:
            return -1e7

    score = scoreEvaluationFunction(currentGameState)
    foodDistance = []
    for food in newFood.asList():
        foodDistance.append(util.manhattanDistance(food, newPos))
    
    score = score - 2*min(foodDistance) - max(foodDistance) - 8*currentGameState.getNumFood() + random.randrange(1, 2) 

    return score

# Abbreviation
better = betterEvaluationFunction
