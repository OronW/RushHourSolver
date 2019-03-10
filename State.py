from Play_tools import Vehicle, Board
import math
from utils import string_modify, string_switch


class State:
    def __init__(self, _board_obj):
        self.board_state = _board_obj

    def find_next_steps(self):
        board = self.board_state.get_board()
        side = int(math.sqrt(len(board)))
        next_states = []

        # check horizontal
        for i in range(0, (len(board) - 1), side):  # run over rows
            j = 0
            while j < side:  # run over columns
                p = i + j  # set p as position on board
                if board[p] == '.':  # empty square
                    j += 1
                    continue
                if self.board_state.get_vehicle(board[p]).get_direction() == 'V':  # check if vertical
                    j += 1
                    continue

                v_len = self.board_state.get_vehicle(board[p]).get_length()

                # check right
                steps = 0
                temp_state = board
                p_next = p + 1
                while (p_next % side != 0) and (p_next < len(board)) and (board[p_next] == '.'):
                    temp_state = string_switch(temp_state, p_next, p - (v_len - 1))
                    steps += 1
                    next_states.append(temp_state + ',' + temp_state[p] + 'R' + str(steps))
                    p = p_next
                    p_next += 10
                    j += 1

                p = i + j  # set p as position on board
                if p < len(board):
                    v_id = board[p]
                if (p >= len(board)) or \
                        ((board[p] != '.') and
                         (self.board_state.get_vehicle(board[p]).get_direction() == 'V')):  # check if vertical
                    j += 1
                    continue
                # check left
                temp_state = board
                p_next = p - 1
                steps = 0
                while (p_next % side != side - 1) and (board[p_next] == '.'):
                    temp_state = string_switch(temp_state, p_next, p + (v_len - 1))
                    steps += 1
                    next_states.append(temp_state + ',' + temp_state[p] + 'L' + str(steps))
                    p = p_next
                    p_next -= 1
                j += 1

        # check vertical
        for i in range(0, side-1, 1):  # run over columns
            j = 0
            while j < len(board):  # run over rows
                p = i + j  # set p as position on board
                if board[p] == '.':  # empty square
                    j += side
                    continue
                if self.board_state.get_vehicle(board[p]).get_direction() == 'H':  # check if horizontal
                    j += side
                    continue

                v_len = self.board_state.get_vehicle(board[p]).get_length()

                # check down
                temp_state = board
                steps = 0
                p_next = p + side
                while (p_next < len(board)) and (board[p_next] == '.'):
                    temp_state = string_switch(temp_state, p_next, p - ((v_len - 1)*side))
                    steps += 1
                    next_states.append(temp_state + ',' + temp_state[p] + 'D' + str(steps))
                    p = p_next
                    p_next += side
                    j += side
                j += side
                p = i + j  # set p as position on board
                if p < len(board):
                    v_id = board[p]

                if (p >= len(board)) or \
                        ((board[p] != '.') and
                         (self.board_state.get_vehicle(board[p]).get_direction() == 'H')):  # check if horizontal
                    j += side
                    continue
                # check up
                temp_state = board
                p_next = p - side
                steps = 0
                while (p_next >= 0) and (board[p_next] == '.'):
                    temp_state = string_switch(temp_state, p_next, p + ((v_len - 1)*side))
                    steps += 1
                    next_states.append(temp_state + ',' + temp_state[p] + 'U' + str(steps))
                    p = p_next
                    p_next -= side
                j += side

        return next_states

