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

        #Kho???ng c??ch t??? food t???i pacman
        foodDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]

        closetFood = 1
        if len(foodDistances) > 0:
            closetFood = min(foodDistances)

        #Kho???ng c??ch t??? ghost t???i pacman
        ghostPositions = successorGameState.getGhostPositions()
        dis_ghost_pacman = [manhattanDistance(newPos, ghost) for ghost in ghostPositions]
        
        # ??i???m ????nh gi?? t??? kho???ng c??ch pacman ?????n th???c ??n g???n nh???t
        point = 1 / closetFood * 10

        # ??i???m ????nh gi?? t??? v??? tr?? ghost t???i v??? tr?? pacman
        # C??ng g???n th?? ??i???m c??ng th???p
        for dis in dis_ghost_pacman:
            if (dis == 0):
                point-=999
            elif (dis == 1):
                point-=1/dis
            else:
                point+=1/dis
        
        # Ki???m tra xem v??? tr?? hi???n t???i c?? th???c ??n ko
        if newPos in currentGameState.getFood().asList():
            point += 10

        # D???ng l???i lu??n kh??ng l?? gi???i ph??p t???i ??u
        if action == 'Stop':
            point = 0

        return point


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "* YOUR CODE HERE *"
        def maxLevel(gameState, depth):

            currentDepth = depth + 1

            # N???u th???ng ho???c thua th?? tr??? v??? h??m ????nh gi??
            if gameState.isWin() or gameState.isLose() or currentDepth == self.depth:
                return self.evaluationFunction(gameState)

            # ????? quy t??m gi?? tr??? max cho pacman
            maxValue = -float('inf')
            actions = gameState.getLegalActions(0)
            for action in actions:
                successor = gameState.generateSuccessor(0, action)
                maxValue = max(maxValue, minLevel(successor, currentDepth, 1))
            return maxValue
        
        numberOfGhosts = gameState.getNumAgents() - 1

        def minLevel(gameState, depth, agentIndex):

            # N???u th???ng ho???c thua th?? tr??? v??? h??m ????nh gi??
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            # ????? quy t??m gi?? tr??? min c???a ghost
            minValue = float('inf')
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == numberOfGhosts:
                    minValue = min(minValue, maxLevel(successor, depth))
                else:
                    minValue = min(minValue, minLevel(successor, depth, agentIndex + 1))
            return minValue
        

        # ????nh gi?? action n??o s??? cho ??i???m chu???n cao nh???t
        currentScore = -float('inf')
        bestAction = ''
        for action in gameState.getLegalActions(0):
            score = minLevel(gameState.generateSuccessor(0, action), 0, 1)
            if score > currentScore:
                currentScore = score
                bestAction = action
        return bestAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -float('inf')
        beta = float('inf')
        def maxLevel(gameState, depth, alpha, beta):
            currentDepth = depth + 1
            if gameState.isWin() or gameState.isLose() or currentDepth == self.depth:
                return self.evaluationFunction(gameState)

            maxValue = -float('inf')
            actions = gameState.getLegalActions(0)

            for action in actions:
                successor = gameState.generateSuccessor(0, action)
                maxValue = max(maxValue, minLevel(successor, currentDepth, 1, alpha, beta))
                if maxValue > beta:
                    return maxValue
                alpha = max(alpha, maxValue)
            return maxValue

        numberOfGhosts = gameState.getNumAgents() - 1

        def minLevel(gameState, depth, agentIndex, alpha, beta):
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            minValue = float('inf')

            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == numberOfGhosts:
                    minValue = min(minValue, maxLevel(successor, depth, alpha, beta))
                    if minValue < alpha:
                        return minValue
                    beta = min(minValue, beta)
                else:
                    minValue = min(minValue, minLevel(successor, depth, agentIndex + 1, alpha, beta))
                    if minValue < alpha:
                        return minValue
                    beta = min(minValue, beta)
            return minValue

        currentScore = -float('inf')
        bestAction = ''
        for action in gameState.getLegalActions(0):
            score = minLevel(gameState.generateSuccessor(0, action), 0, 1, alpha, beta)
            if score > currentScore:
                currentScore = score
                bestAction = action
            if score > beta:
                return bestAction
            alpha = max(alpha, score)
        return bestAction


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

        # L???y gi?? tr??? max c???a pacman
        def maxLevel(gameState, depth):

            currentDepth = depth + 1

            # N???u th???ng ho???c thua th?? tr??? v??? h??m ????nh gi??
            if gameState.isWin() or gameState.isLose() or currentDepth == self.depth:
                return self.evaluationFunction(gameState)
            
            # ????? quy t??m gi?? tr??? max cho pacman
            maxValue = -float('inf')
            actions = gameState.getLegalActions(0)
            for action in actions:
                successor = gameState.generateSuccessor(0, action)
                maxValue = max(maxValue, chanceNode(successor, currentDepth, 1))
            return maxValue
        
        numberOfGhosts = gameState.getNumAgents() - 1

        # Tr??? v??? trung b??nh c???a c??c chaneNode(c??c ghost)
        def chanceNode(gameState, depth, agentIndex):

            # N???u th???ng ho???c thua th?? tr??? v??? h??m ????nh gi??
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            # ????? quy t??m gi?? tr??? t???ng tr???ng s??? c??c tr???ng th??i cu???i c??ng
            avgValue = 0
            legalActions = gameState.getLegalActions(agentIndex)
            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == numberOfGhosts:
                    avgValue = avgValue + maxLevel(successor, depth)
                else:
                    avgValue = avgValue + chanceNode(successor, depth, agentIndex + 1)
            return avgValue/len(legalActions)
        

        # ????nh gi?? xem action n??o c?? gi?? tr??? trung b??nh cao nh???t
        currentScore = -float('inf')
        bestAction = ''
        for action in gameState.getLegalActions(0):
            score = chanceNode(gameState.generateSuccessor(0, action), 0, 1)
            if score > currentScore:
                currentScore = score
                bestAction = action
        return bestAction


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    # L???y th??ng tin h???u ??ch
    foodPositions = currentGameState.getFood().asList()
    pacmanPosition = currentGameState.getPacmanPosition()
    ghostPosition = currentGameState.getGhostPositions()

    # V??? tr?? th???c ??n g???n nh???t
    closetFood = 1
    if len(foodPositions) != 0: 
        closetFood = min([manhattanDistance(food, pacmanPosition) for food in foodPositions])

    # T??nh ??i???m
    # Th???c ??n c??ng g???n => c??ng cao
    score = 1/closetFood * 10

    #X??t v??? tr?? ghost, ghost c??ng g???n ??i???m c??ng th???p
    for ghost in ghostPosition:
        temp = manhattanDistance(pacmanPosition, ghost)
        if temp == 0:
            score -=999
        elif temp <= 1:
            score -= 1/temp

    return currentGameState.getScore() + score

# Abbreviation
better = betterEvaluationFunction
