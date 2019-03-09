from Play_tools import Vehicle, Board


class State:
    def __init__(self, _boardobj):
        # 3 bit solution - 1. regular/special 2. H/V 3.2/3
        self.bin_state = ''
        for c in _boardobj.get_board():
            first_bit = str(int(c == '.' or c == 'X'))
            if c != '.':
                second_bit = str(int(_boardobj.get_vehicle(c).get_direction() == 'V'))
                third_bit = str(int(_boardobj.get_vehicle(c).get_direction() == 3))
            else:
                second_bit = '0'
                third_bit = '1'
            self.bin_state += first_bit + second_bit + third_bit
