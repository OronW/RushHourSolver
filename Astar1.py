from State import State
import copy
import math
from Node1 import Node
from heapq import heappop as pop
from heapq import heappush as push
from time import time


class Astar:

    def __init__(self, puzzle, max):
        currentState = State(puzzle)
        self.first_node=Node(currentState, 0)

        self.path=[]
        self.path.append(self.first_node)

        self.max_tries=max
        self.d = dict()
        self.Open_dic = dict()
        self.Close_dic = dict()
        self.state_id = 1
        self.Close = []
        self.Open = []





    #Min heap funcs
    def openPush(self, node):
        key = node.F
        push(self.Open, (key, node))



    def closePush(self, node):
        #OPT1: CLOSE IS HEAP
        key = node.F
        push(self.Close, (key, node))
        #OPT 2: CLOSE IS LIST
        #self.Close.append(node)

    """
    def closePop(self):
        v=pop(self.Close)
        if v == None:
            return v
        else:
            return v[1]
    """


    def openPop(self):
        v=pop(self.Open)
        if v == None:
            return v
        else:
            return v[1]


    def removeNode(self, l, value):
        n=len(l)
        #Open heap:

        for i in range(0,n):
            if (l[i][1].name==value):
                l.pop(i)
                return

    def solveHeap(self, max_time, H, printStats):

        if (H == 1):
            self.first_node.F = self.H1(self.first_node.state)
        elif (H == 2):
            self.first_node.F = self.H2(self.first_node.state)
        else:
            self.first_node.F = self.H3(self.first_node.state)

        start = time()
        #insert beginning of puzzle to Open
        self.openPush(self.first_node)
        self.Open_dic.update({self.first_node.name: self.first_node.F})

        # while (self.Open) and (time()-start < max_time):
        while self.Open:
            currentNode = self.openPop()

            #check if solved
            if(currentNode.state.isGoalState()):
                #DONE:
                end = time()
                t = end - start
                result = [self.printSolutionHeap(currentNode),currentNode.depth+1,t]
                if (printStats):
                    ebf=self.getEBF()
                    depth_ratio = self.getDepthRatio()
                    H_avg = self.getHeuristicAverage()
                    tree_depth = self.getTreeDepth()
                    N = self.countNodes()
                    result = [ebf, depth_ratio, H_avg, tree_depth, N, t]

                return result


            #put node in CLOSED
            self.closePush(currentNode)
            self.Close_dic.update({currentNode.name: currentNode.F})

            #Expand node
            self.expand(currentNode, H)

        end = time()
        if (not self.Open):
            print("Open empty; solution not found")

        #open is empty; no solution
        #print("Failed!")
        #print("Total time: ",end-start)
        result = None
        if (printStats):
            ebf = self.getEBF()
            depth_ratio = self.getDepthRatio()
            H_avg = self.getHeuristicAverage()
            tree_depth = self.getTreeDepth()
            N=self.countNodes()
            result = [ebf, depth_ratio, H_avg, tree_depth, N, end-start]

        return result

    def expand(self, node, H):
        moves = node.moves
        n = len(moves)
        depth = node.depth

        currentState = node.state

        if (n==0):
            print("Solution not found")
            return False

        for i in range (0,n):
            #copy current state
            nextState = copy.deepcopy(currentState)

            #perform move [i]
            nextState.run_command(moves[i][-3:])
            s = nextState.get_string_board()

            # Eval nextState
            if (H==1):
                h = self.H1(nextState)
            elif (H==2):
                h = self.H2(nextState)
            else:
                h = self.H3(nextState)


            f = h + depth + 1

            """CASE 1 : new state is neither in OPEN nor in CLOSE"""
            if (not s in self.Open_dic) and (not s in self.Close_dic):
                # Create child node
                nextNode = Node(nextState, depth + 1)
                nextNode.F = f
                nextNode.parent = node
                nextNode.previous_move = moves[i]

                #insert child node to OPEN
                self.openPush(nextNode)
                self.Open_dic.update({s: f})


            #CASE 2: nextState in OPEN and our value is better
            elif (s in self.Open_dic):
                other_F = self.Open_dic.get(s)
                if (other_F>f):
                    # DO: Repalce previous state with this state

                    # Create child node
                    nextNode = Node(nextState, depth + 1)
                    nextNode.F = f
                    nextNode.parent = node
                    nextNode.previous_move = moves[i]

                    #Replace nodes
                    self.removeNode(self.Open, s)
                    self.openPush(nextNode)

                    #update dic
                    self.Open_dic.update({s: f})


            # CASE 3: nextState in CLOSE and our value is better
            elif (s in self.Close_dic):
                other_F = self.Close_dic.get(s)
                if (other_F > f):
                    #DO: Repalce previous state with this state
                    #Move this state to OPEN

                    # Create child node
                    nextNode = Node(nextState, depth + 1)
                    nextNode.F = f
                    nextNode.parent = node
                    nextNode.previous_move = moves[i]

                    # remove old node
                    self.removeNode(self.Close, s)

                    #put node in OPEN
                    self.openPush(nextNode)

                    # update both dictionaries
                    self.Open_dic.update({s: f})
                    self.Close_dic.pop(s)


        return True





    def H1(self, state):     # Heuristic returns the number of blocked squares in path of red car
        h=0
        goalcar = state.get_board().get_vehicle('X')
        x = int(goalcar.top_left / 6)
        y = goalcar.top_left % 6
        y = y + goalcar.get_length()


        for i in range(y, 6):
            if (state.get_string_board()[x*6+i]!='.'):
                h+=1

        return h



    def H2(self, state):    # Heuristic returns the number of blocked squares in path of red car + sizes of blocking cars
        h = 0
        goalcar = state.get_board().get_vehicle('X')
        x = int(goalcar.top_left / 6)
        y = goalcar.top_left % 6
        y = y + goalcar.get_length()

        for i in range(y, 6):
            c = state.get_string_board()[x*6+i]
            if (c != '.'):
                blocking_car = state.get_board().get_vehicle(c)
                h += blocking_car.size + 1


        return h


    def H3(self, state):
        h = 0
        goalcar = state.get_board().get_vehicle('X')
        x = int(goalcar.top_left / 6)
        y = goalcar.top_left % 6
        y = y + goalcar.get_length()
        blocking_cars = []

        for i in range(y, 6):
            c = state.get_string_board()[x*6+i]
            if (c != '.'):
                car = state.get_board().get_vehicle(c)
                h += 1
                if (not state.isFree(car)):
                    # Car cannot clear the way, punish the heuristic
                    h+=car.get_length()

        return h


   # given string s of a state,
    def isNewState(self, state):
        s=state.boardToString()
        if (s in self.d):
            return False
        else:
            return True

    def updateDict(self, obj, key):
        if (type(obj) is State):
            s = obj.boardToString()
        elif (type(obj) is Node):
            s=obj.state.boardToString()
        else:
            #unknown obj type
            print("UpdateDict: unknown object type")
            return False

        self.d.update({s: key})
        self.state_id += 1


    def goalState(self, node):
        return node.state.isGoalState()


    def printSolution(self):
        solution=""
        i=self.path.__len__()-1
        while(i>0):
            solution=path[i].previous_move[-3:]+" "+solution
            i-=1

        return solution

    def printSolutionHeap(self, node):
        solution=""
        ebf=0
        head = copy.deepcopy(node)
        path=[]
        while (node.parent != None):
            path.append(node)
            ebf += node.BF
            node=node.parent

        for i in range(0,len(path)):
            solution=path[i].previous_move[-3:]+" "+solution

        if (head == None):
            print("HEAD NONE")
        solution = solution +" "+ self.lastMove(head)

        return solution




    def move2str(self, node):
            m=node.previous_move
            car = m[4]
            dir = ""
            amount = max( abs(m[2]), abs(m[3]))


            #Horizontal movement
            if (m[2]>0):
                dir='R'
            elif (m[2]<0):
                dir='L'

            #Vertical movement
            elif (m[3]>0):
                dir = 'D'
            elif (m[3]<0):
                dir = 'U'

            else:
                print("move2str: invalid move")
                return None

            return car+dir+str(amount)


    def lastMove(self, node):
        steps_to_end = 6 - (node.state.get_board().get_vehicle('X').bottom_right % 6)

        return "XR" + str(steps_to_end)
    def getEBF(self):
        allNodes = self.Open + self.Close
        ebf=0
        n=len(allNodes)
        for i in range (0,n):
            ebf+=allNodes[i][1].BF

        return ebf/n


    def getTreeDepth(self):
        treeNodes = self.Open
        n = len(treeNodes)
        min=math.inf
        max=0
        avg=0

        for i in range(0, n):
            d = treeNodes[i][1].depth
            if (d<min):
                min=d
            if (d>max):
                max=d
            avg+=d

        avg=avg/n
        return [min, avg, max]




    def getHeuristicAverage(self):
        allNodes = self.Open + self.Close
        h = 0
        n = len(allNodes)
        for i in range(0, n):
            h+=allNodes[i][1].F - allNodes[i][1].depth

        return h/n



    def getDepthRatio(self):
        treeNodes = self.Open
        n = len(treeNodes)
        max_depth = 0
        N = n + len(self.Close)

        for i in range(0, n):
            d = treeNodes[i][1].depth
            if (d > max_depth):
                max_depth = d

        return max_depth/N

    def countNodes(self):
        return len(self.Open)+len(self.Close)