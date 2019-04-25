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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    if(problem.isGoalState(startState)):
        return [] # no need to explore if start state is goal state
    
    # What type of frontier to use? Stack, FIFO or priority queue
    frontier = util.Stack()
    frontier.push(startState) # pushing initial state in stack
    explored = set() # to track explored nodes for graph search
    parentMap = {} # to traceback path to initial state from goal state
    actionMap = {}
    while True:
        if frontier.isEmpty():
            return [] # no solution, can't reach goal state after exploring all nodes
        node = frontier.pop() # getting node to explore
#        print "pop: ", node , "<--" , parentMap.get(node)
        if problem.isGoalState(node):
#            print "Goal State: ", node
            actionList = solution(node, parentMap, actionMap)
            return  actionList
        explored.add(node) # mark the state as explored
        for suc in (problem.getSuccessors(node)): 
            # Using 'reversed' was a bit costly for medium sized maze
#            print(suc)
            if suc[0] not in explored:
#                print "push:", suc
                frontier.push(suc[0])
                actionMap[suc[0]] = suc[1]
                parentMap[suc[0]] = node
#    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    if(problem.isGoalState(startState)):
        return [] # no need to explore if start state is goal state
    
    # What type of frontier to use? Stack, FIFO or priority queue
    frontier = util.Queue()
    frontier.push(startState) # pushing initial state in queue
    explored = set() # to track explored nodes for graph search
    parentMap = {}  # to traceback path to initial state from goal state
    actionMap = {} 
    while True:
        if frontier.isEmpty():
            return [] # no solution, can't reach goal state after exploring all nodes
        node = frontier.pop() # getting node to explore
#        print "pop: ", node , "<--" , parentMap.get(node)
        if problem.isGoalState(node):
#            print "Goal State: ", node
#            print(parentMap)
            actionList = solution(node, parentMap, actionMap)                    
            return  actionList
        
        explored.add(node) # mark the state as explored
        for suc in (problem.getSuccessors(node)): 
            # Using 'reversed' was a bit costly for medium sized maze
#            print(suc)
            if suc[0] not in explored and suc[0] not in frontier.list:
#                print "push:", suc
                frontier.push(suc[0])
                actionMap[suc[0]] = suc[1]
                parentMap[suc[0]] = node

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    if(problem.isGoalState(startState)):
        return [] # no need to explore if start state is goal state
    
    # What type of frontier to use? Stack, FIFO or priority queue
    frontier = util.PriorityQueue()
    frontier.push(startState, 0) # pushing initial state and initial cost 0 in priority queue
    explored = set() # to track explored nodes for graph search
    parentMap = {} # to traceback path to initial state from goal state
    actionMap = {}
    counter = util.Counter()
    while True:
        if frontier.isEmpty():
            return [] # no solution, can't reach goal state after exploring all nodes
        node = frontier.pop() # getting node to explore
        
        if problem.isGoalState(node): #unlike DFS&BFS, we want to find optimal goal, not the goal that is explored first
            actionList = solution(node, parentMap, actionMap)
            return  actionList
        
        explored.add(node) # mark the state as explored
        for suc in (problem.getSuccessors(node)): 
            cost = counter[node] + suc[2] # cumulative cost
#            print suc, ":::", cost
            if suc[0] not in explored and counter[suc[0]] == 0:
#                print "push:", suc
                frontier.push(suc[0], cost)
                counter[suc[0]] = cost
                actionMap[suc[0]] = suc[1]
                parentMap[suc[0]] = node
            elif cost < counter[suc[0]]:
                frontier.update(suc[0], cost) # updating frontier with lowest cost of same item
                actionMap[suc[0]] = suc[1]
                parentMap[suc[0]] = node

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    if(problem.isGoalState(startState)):
        return [] # no need to explore if start state is goal state
    
    # What type of frontier to use? Stack, FIFO or priority queue
    frontier = util.PriorityQueue()
    frontier.push(startState, 0) # pushing initial state and initial cost 0 in priority queue
    explored = set() # to track explored nodes for graph search
    parentMap = {} # to traceback path to initial state from goal state
    actionMap = {}
    counter = util.Counter()
    while True:
        if frontier.isEmpty():
            return [] # no solution, can't reach goal state after exploring all nodes
        node = frontier.pop() # getting node to explore
#        print "pop::", node
        if problem.isGoalState(node): #unlike DFS&BFS, we want to find optimal goal, not the goal that is explored first
#           print "Goal State: ", suc
            actionList = solution(node, parentMap, actionMap)
            return  actionList
        
        explored.add(node) # mark the state as explored
        for suc in (problem.getSuccessors(node)):
            parentHeuristic = heuristic(node, problem)
            childHeuristic = heuristic(suc[0], problem)
            cost = counter[node] + suc[2] + childHeuristic - parentHeuristic
#            print "parent:", node, "::heu::", parentHeuristic
#            print "child:", suc, "::heu::", childHeuristic, "::cost::", cost
            if suc[0] not in explored and counter[suc[0]] == 0:
#                print "push:", suc
                frontier.push(suc[0], cost)
                counter[suc[0]] = cost
                actionMap[suc[0]] = suc[1]
                parentMap[suc[0]] = node
            elif cost < counter[suc[0]]:
                frontier.update(suc[0], cost) # updating frontier with lowest cost of same item
                actionMap[suc[0]] = suc[1]
                parentMap[suc[0]] = node   


def solution(goalState, parentMap, actionMap):
    actionList = []
    parent = parentMap.get(goalState)
    currAction = actionMap.get(goalState)
    actionList.insert(0, currAction)
    while True:
#        print parent
        action = actionMap.get(parent)
        if action is not None:
            actionList.insert(0, action)
        parent = parentMap.get(parent)
        if parent is None:
            break
#    print(actionList)
    return actionList
        
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
