import random
import ipdb


class eightBlock():

    def __init__(self, positions = None):
        '''The most important step in this initial init is defining the initial 
        board configuration. Calling init with no positions will just randomly 
        shuffle valid_vals. Otherwise, we'll start with the positions given, 
        assuming it is a list containing only integers 0 through 8
        '''
        self.valid_vals = [i for i in range(9)]
        self.valid_inds = [i for i in range(3)]
        if positions is None:
            random.shuffle(self.valid_vals)
            self.board_config = self.valid_vals
        elif isinstance(positions, list):
            if sorted(positions) == self.valid_vals:
                self.board_config = positions
            else:
                v_msg = "positions must be a permutation of integers 0-8"
                raise ValueError(v_msg)
        else:
            inpt_tp = type(positions).__name__
            t_msg = "positions must be a list, not {}".format(inpt_tp)
            raise TypeError(t_msg)
            
    def display_board(self, board = None):
        '''Will display a given board configuration in 3 X 3 form.

        If called with board = None, we'll simply display whatever the current 
        value of self.board_config is. You can also pass in a possible child
        configuration like those output from the move left, right, up, and down 
        functions. If given an empty list, this will simply print out a message 
        about the move being invalid.
        '''
        if isinstance(board, list) and not board:
            print("Invalid move...cannot display")
        else:
            if board is None:
                board = self.board_config
            for r in self.valid_inds:
                print(board[3*r:3*(r + 1)])

    def get_misplaced_values(self):
        '''scans self.board_config and returns a list of misplaced values
        against the assumed goal state of [1,2,3,4,5,6,7,8,0].

        By extension, this will return an empty list if the board is solved
        '''
        misplaced = []
        for v in self.board_config:
            if (v == 0) and (self.board_config.index(v) != 8):
                misplaced.append(v)
            elif (v != 0) and (self.board_config.index(v) != (v - 1)):
                misplaced.append(v)
        return misplaced

    def get_row(self, board_val):
        '''Given a value 0-8, this function will return the row where that 
        value currently is
        '''
        curr_ind = self.board_config.index(board_val)
        return int(curr_ind/3)

    def get_col(self, board_val):
        '''Given a value 0-8, this function will return the column where that 
        value currently is
        '''
        curr_ind = self.board_config.index(board_val)
        return curr_ind % 3

    def mv_left(self):
        '''Moves the zero in the current board configuration to the left if
        possible. Otherwise returns an empty list
        '''
        next_board = []
        z_col = self.get_col(0)
        if (z_col - 1) in self.valid_inds:
            next_board.extend(self.board_config)
            z_ind = next_board.index(0)
            swap_v = next_board[z_ind - 1]
            next_board[z_ind - 1] = 0
            next_board[z_ind] = swap_v
        return next_board

    def mv_right(self):
        '''Moves the zero in the current board configuration to the right if
        possible. Otherwise returns an empty list
        '''
        next_board = []
        z_col = self.get_col(0)
        if (z_col + 1) in self.valid_inds:
            next_board.extend(self.board_config)
            z_ind = next_board.index(0)
            swap_v = next_board[z_ind + 1]
            next_board[z_ind + 1] = 0
            next_board[z_ind] = swap_v
        return next_board

    def mv_up(self):
        '''Moves the zero in the current board configuration up if possible. 
        Otherwise returns an empty list
        '''
        next_board = []
        z_row = self.get_row(0)
        if (z_row - 1) in self.valid_inds:
            next_board.extend(self.board_config)
            z_ind = next_board.index(0)
            swap_v = next_board[z_ind - 3]
            next_board[z_ind - 3] = 0
            next_board[z_ind] = swap_v
        return next_board

    def mv_down(self):
        '''Moves the zero in the current board configuration down if possible. 
        Otherwise returns an empty list
        '''
        next_board = []
        z_row = self.get_row(0)
        if (z_row + 1) in self.valid_inds:
            next_board.extend(self.board_config)
            z_ind = next_board.index(0)
            swap_v = next_board[z_ind + 3]
            next_board[z_ind + 3] = 0
            next_board[z_ind] = swap_v
        return next_board

    def get_next_boards(self):
        nxts = [self.mv_left(), self.mv_right(), self.mv_up(), self.mv_down()]
        return [x for x in nxts if x]






if __name__ == "__main__":
    
    foo = eightBlock()
    # Display the board properly
    foo.display_board()

    # Index into things properly
    for v in range(len(foo.valid_vals)):
        r = foo.get_row(v)
        c = foo.get_col(v)
        print("{} located at position ({},{})".format(v, r, c))

    # Test whether the board is solved
    wrongs = foo.get_misplaced_values()
    if not wrongs:
        print("Board is solved!")
    else:
        print("These are out of place: {}".format(wrongs))

    # Try to move the empty slot in all possible directions
    print("Moving Left...")
    foo.display_board(foo.mv_left())
    print()

    print("Moving Right...")
    foo.display_board(foo.mv_right())
    print()

    print("Moving Up...")
    foo.display_board(foo.mv_up())
    print()

    print("Moving Down...")
    foo.display_board(foo.mv_down())
    print()

    # print("Another way to do this ...")
    # for q in foo.get_next_boards():
    #     foo.display_board(q)
    #     print()

    ipdb.set_trace()




    