from State import State
import copy
import math
import hashlib
from collections import defaultdict




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
        self.BF = len(_state.find_next_steps())

        #depth : how many moves to get this state
        self.depth = _depth

        #Estimation of distance from goal state
        self.F = 0

        #pointer to parent node
        self.parent = None



    def __lt__(self, other):
        return self.F < other.F