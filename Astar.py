from Play_tools import Board
from State import State
from heapq import heappop as pop
from heapq import heappush as push
import math
import copy
from time import time


class Astar:

    def __init__(self, puzzle):
        curr_state = State(puzzle)
        self.first_node = Node(curr_state, 0)

        self.path = []
        self.path.append(self.first_node)

        self.d = dict()
        self.Open_dic = dict()
        self.Close_dic = dict()
        self.state_id = 1
        self.Close = []
        self.Open = []

    def open_push(self, node):
        key = node.F
        push(self.Open, (key, node))

    def open_pop(self):
        v = pop(self.Open)
        if v is None:
            return v

        return v[1]

    def close_push(self, node):
        key = node.F
        push(self.Close, (key, node))

    def remove_node(self, l, value):
        n = len(l)
        # Open heap:

        for i in range(0, n):
            if (l[i][1].name == value):
                l.pop(i)
                return

    def solve(self, max_time, _heuristic, DB):

        if _heuristic == 1:
            self.first_node.F = self.H1(self.first_node.state)
        else:
            self.first_node.F = self.H2(self.first_node.state)

        start = time()
        flag = 0
        # insert beginning of puzzle to Open
        self.open_push(self.first_node)
        self.Open_dic.update({self.first_node.name: self.first_node.F})

        while (self.Open) and (time()-start < max_time):
            currentNode = self.open_pop()
            res = DB.get_next(currentNode.state)
            if res == 0:
                continue
            if res != 1:
                while True:
                    self.close_push(currentNode)
                    self.Close_dic.update({currentNode.name: currentNode.F})
                    self.expand_from_DB(currentNode, H, res)
                    currentNode = self.open_pop()
                    res = DB.get_next(currentNode.state)
                    if res == 1:
                        flag = 1
                        break

            # check if solved
            if (flag == 1) or (currentNode.state.final_move()):
                # DONE:
                end = time()
                t = end - start
                result = [self.printSolutionHeap(currentNode, DB, flag), currentNode.depth + 1, t]
                return result

            # put node in CLOSED
            self.close_push(currentNode)
            self.Close_dic.update({currentNode.name: currentNode.F})

            # Expand node
            self.expand(currentNode, _heuristic)

        end = time()
        if (not self.Open):
            print("Open empty; solution not found")

        result = None

        return result

    def expand(self, node, _heuristic):
        moves = node.moves
        n = len(moves)
        depth = node.depth

        curr_state = node.state

        if (n == 0):
            print("Solution not found")
            return False

        for i in range(0, n):
            # copy current state
            next_state = copy.deepcopy(curr_state)

            # perform move [i]
            next_state.run_command(moves[i][-3:])
            s = next_state.get_string_board()

            # Eval next_state
            if _heuristic == 1:
                h = self.H1(next_state)
            else:
                h = self.H2(next_state)

            f = h + depth + 1

            """CASE 1 : new state is neither in OPEN nor in CLOSE"""
            if (not s in self.Open_dic) and (not s in self.Close_dic):
                # Create child node
                next_node = Node(next_state, depth + 1)
                next_node.F = f
                next_node.parent = node
                next_node.previous_move = moves[i]

                # insert child node to OPEN
                self.open_push(next_node)
                self.Open_dic.update({s: f})


            # CASE 2: next_state in OPEN and our value is better
            elif s in self.Open_dic:
                other_F = self.Open_dic.get(s)
                if other_F > f:
                    # DO: Repalce previous state with this state

                    # Create child node
                    next_node = Node(next_state, depth + 1)
                    next_node.F = f
                    next_node.parent = node
                    next_node.previous_move = moves[i]

                    # Replace nodes
                    self.remove_node(self.Open, s)
                    self.open_push(next_node)

                    # update dic
                    self.Open_dic.update({s: f})


            # CASE 3: next_state in CLOSE and our value is better
            elif s in self.Close_dic:
                other_F = self.Close_dic.get(s)
                if other_F > f:
                    # DO: Repalce previous state with this state
                    # Move this state to OPEN

                    # Create child node
                    next_node = Node(next_state, depth + 1)
                    next_node.F = f
                    next_node.parent = node
                    next_node.previous_move = moves[i]

                    # remove old node
                    self.remove_node(self.Close, s)

                    # put node in OPEN
                    self.open_push(next_node)

                    # update both dictionaries
                    self.Open_dic.update({s: f})
                    self.Close_dic.pop(s)

        return True

    def expand_from_DB(self, node, _heuristic, _command):
        depth = node.depth

        curr_state = node.state

        # copy current state
        next_state = copy.deepcopy(curr_state)

        # perform move
        next_state.run_command(_command)
        s = next_state.get_string_board()

        # Eval next_state
        if (_heuristic == 1):
            h = self.h(next_state)
        else:
            h = self.H2(next_state)

        f = h + depth + 1

        """CASE 1 : new state is neither in OPEN nor in CLOSE"""
        if (not s in self.Open_dic) and (not s in self.Close_dic):
            # Create child node
            next_node = Node(next_state, depth + 1)
            next_node.F = f
            next_node.parent = node
            next_node.previous_move = s + _command

            # insert child node to OPEN
            self.open_push(next_node)
            self.Open_dic.update({s: f})

        return True

    def H1(self, state):  # this heuristic returns the number of blocked squares for the red car
        h = 0
        goalcar = state.get_board().get_vehicle('X')
        x = int(goalcar.top_left / 6)
        y = goalcar.top_left % 6
        y = y + goalcar.get_length()

        for i in range(y, 6):
            if (state.get_string_board()[x * 6 + i] != '.'):
                h += 1

        return h

    def H2(self, _state):  # this heuristic returns the number of blocked squares for the red car + blocking car sizes
        h = 0

        vehicle = _state.get_board().get_vehicle('X')
        start_point = vehicle.top_left + vehicle.get_length()
        steps_to_end = 6 - ((vehicle.top_left + vehicle.get_length()) % 6)

        for i in range(0, steps_to_end+1):
            c = _state.get_string_board()[start_point + i]
            if c != '.':
                blocking_vehicle = _state.get_board().get_vehicle(c)
                h += blocking_vehicle.get_length() + 1

        return h

    # given string s of a state,
    def isNewState(self, state):
        s = state.boardToString()
        if (s in self.d):
            return False
        else:
            return True

    def updateDict(self, obj, key):
        if (type(obj) is State):
            s = obj.boardToString()
        elif (type(obj) is Node):
            s = obj.state.boardToString()
        else:
            # unknown obj type
            print("UpdateDict: unknown object type")
            return False

        self.d.update({s: key})
        self.state_id += 1

    def goalState(self, node):
        return node.state.final_move()

    def printSolution(self):
        solution = ""
        i = self.path.__len__() - 1
        while (i > 0):
            solution = path[i].previous_move[-3:] + " " + solution
            i -= 1

        return solution

    def printSolutionHeap(self, node, _DB, _flag):
        solution = ""
        ebf = 0
        head = copy.deepcopy(node)
        path = []
        if _flag == 0:
            next_move = self.lastMove(head)
        while node.parent != None:
            if _flag == 0:
                _DB.set_next(node.state, next_move)
                next_move = node.previous_move[-3:]
            path.append(node)
            ebf += node.BF
            node = node.parent

        if _flag == 0:
            _DB.set_next(node.state, next_move)

        for i in range(0, len(path)):
            solution = path[i].previous_move[-3:] + " " + solution

        if (head == None):
            print("HEAD NONE")

        if _flag == 0:
            solution = solution + " " + self.lastMove(head)

        return solution

    # def move2str(self, node):
    #     m = node.previous_move
    #     car = m[4]
    #     dir = ""
    #     amount = max(abs(m[2]), abs(m[3]))
    #
    #     # Horizontal movement
    #     if (m[2] > 0):
    #         dir = 'R'
    #     elif (m[2] < 0):
    #         dir = 'L'
    #
    #     # Vertical movement
    #     elif (m[3] > 0):
    #         dir = 'D'
    #     elif (m[3] < 0):
    #         dir = 'U'
    #
    #     else:
    #         print("move2str: invalid move")
    #         return None
    #
    #     return car + dir + str(amount)

    def lastMove(self, node):
        steps_to_end = 6 - (node.state.get_board().get_vehicle('X').bottom_right % 6)

        return "XR" + str(steps_to_end + 1)

    def getEBF(self):
        allNodes = self.Open + self.Close
        ebf = 0
        n = len(allNodes)
        for i in range(0, n):
            ebf += allNodes[i][1].BF

        return ebf / n

    def getTreeDepth(self):
        treeNodes = self.Open
        n = len(treeNodes)
        min = math.inf
        max = 0
        avg = 0

        for i in range(0, n):
            d = treeNodes[i][1].depth
            if (d < min):
                min = d
            if (d > max):
                max = d
            avg += d

        avg = avg / n
        return [min, avg, max]

    def getHeuristicAverage(self):
        allNodes = self.Open + self.Close
        h = 0
        n = len(allNodes)
        for i in range(0, n):
            h += allNodes[i][1].F - allNodes[i][1].depth

        return h / n

    def getDepthRatio(self):
        treeNodes = self.Open
        n = len(treeNodes)
        max_depth = 0
        N = n + len(self.Close)

        for i in range(0, n):
            d = treeNodes[i][1].depth
            if (d > max_depth):
                max_depth = d

        return max_depth / N

    def countNodes(self):
        return len(self.Open) + len(self.Close)

class Node:

    def __init__(self, _state, _depth):

        #state the node represents
        self.state = _state

        #name of state
        self.name = _state.get_string_board()

        #list of possible moves
        self.moves = self.state.find_next_steps()

        #move performed to reach current node
        self.previous_move = None

        #next move to visit
        self.move_index=0

        # branch factor
        self.BF = len(self.moves)

        #depth : how many moves to get this state
        self.depth = _depth

        #Estimation of distance from goal state
        self.F = 0

        #pointer to parent node
        self.parent = None



    def __lt__(self, other):
        return self.F < other.F