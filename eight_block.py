import random
import ipdb


class eightBlock():

    def __init__(self, positions = None):
        '''The most important step in this initial init is defining the initial 
        board configuration. Calling init with no positions will just randomly 
        shuffle valid_vals. Otherwise, we'll start with the positions given, 
        assuming it is a list containing only integers 0 through 8


        TKTK Might want to initialize each of these with a goal state, too. Just
        to be explicit about it
        '''
        self.valid_vals = [i for i in range(9)]
        self.valid_dims = [i for i in range(3)]
        self.valid_dirs = ["left","right","up","down"]
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
            for r in self.valid_dims:
                print(board[3*r:3*(r + 1)])

    def get_misplaced_values(self):
        '''scans self.board_config and returns a list of misplaced values
        against the assumed goal state of [1,2,3,4,5,6,7,8,0].

        By extension, this will return an empty list if the board is solved

        TKTK: RIGHT NOW THIS ASSUMES A GOAL STATE. This would need to change
        if goal_state was ever defined as a part of the class itself
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

    def make_move(self, mv_dir):
        '''Moves the zero in the current board configuration in the direction 
        specified by mv_dir. Will return the updated configuration if that 
        direction is valid. Returns an empty list otherwise
        '''
        if mv_dir not in self.valid_dirs:
            d_msg = "direction must be {}".format(", ".join(self.valid_dirs))
            raise ValueError(d_msg)
        next_board = []
        dim_chk = self.get_row(0) if mv_dir in ["up","down"] else self.get_col(0)
        chk_val = -1 if mv_dir in ["left","up"] else 1
        if (dim_chk + chk_val) in self.valid_dims:
            next_board.extend(self.board_config)
            z_ind = next_board.index(0)
            mv_amt = 3 * chk_val if mv_dir in ["up","down"] else chk_val
            swap_v = next_board[z_ind + mv_amt]
            next_board[z_ind + mv_amt] = 0
            next_board[z_ind] = swap_v
        return next_board

    def get_next_boards(self):
        '''Will attempt to move the zero of the current board configuration in 
        all possible directions: left, right, up, and down.

        Returns a list of those next configurations that are valid (i.e., the
        ones that aren't empty lists)

        TKTK: Option to exclude direction made in prior call?
        '''
        nxts = [self.make_move(mv_dir) for mv_dir in self.valid_dirs]
        return [x for x in nxts if x]


class depthFirstSearchSolver(eightBlock):

    def __init__(self, positions = None):
        '''Still reserving the option to define a starting position. Only 
        adding an array that keeps track of the moves_made function
        '''
        self.moves_made = []
        super().__init__(positions)

    def solve(self):
        if self.get_misplaced_values():
            print("board is not solved...shit")
        else:
            print("MY WORK HERE IS DONE")



if __name__ == "__main__":
    
    foo = depthFirstSearchSolver()
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

    print("Moving zero {}".format(", ".join(foo.valid_dirs)))
    for q in foo.get_next_boards():
        foo.display_board(q)
        print()

    # ipdb.set_trace()

    bar = depthFirstSearchSolver([1,2,3,4,5,6,7,8,0])
    ipdb.set_trace()




    